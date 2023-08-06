from .read_data import *

import bob.ip.facedetect

def bounding_box(bbx):
  return bob.ip.facedetect.BoundingBox((bbx[1], bbx[0]), size = (bbx[3], bbx[2]))

def overlap(gt, det):
  intersection = gt.overlap(det)

  # negative size of intersection: no intersection
  if any(s <= 0 for s in intersection.size_f):
    # no overlap
    return 0.

  # compute union; reduce required overlap to the ground truth
  union = max(gt.area/4, intersection.area) + det.area - intersection.area

  # return intersection over modified union (modified Jaccard similarity)
  return intersection.area / union


def split_data_list_into_parallel(data, processes, arguments):
  return [([d for i, d in enumerate(data) if i % processes == p], ) + arguments for p in range(processes)]

def split_data_dict_into_parallel(data, processes, arguments):
  return [({f:v for i,(f,v) in enumerate(data.items()) if i % processes == p}, ) + arguments for p in range(processes)]
