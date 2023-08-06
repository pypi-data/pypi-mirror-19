#!/mgunther/bob/bob-stable/py27/bin/python

import sys
import os

import bob.core
logger = bob.core.log.setup("challenge.UCCS.FaceRecog")

import bob.io.base
import bob.io.image
import bob.ip.base
import bob.ip.color
import bob.ip.facedetect
import bob.learn.linear
import numpy
import scipy.spatial

import math
import bob.io.base
import multiprocessing

from .. import utils

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--data-directory', '-D', default = "data/UCCS", help = "Select the directory, where image files are stored")
  parser.add_argument('--result-file', '-w', default = "results/UCCS-recognition-baseline.txt", help = "Select the file to write the scores into")
  parser.add_argument('--no-train-on-unknowns', '-u', action='store_true', help = "If selected, the known unknowns will not be used as a separate class")
  parser.add_argument('--eigenvalue-energy', '-e', type = float, default = .99, help = "Select the PCA energy that is kept")
  parser.add_argument('--maximum-scores', '-m', type=int, default=10, help = "Specify, how many scores per validation image should be stored")

  parser.add_argument('--maximum-detections', '-M', type=int, default=20, help = "Specify, how many detections per image should be stored")
  parser.add_argument('--number-of-overlaps', '-o', type=int, default=5, help = "If given, only detections with the given number of overlapping detections are considered")
  parser.add_argument('--absolute-threshold', '-t', type=float, default=10, help = "If given, only detections with predictions above this threshold will be used.")
  parser.add_argument('--relative-threshold', '-T', type=float, default=0.5, help = "Limits detections to those that have a prediction value higher than --relative-threshold * max(predictions)")

  parser.add_argument('--cascade-file', '-r', help = "The file to read the resulting cascade from; If left empty, the default cascade will be loaded")
  parser.add_argument('--distance', '-s', type=int, default=2, help = "The distance with which the image should be scanned.")
  parser.add_argument('--scale-factor', '-S', type=float, default = math.pow(2.,-1./16.), help = "The logarithmic distance between two scales (should be between 0 and 1).")
  parser.add_argument('--lowest-scale', '-f', type=float, default = 0.0625, help = "Faces which will be lower than the given scale times the image resolution will not be found.")
  parser.add_argument('--detection-overlap', '-b', type=float, default=0.25, help = "If given, the average of the overlapping detections with this minimum overlap will be considered.")

  parser.add_argument('--projector-file', default='temp/UCCS-Projector.hdf5', help = "Set intermediate file, where Projector is stored")
  parser.add_argument('--models-file', default='temp/UCCS-Models.hdf5', help = "Set intermediate file, where the models are stored")
  parser.add_argument('--probes-file', default='temp/UCCS-Probes.hdf5', help = "Set intermediate file, where the probes are stored")

  parser.add_argument('--parallel', '-P', type=int, help = "If given, images will be processed with the given number of parallel processes")

  parser.add_argument('--display', '-x', action='store_true', help = "Displays preprocessed images (waits for user keypress)")
  parser.add_argument('--debug', '-q', type=int, help = "Use only the given number of identities")
  parser.add_argument('--force', '-F', action='store_true', help = "If selected, already processed files will be overwritten")


  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.parallel is not None and args.display:
    logger.warn("Disabling --display (-x) as we run in parallel mode")
    args.display = False

  if args.debug is not None:
    temp_dir = "temp-%d" % args.debug
    args.projector_file = args.projector_file.replace("temp", temp_dir)
    args.models_file = args.models_file.replace("temp", temp_dir)
    args.probes_file = args.probes_file.replace("temp", temp_dir)
    args.result_file = args.result_file.replace("baseline", "baseline-%d"%args.debug)
  else:
    bob.io.base.create_directories_safe(os.path.dirname(args.projector_file))
    bob.io.base.create_directories_safe(os.path.dirname(args.models_file))
    bob.io.base.create_directories_safe(os.path.dirname(args.probes_file))

  return args


def _align(image, bbx, args, gts=[], value=0):
  cropper = bob.ip.base.GeomNorm(0., 1., (80,64), (40,32))
  # crop by the bounding box
  # as the images are not aligned inside the bounding box, we crop the center of them
  center = bbx.center
  # set the scale
  cropper.scaling_factor = min(float(cropper.crop_size[0]) / bbx.size[0], float(cropper.crop_size[1]) / bbx.size[1])
  cropped = numpy.ndarray(cropper.crop_size)
  cropper(image, cropped, center)

  if args.display:
    from matplotlib import pyplot, patches
    pyplot.figure("original")
    pyplot.clf()
    pyplot.imshow(image, 'gray', clim=(0,255))
    pyplot.gca().add_patch(patches.Rectangle((bbx.left, bbx.top), bbx.size[1], bbx.size[0], fill=False, color='g', lw=3))
    for gt in gts:
      pyplot.gca().add_patch(patches.Rectangle((gt.left, gt.top), gt.size[1], gt.size[0], fill=False, color='r', lw=3))
    pyplot.figure("cropped")
    pyplot.clf()
    pyplot.imshow(cropped.astype(numpy.uint8), 'gray', clim=(0,255))
    raw_input("Press Enter to continue; %1.5f" % value)
  return cropped

def _feature(face):
  """Extracts a feature for the given face chip.

  Here, the 2-dimensional image is aligned to a 1-dimensional vector.
  """
  return bob.ip.base.lbphs(face, bob.ip.base.LBP(8,1,uniform=True,border_handling='wrap'), block_size=(16,16)).astype(numpy.float64).flatten()


def _extract_training_features(params):
  """Extracts training features and rearranges them by identity"""
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else -1

  dataset, args = params
  # load classifier and feature extractor; each process needs its own cascade
  if args.cascade_file is None:
    if abs(process_id) == 1:
      logger.info("Using default frontal face detection cascade from bob.ip.facedetect")
    cascade = bob.ip.facedetect.default_cascade()
  else:
    if abs(process_id) == 1:
      logger.info("Loading cascade from file '%s'", args.cascade_file)
    cascade = bob.ip.facedetect.detector.Cascade(bob.io.base.HDF5File(args.cascade_file))
  # initialize sampler
  sampler = bob.ip.facedetect.detector.Sampler(patch_size=cascade.extractor.patch_size, distance=args.distance, scale_factor=args.scale_factor, lowest_scale=args.lowest_scale)


  logger.debug("Detecting faces in %d training images%s", len(dataset), (" in process %d" % process_id) if process_id > 0 else "")

  features = {}
  for image_name in dataset:
    # load image
    image = bob.io.base.load(os.path.join(args.data_directory, "training", image_name))
    if image.ndim == 3:
      image = bob.ip.color.rgb_to_gray(image)

    # detect all faces, with a low threshold
    detections, qualities = bob.ip.facedetect.detect_all_faces(image, cascade, sampler, 0, 3, 0.25, 0.)

    for subject, bbx in dataset[image_name]:
      if subject == -1 and args.no_train_on_unknowns:
        continue
      # For the training set:
      # check which of the detected bounding boxes have the best overlap with the GT bounding box
      gt = utils.bounding_box(bbx)
      overlaps = sorted(((utils.overlap(gt, det), det, val) for det, val in zip(detections, qualities)), key=lambda x:x[0], reverse=True)
      if overlaps[0][0] < 0.5:
        logger.warning("Labeled face of training subject %d at location %s in image %s not detected; skipping", subject, gt, image_name)
        continue

      cropped = _align(image, overlaps[0][1], args, [gt], overlaps[0][2])
      if subject not in features:
        features[subject] = []
      features[subject].append(_feature(cropped))

  logger.debug("Finished processing%s" % (" process %d" % process_id) if process_id > 0 else "")
  return features


def _bbx(b,q):
  # turns the BoundingBox C++ object into a (picklable) list so that it can be returned through multiprocessing
  return b.left_f, b.top_f, b.size_f[1], b.size_f[0], q

def _extract_test_features(params):
  """Extracts test features and rearranges them by filename"""
  # get process ID
  p = multiprocessing.current_process().name
  process_id = int(p.split('-')[1]) if p != 'MainProcess' else -1

  dataset, args = params
  # load classifier and feature extractor; each process needs its own cascade
  if args.cascade_file is None:
    if abs(process_id) == 1:
      logger.info("Using default frontal face detection cascade from bob.ip.facedetect")
    cascade = bob.ip.facedetect.default_cascade()
  else:
    if abs(process_id) == 1:
      logger.info("Loading cascade from file '%s'", args.cascade_file)
    cascade = bob.ip.facedetect.detector.Cascade(bob.io.base.HDF5File(args.cascade_file))
  # initialize sampler
  sampler = bob.ip.facedetect.detector.Sampler(patch_size=cascade.extractor.patch_size, distance=args.distance, scale_factor=args.scale_factor, lowest_scale=args.lowest_scale)

  logger.debug("Detecting faces in %d test images%s", len(dataset), (" in process %d" % process_id) if process_id > 0 else "")

  features = {}
  for image_name in dataset:
    features[image_name] = []
    # load image
    image = bob.io.base.load(os.path.join(args.data_directory, "validation", image_name))
    if image.ndim == 3:
      image = bob.ip.color.rgb_to_gray(image)

    # get bounding boxes and their qualities
    faces = bob.ip.facedetect.detect_all_faces(image, cascade, sampler, args.absolute_threshold, args.number_of_overlaps, args.detection_overlap, args.relative_threshold)
    bounding_boxes, qualities = faces if faces is not None else ([],[])

    # limit bounding boxes
    bounding_boxes = bounding_boxes[:args.maximum_detections]

    # ground truth bbxs are only for displaying purposes
    gt_bbxs = [utils.bounding_box(gt[1]) for gt in dataset[image_name]] if args.display else []
    for i, bbx in enumerate(bounding_boxes):
      cropped = _align(image, bbx, args, gt_bbxs, qualities[i])
      features[image_name].append((_bbx(bbx, qualities[i]), _feature(cropped)))

  logger.debug("Finished processing%s" % (" process %d" % process_id) if process_id > 0 else "")
  return features


def extract_features(data, pool, args, is_training):
  which = "training" if is_training else "test"
  extractor = _extract_training_features if is_training else _extract_test_features
  logger.info("Extracting %s features from %d images", which, len(data))
  # extract training features
  if pool is None:
    features = extractor((data, args))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    splits = utils.split_data_dict_into_parallel(data, args.parallel, (args,))
    features = {}
    for extracted in pool.imap_unordered(extractor, splits):
      for k,v in extracted.items():
        if k not in features:
          features[k] = []
        features[k].extend(v)

  return features


def _project(params):
  data, matrix, mean = params
  projector = bob.learn.linear.Machine(matrix)
  projector.input_subtract = mean
  return {subject: projector(f) if len(f) else [] for subject, f in data.items()}


def project(projector, data, pool, args):
  if pool is None:
    return _project((data, projector.weights, projector.input_subtract))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    data_splits = utils.split_data_dict_into_parallel(data, args.parallel, (projector.weights, projector.input_subtract))
    projected = {}
    for p in pool.imap_unordered(_project, data_splits):
      projected.update(p)
    return projected


def train_pca_lda(training_features, pool, args):
  data = numpy.vstack(training_features.values())
  logger.info("Training PCA with %d features of dimension %d", *data.shape)
  trainer = bob.learn.linear.PCATrainer()
  pca, eigen_values = trainer.train(data)

  # compute relative energy
  cumulated = numpy.cumsum(eigen_values) / numpy.sum(eigen_values)
  # compute number of eigenvalues so that the cumulated energy is larger than the one specified on command line
  pca_subspace = numpy.searchsorted(cumulated, args.eigenvalue_energy, side='right')
  # limit number of pcs
  pca.resize(pca.shape[0], pca_subspace)

  logger.info("Projecting training features into PCA subspace of size %d", pca_subspace)
  projected_pca = project(pca, training_features, pool, args)


  logger.info("Training LDA using %d subjects", len(projected_pca))
  trainer = bob.learn.linear.FisherLDATrainer(use_pinv = True, strip_to_rank = True)
  lda, variances = trainer.train(projected_pca.values())
  logger.info("Final LDA subspace size %s", lda.shape[1])

  # project training features into LDA subspace
  projected_lda = project(lda, projected_pca, pool, args)

  logger.info("Computing combined PCA+LDA projection matrix")
  combined_matrix = numpy.dot(pca.weights, lda.weights)
  projector = bob.learn.linear.Machine(combined_matrix)
  projector.input_subtract = pca.input_subtract

  # write into file
  logger.info("Writing data into %s", args.projector_file)
  h = bob.io.base.HDF5File(args.projector_file, 'w')
  h.create_group("Projector")
  h.create_group("Projected")
  h.cd("Projector")
  projector.save(h)
  h.cd("../Projected")
  for f,v in projected_lda.items():
    h.set(str(f),v)
  return projector, projected_lda

def read_projector(args):
  logger.info("Reading data from %s", args.projector_file)
  h = bob.io.base.HDF5File(args.projector_file, 'r')
  h.cd("Projector")
  projector = bob.learn.linear.Machine(h)
  h.cd("../Projected")
  projected = {int(f):h.get(f) for f in h.keys(relative=True)}
  return projector, projected


def _compare(model, probe):
  return - scipy.spatial.distance.euclidean(model, probe)

def _scores(arguments):
  probes, models, args  = arguments
  scores_for_probes = {}
  for image, probe_features in probes.items():
    scores_for_probes[image] = []
    scores = {}
    for probe in probe_features:
      for subject, model in models.items():
        scores[subject] = _compare(model, probe)
      # keep only maximum scores
      lowest_score = sorted(scores.values())[-args.maximum_scores]
      if -1 in scores:
        # when we predict -1 in our scores, the -1 score should be the lowest to be written
        lowest_score = max(lowest_score, scores[-1])
      scores_for_probes[image].append({subject : score for subject,score in scores.items() if score >= lowest_score})
  return scores_for_probes


def compute_scores(models, probes, pool, args):
  logger.info("Computing scores between %s models and %d probes", len(models), len(probes))
  # extract training features
  if pool is None:
    scores = _scores((probes, models, args))
  else:
    logger.info("Splitting into %d parallel processes", args.parallel)
    probe_splits = utils.split_data_dict_into_parallel(probes, args.parallel, (models, args))
    scores = {}
    for score in pool.imap_unordered(_scores, probe_splits):
      scores.update(score)

  return scores

def limit(data, subjects, use_unknowns):
  tmp = {}
  unknown_counter = 0
  max_unknowns = len(subjects) * 10
  for f,v in data.items():
    if use_unknowns and v[0][0] == -1 and unknown_counter < max_unknowns:
      tmp[f] = v
      unknown_counter += 1
    elif v[0][0] in subjects:
      tmp[f] = v
  return tmp


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)

  training = utils.read_by_file("UCCS", "training")
  validation = utils.read_by_file("UCCS", "validation")

  if args.debug is not None:
    subjects = set(range(1,args.debug+1))
    training = limit(training, subjects, not args.no_train_on_unknowns)
    validation = limit(validation, subjects, True)
    logger.info("Limited to %d training and %d validation images of %d subjects", len(training), len(validation), len(subjects))

  pool = None if args.parallel is None else multiprocessing.Pool(args.parallel)

  if not os.path.exists(args.projector_file) or args.force:
    # extract training features
    training_features = extract_features(training, pool, args, is_training=True)

    # train PCA+LDA on training features
    projector, projected_training_data = train_pca_lda(training_features, pool, args)
  else:
    projector, projected_training_data = read_projector(args)

  if not os.path.exists(args.models_file) or args.force:
    # enroll models from training set images
    models = {subject : numpy.mean(features, axis=0) for subject, features in projected_training_data.items()}
    logger.info("Writing models to file %s", args.models_file)
    h = bob.io.base.HDF5File(args.models_file, 'w')
    for subject, model in models.items():
      h.set(str(subject), model)
  else:
    logger.info("Reading models from file %s", args.models_file)
    h = bob.io.base.HDF5File(args.models_file, 'r')
    models = {int(f): h.get(f) for f in h.keys(relative=True)}


  if not os.path.exists(args.probes_file) or args.force:
    # now, get validation features
    validation_features = extract_features(validation, pool, args, is_training=False)

    # align features to be projected
    bounding_boxes = {image : [feature[0] for feature in val] for image, val in validation_features.items()}
    features = {image : [feature[1] for feature in val] for image, val in validation_features.items()}

    # and project them
    logger.info("Projecting features from %d images", len(features))
    probes = project(projector, features, pool, args)

    logger.info("Writing probes from %d images to file %s", len(probes), args.probes_file)
    h = bob.io.base.HDF5File(args.probes_file, 'w')
    for filename, probe in probes.items():
      h.set(filename.replace("/","$"), probe)
      h.set(filename.replace("/","$")+"-bbxs", bounding_boxes[filename])

  else:
    logger.info("Reading probes from file %s", args.probes_file)
    h = bob.io.base.HDF5File(args.probes_file, 'r')
    probes = {f.replace("$","/"): h.get(f) for f in h.keys(relative=True) if '-bbxs' not in f}
    bounding_boxes = {f.replace("$","/").replace("-bbxs",""): h.get(f) for f in h.keys(relative=True) if '-bbxs' in f}


  # compute similarities between model and probes
  scores = compute_scores(models, probes, pool, args)

  logger.info("Writing scores to score file %s", args.result_file)
  with open(args.result_file, 'w') as f:
    if command_line_arguments is None:
      import sys
      command_line_arguments = sys.argv
    f.write("# Created using command line: %s\n" % " ".join(command_line_arguments))
    f.write("FILE,FACE_X,FACE_Y,FACE_WIDTH,FACE_HEIGHT,FD_SCORE,SUBJECT_1,SCORE_1,SUBJECT_2,SCORE_2,...\n")
    for probe_image in sorted(scores.keys()):
      for p, values in enumerate(scores[probe_image]):
        bbx = bounding_boxes[probe_image][p]
        f.write("%s,%3.2f,%3.2f,%3.2f,%3.2f,%3.2f" % (probe_image, bbx[0], bbx[1], bbx[2], bbx[3], bbx[4]))
        for subject, value in values.items():
          f.write(",%d,%3.2f" % (subject, value))
        f.write("\n")
