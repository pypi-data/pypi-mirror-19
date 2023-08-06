#!/mgunther/test_checkouts/bob.bio.caffe/bin/python

import bob.core
logger = bob.core.log.setup("challenge.UCCS")

import numpy
from .. import utils

import bob.measure

from bob.ip.facedetect import BoundingBox

def command_line_options(command_line_arguments):
  import argparse
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--database', '-d', default = 'UCCS', choices = ("UCCS", "MegaFace"), help = "Select the database for which to evaluate")
  parser.add_argument('--recognition-files', '-i', nargs='+', required=True, help = "Get the file with the face recognition results")
  parser.add_argument('--overlap-threshold', '-t', type=float, default=0.5, help = "The overlap threshold for detected faces to be considered to be detected correctly")
  parser.add_argument('--rank', '-r', type=int, default=1, help = "Plot DIR curves for the given rank")
  parser.add_argument('--labels', '-l', nargs='+', help = "Use these labels; if not given, the filenames will be used")
  parser.add_argument('--dir-file', '-w', default = "DIR.pdf", help = "The file, where the DIR curve will be plotted into")
  parser.add_argument('--only-present', '-x', action="store_true", help = "Only caluclate the results for files that have been detected (for debug purposes only)")
  parser.add_argument('--log-x', '-s', action='store_true', help = "If selected, plots will be in semilogx")

  bob.core.log.add_command_line_option(parser)
  args = parser.parse_args(command_line_arguments)
  bob.core.log.set_verbosity_level(logger, args.verbose)

  if args.labels is None:
    args.labels = args.recognition_files

  return args


def split(subject, bbx, scores):
  # splits the detections for this image into positives and negatives
  # takes the scores for the bbx with the highest overlap with the GT
  gt = utils.bounding_box(bbx)
  overlaps = sorted([(utils.overlap(gt, utils.bounding_box(d)), s) for d, s in scores], reverse=True, key=lambda x: x[0])

  if overlaps[0][0] == 0:
    # no overlap -> no positives and no negatives
    return [], []
  best_scores = overlaps[0][1]

  positives = [best_scores[subject]] if subject in best_scores else []
  negatives = [best_scores[s] for s in best_scores if s != subject]

  return negatives, positives

def split_by_probe(ground_truth, scores, args):
  scores_by_probe = {}
  for image in ground_truth:
    if image not in scores and args.only_present:
      continue

    for subject, bbx in ground_truth[image]:
      key = (image, subject)
      if key not in scores_by_probe:
        scores_by_probe[key] = (subject, [], [])
      _, negatives, positives = scores_by_probe[key]
      if image in scores:
        neg, pos = split(subject, bbx, scores[image])
        # we ignore all positives for subject -1
        # TODO: implement better strategy?
        if subject != -1 and pos:
          positives.extend(pos)
        # we always add the negatives, if present
        if neg:
          if subject == -1:
#           if not pos or max(neg) > min(pos):
            # for unknowns, we only use the maximum score
            negatives.append(max(neg))
          else:
            # else, we use all of them
            negatives.extend(neg)

  return scores_by_probe


def detection_identification_rate(scores_by_probe, args):
  # collect all negatives, independent of the actual subject
  negatives = sorted(v for subject,neg,_ in scores_by_probe.values() if subject == -1 for v in neg)

  assert negatives, "At least one negative without positive is required"

  # compute FAR values
  far_values = bob.measure.plot.log_values() if args.log_x else numpy.arange(0.,1.01,0.05)

  # and compute thresholds
  thresholds = [bob.measure.far_threshold(negatives, [], v, True) for v in far_values]

  # now, get the DIR for the given thresholds
  counter = numpy.zeros(len(thresholds))
  correct = numpy.zeros(len(thresholds))
  for subject, neg, pos in scores_by_probe.values():
    if subject == -1:
      # for each negative (which here means: an identity is assigned)...
      for n in neg:
        for i,t in enumerate(thresholds):
          # ... increase the number of misdetections, when the negative is over threshold
          if n > t:
            counter[i] += 1
    else:
      # if the identity is known, we always have to count the probe
      counter += 1

      # compute the rank of the positive, if any
      if pos:
        if len(pos) != 1:
          logger.warning("We have %d positive scores %s for subject %d; taking the first one", len(pos), pos, subject)
        pos = pos[0]
        if not neg:
          neg = []
        is_detected = sum(n >= pos for n in neg) < args.rank
        if is_detected:
          for i,t in enumerate(thresholds):
            # ... increase the number of correct detections, when the positive is over threshold
            if pos >= t:
              correct[i] += 1

  # normalize by the counters
  correct *= 100./counter

  return far_values, correct


def main(command_line_arguments = None):

  # get command line arguments
  args = command_line_options(command_line_arguments)
  # read the detections
  # read the ground truth bounding boxes of the validation set
  logger.info("Reading UCCS ground-truth")
  ground_truth = utils.read_by_file(args.database, "validation")

  results = []
  for recognition_file in args.recognition_files:
    logger.info("Reading scores from %s", recognition_file)
    scores = utils.read_recognitions(recognition_file)

    logger.info("Computing Rates")
    scores_by_probe = split_by_probe(ground_truth, scores, args)
    far, dir_ = detection_identification_rate(scores_by_probe, args)

    results.append((far, dir_))

  logger.info("Plotting DIR curve(s) to file '%s'", args.dir_file)
  # import matplotlib and set some defaults
  from matplotlib import pyplot
  pyplot.ioff()
  import matplotlib
  matplotlib.rc('text', usetex=True)
  matplotlib.rc('font', family='serif')
  matplotlib.rc('lines', linewidth = 4)
  # increase the default font size
  matplotlib.rc('font', size=18)

  # now, plot
  figure = pyplot.figure()
  plotter = pyplot.semilogx if args.log_x else pyplot.plot
  for i, label in enumerate(args.labels):
    # compute some thresholds
    plotter([r*100 for r in results[i][0]], results[i][1], label=label)

  # finalize plot
  if args.log_x:
    pyplot.xticks((.01, .1, 1, 10, 100), ('0.01', '0.1', '1', '10', '100'))
  pyplot.grid(True, color=(0.6,0.6,0.6))
  pyplot.title("Rank %d DIR curve" % args.rank)
  pyplot.legend(loc=1,prop={'size': 16})
  pyplot.xlabel('False Alarm Rate in \%%')
  pyplot.ylim((0, 100))
  pyplot.ylabel('Detection Identification Rate in \%%')
  pyplot.savefig(args.dir_file)
