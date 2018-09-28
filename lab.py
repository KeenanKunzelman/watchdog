import os, sys, stat, time
import argparse
import hashlib

"""
initialize command line args
"""
parser = argparse.ArgumentParser(description='Monitor files in directory for changes')
parser.add_argument('path', help='Provide a absolute path to directory to be monitored')
parser.add_argument('interval', help='Provide an interval in seconds to poll files')
args = parser.parse_args()
path = args.path

"""
Initialize hashing object and a buffer for how many bytes to read in at a time
to keep memory usage low
"""
Buffer = 65536
md5 = hashlib.md5()

"""
create two dictionaries that will be used to check for file changes
"""
current_files = dict()
new_files = dict()

"""
class that will be used to creat aFile objects as the values for
current_files and new_files
"""
class aFile:
  def __init__ (self, name, timestamp, permissions, file_hash):
    """
    make name abs path
    """
    self.name = name
    self.timestamp = timestamp
    self.permissions = permissions
    if file_hash == None:
      self.file_hash = "can not hash empty file"
    else:
      self.file_hash = file_hash

"""
Compare the hashes of two files to ensure malicious edits
are not occuring
"""
def checksum(hash1, hash2):
  if hash1 == hash2:
    return True
  else:
    return False

"""
initializes the dictionaries 
"""
def initialize_files(path, init):
  for root, dirs, files in os.walk(path, topdown=False):
      for name in files:
        file_hash = hashFile(path + '/' + name)
        permissions = os.stat(path + '/' + name)[stat.ST_MODE]
        timestamp = time.ctime(os.path.getmtime(path + '/' + name))
        if init == True:
          current_files[name] = aFile(name, timestamp, permissions, file_hash)
        else:
          new_files[name] = aFile(name, timestamp, permissions, file_hash)
        

        


def check_changes():
  pass

"""
creates md5 file hash
"""
def hashFile(path):
  f = open(path,'rb')
  while True:
    data = f.read(Buffer)
    if not data:
      break
    md5.update(data)
    return md5.hexdigest()


def main():

  
  initialize_files(path, True)

  for files in current_files:
    curFile = current_files[files]

    print("%s last modified:%s permissions:%s filehash:%s" % (curFile.name, curFile.timestamp , str(curFile.permissions) , str(curFile.file_hash)))

  
      
      
 
    

  while True:
    time.sleep(int(args.interval))
    for root, dirs, files in os.walk(path, topdown=False):
      for name in files:
        print(root + "/" + name)
      


if __name__ == '__main__':
  main()
