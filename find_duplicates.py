import hashlib
import multiprocessing
import os
import time

MEASURE_TIME = True
HASH_FUNC = "sha1" # md5, sha1, sha224, sha256, sha384, sha512
DEFAULT_ROOT_DIR = "."
LINE_SEP = "-" * 80
FILE_CHUNK_SIZE = 1024 * 1024


class File:
  def __init__(self, dirpath, filename):
    self.dirpath = dirpath
    self.filename = filename
    self.filesize = os.path.getsize(self.GetFilePath())

  def CreateHash(self):
    with open(self.GetFilePath(), "rb") as f:
      h = hashlib.new(HASH_FUNC)
      data = f.read(FILE_CHUNK_SIZE)
      while data:
        h.update(data)
        data = f.read(FILE_CHUNK_SIZE)
      self.hash = h.hexdigest()

  def GetDirPath(self):
    return self.dirpath

  def GetFilePath(self):
    return os.path.join(self.dirpath, self.filename)

  def GetFileName(self):
    return self.filename

  def GetFileSize(self):
    return self.filesize

  def GetHash(self):
    return self.hash


def FormatSize(size):
  if size < 1024:
    return "%d B" % size
  if size < 1024 / 1024:
    return "%.2f KB" % (float(size) / 1024)
  if size < 1024 / 1024 / 1024:
    return "%.2f MB" % (float(size) / 1024 / 1024)
  return "%.2f GB" % (float(size) / 1024 / 1024 / 1024)


def GetTotalSize(files):
  return FormatSize(sum(f.GetFileSize() for f in files))


def CollectFiles():
  print "Building list of files...",
  files = []
  zeroSizedFiles = []
  numberOfDirs = -1 # skip root dir
  for dirpath, dirnames, filenames in os.walk(DEFAULT_ROOT_DIR):
    numberOfDirs += 1
    for filename in filenames:
      file = File(dirpath, filename)
      if file.GetFileSize() == 0:
        zeroSizedFiles.append(file)
      else:
        files.append(file)
  print "Done, found %d files in %d directories, %s" % (len(files), numberOfDirs, GetTotalSize(files))
  return files, zeroSizedFiles


def FilterFilesBySize(files):
  print "Filtering unique files (by size)...",
  filesBySize = {}
  for file in files:
    if file.GetFileSize() in filesBySize:
      filesBySize[file.GetFileSize()] += [file]
    else:
      filesBySize[file.GetFileSize()] = [file]
  result = [file for fileList in filesBySize.itervalues() if len(fileList) > 1 for file in fileList]
  print "Done, %d files left, %s" % (len(result), GetTotalSize(result))
  return result


# Helper function for multiprocessing
def GetHashedFile(file):
  try:
    file.CreateHash()
    return file
  except KeyboardInterrupt:
    pass


def HashFiles(files):
  print "Hashing files...",
  pool = multiprocessing.Pool()
  result = pool.map_async(GetHashedFile, files).get(timeout=60*60) # workaround for Ctrl+C
  pool.close()
  pool.join()
  print "Done"
  return result


def FilterFilesByHash(files):
  print "Filtering unique files (by hash)...",
  result = {}
  for file in files:
    if file.GetHash() in result:
      result[file.GetHash()] += [file]
    else:
      result[file.GetHash()] = [file]
  result = {hash: result[hash] for hash in result if len(result[hash]) > 1}

  totalSize = GetTotalSize(file for fileList in result.itervalues() for file in fileList)

  print "Done, %d files left, %s" % (sum(len(result[hash]) for hash in result), totalSize)
  return result


def PrintDuplicates(filesByHash):
  filesByDir = {
    #dirpath: [
    #  filename: [duplicateFilePath, ...],
    #  ...
    #],
    #...
  }
  for fileList in filesByHash.itervalues():
    for file in fileList:
      if file.GetDirPath() not in filesByDir:
        filesByDir[file.GetDirPath()] = {}
      filesByDir[file.GetDirPath()][file.GetFileName()] = [f for f in fileList if f != file]

  print LINE_SEP
  for dirpath in filesByDir:
    print dirpath
    for filename in filesByDir[dirpath]:
      print "    %s:" % filename
      for dupFile in filesByDir[dirpath][filename]:
        print "        %s" % dupFile.GetFilePath()
    print LINE_SEP


def PrintZeroSizedFiles(files):
  if len(files):
    print "Zero-sized files:"
    for file in files:
      print "    %s:" % file.GetFilePath()
    print LINE_SEP


def main():
  files, zeroSizedFiles = CollectFiles()
  files = FilterFilesBySize(files)
  files = HashFiles(files)
  filesByHash = FilterFilesByHash(files)
  PrintDuplicates(filesByHash)
  PrintZeroSizedFiles(zeroSizedFiles)


if __name__ == "__main__":
  if MEASURE_TIME:
    startTime = time.time()
    main()
    endTime = time.time()
    print "Finished in %.2f seconds" % (endTime - startTime)
  else:
    main()
