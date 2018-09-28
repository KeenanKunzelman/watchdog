import os, sys, stat, time
import argparse
import hashlib
import sqlite3
import Database


current_files = dict()
existing_files = dict()
master_dict = dict()


def check_for_change(db, currWalk):

  for curFile in db:
    master_dict[curFile] = db[curFile]

  for curFile in currWalk:
    master_dict[curFile] = currWalk[curFile]

  for curFile in master_dict:
    if (curFile in db and curFile not in currWalk):
      deleted_file = db[curFile]
      print(deleted_file.name + " was deleted") 
      #file was deleted
    elif (curFile not in db and curFile in currWalk):
      added_file = currWalk[curFile]
      print(added_file.name + " was added")
      #new file was added
    elif (curFile in db and curFile in currWalk):
      #file was either modified or unchanged
      new_file = currWalk[curFile]
      old_file = db[curFile]
      if new_file.timestamp != old_file.timestamp:
        print(new_file.name + " was modified at " + new_file.timestamp)
      if new_file.permissions != old_file.permissions:
        print(new_file.name + "'s permissions were modified from " + old_file.permissions + " to " + new_file.permissions)
      if new_file.file_hash != old_file.file_hash:
        print("File hashes do not match if time stamps were not changed you may have malicious code in your system")


"""
initialize command line args
"""
parser = argparse.ArgumentParser(description='Monitor files in directory for changes')
parser.add_argument('path', help='Provide a absolute path to directory to be monitored \n ex. root/Destop/hello')
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
def initialize_files(path):
  for dirName, subdirList, fileList in os.walk(path):
    for name in fileList:
      file_hash = hashFile(dirName + '/' + name)
      permissions = os.stat(dirName + '/' + name)[stat.ST_MODE]
      timestamp = time.ctime(os.path.getmtime(dirName + '/' + name))
     
      current_files[dirName + '/' + name] = aFile(dirName + '/' + name, timestamp, permissions, file_hash)
      

 

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

 
  initialize_files(path)
  """
  still have to connect to db here and populate records variable
  """
  conn = Database.create_connection("test2.db")
  Database.initialize_table(conn)
  results = Database.select_columns(conn)
  Database.set_everything_to_false(conn)
  Database.batch_insert(conn, current_files)


  for record in results:
    existing_files[record[1]] =aFile(record[1], record[2], record[3], record[5])
  
  check_for_change(existing_files, current_files)


  """
  this just for testing
  """
  for files in current_files:
    curFile = current_files[files]
    
    print("%s last modified:%s permissions:%s filehash:%s" % (curFile.name, curFile.timestamp , str(curFile.permissions) , str(curFile.file_hash)))

    
  
      
      
 
    


      


if __name__ == '__main__':
  main()
