import csv
import os

import pkg_resources

def _list_file(dataset, stage):
  return pkg_resources.resource_filename("challenge.uccs", os.path.join("protocol", dataset, "%s.csv" % stage))

def _extract(splits):
  image = splits[1]
  subject = int(splits[2])
  bbx = [float(v) for v in splits[3:7]] # left, top, width, height
  return image, subject, bbx

def read_by_file(dataset, stage):
  """Reads bounding boxes of the training and validation set for the given dataset"""
  data = {}
  with open(_list_file(dataset, stage)) as list_file:
    list_file.readline()
    reader = csv.reader(list_file)
    for splits in reader:
      image, subject, bbx = _extract(splits)
      if image not in data:
        data[image] = []
      data[image].append((subject, bbx))
  return data

def read_by_subject(dataset, stage):
  """Reads bounding boxes of the training and validation set for the given dataset and splits them by ID"""
  data = {}
  with open(_list_file(dataset, stage)) as list_file:
    list_file.readline()
    reader = csv.reader(list_file)
    for splits in reader:
      image, subject, bbx = _extract(splits)
      if subject not in data:
        data[subject] = []
      data[subject].append((image, bbx))
  return data


def _result(splits):
  image = splits[0]
  bbx = [float(v) for v in splits[1:5]] # left, top, width, height
  fd_quality = float(splits[5]) if splits[5] else None
  scores = {int(splits[i]) : float(splits[i+1]) for i in range(6, len(splits), 2)}

  return image, bbx, fd_quality, scores


def read_detections(result_file, header_lines = 2):
  """Reads the csv file for the face detections and sorts them by file."""
  data = {}
  with open(result_file) as data_file:
    for i in range(header_lines):
      data_file.readline()
    reader = csv.reader(data_file)
    for splits in reader:
      image, bbx, q, _ = _result(splits)
      if image not in data:
        data[image] = []
      data[image].append((bbx, q))
  return data


def read_recognitions(result_file, header_lines = 2):
  """Reads the csv file with the face recognition results and sorts them by file."""
  data = {}
  with open(result_file) as data_file:
    # skip header lines
    for i in range(header_lines):
      data_file.readline()

    # read data
    reader = csv.reader(data_file)
    for splits in reader:
      image, bbx, q, scores = _result(splits)
      if image not in data:
        data[image] = []
      data[image].append((bbx, scores))
  return data
