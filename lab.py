import os, sys, stat, time
import argparse
import hashlib
import sqlite3
import Database

# def does_db_exist():
#   if os.path.isfile(watchdog.db):
#     pass 
#   else:

current_files = dict()
existing_files = dict()
new_files = dict()


def check_for_change(db, currWalk):

  for curFile in db:
    if curFile in currWalk:
      new_files[curFile] = currWalk[curFile]

  for curFile in currWalk:
    pass

  if (len(dict1) > len(dict2)):
    for curFile in dict1:
      if curFile not in dict2:
        deleted = dict1[curFile]
        print(deleted.name + " was deleted")
  elif len(dict1) < len(dict2):
    for curFile in dict2:
      if curFile not in dict1:
        added = dict2[curFile]
        print(added.name + " was added")
  else:
    for curFile in dict1:
      oldFile = dict1[curFile]
      newFile = dict2[curFile]
      if (oldFile.timestamp != newFile.timestamp):
        print(newFile.name + " was modified at " + newFile.timestamp)
      if (oldFile.permissions != newFile.permissions):
        print(oldFile.name + "'s permissions were changed")
      if (oldFile.file_hash != newFile.file_hash and oldFile.timestamp == newFile.timestamp):
        print("SECURITY BREACH " + oldFile.name + " was edited without the operating systems knowledge")


"""
select all first time thorugh if empty walk directory
and insert records. make sure to set is new file to false

dump all files and take hash of the string representing the data
store in baseline hash make sure to not include isnewfile colunm


walk dir again when we want to test for changes
insert all records found in dir with isnewfile val being true
dump those files and take hash

run checksum on all data with isnewfile == true and current scan of the directory

if no changes happened do nothing

determine what changes happened 

check for new file

check for permission change

check for new timestamp

check malicious data entry

after changes have been accounted for and output to the screen
set changed files to 
"""




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

  
  for record in records:
    existing_files[record[1]] =aFile(record[1], record[2], record[3], record[5])
  
  


  """
  this just for testing
  """
  for files in current_files:
    curFile = current_files[files]
    
    print("%s last modified:%s permissions:%s filehash:%s" % (curFile.name, curFile.timestamp , str(curFile.permissions) , str(curFile.file_hash)))

    
  
      
      
 
    


      


if __name__ == '__main__':
  main()
