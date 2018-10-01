import os, sys, stat, time
import argparse
import hashlib
import sqlite3
import Database

"""
create three dictionaries that will be used to check for file changes
"""
current_files = dict()
existing_files = dict()
master_dict = dict()

"""
class that will be used to creat aFile objects as the values for
current_files and new_files
"""
class aFile:
  def __init__ (self, name, timestamp, permissions, file_hash):
    self.name = name
    self.timestamp = timestamp
    self.permissions = permissions
    if file_hash == None:
      self.file_hash = "can not hash empty file"
    else:
      self.file_hash = file_hash


"""
initialize command line args
"""
parser = argparse.ArgumentParser(description='Monitor files in directory for changes')
parser.add_argument('path', help='Provide a absolute path to directory to be monitored \n ex. root/Destop/hello \nor type history to print a historic record of the files in the db')
# parser.add_argument('interval', help='Provide an interval in seconds to poll files')

args = parser.parse_args()
path = args.path


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
        print(new_file.name + " was modified at " + new_file.timestamp )
      if str(new_file.permissions) != str(old_file.permissions):
        print(new_file.name + "'s permissions were modified from " + str(old_file.permissions) + " to " + str(new_file.permissions) + "\n\n")
      if new_file.file_hash != old_file.file_hash:
        print("File hashes do not match if time stamps were not changed you may have malicious code in your system")


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
  """
  Initialize hashing object and a buffer for how many bytes to read in at a time
  to keep memory usage low
  """
  Buffer = 65536
  md5 = hashlib.md5()
  f = open(path,'rb')
  while True:
    data = f.read(Buffer)
    if not data:
      break
    md5.update(data)
    return md5.hexdigest()


def main():
  if args.path == "history":
    """
    *******************************************
    *add function that dumps historic log here*
    *******************************************
    """
    conn = Database.create_connection("test2.db")
    results = Database.get_historic_data(conn)
    print(len(results))
    for i in range(len(results)):
      print(results[i])
    exit()



  initialize_files(path)
  conn = Database.create_connection("test2.db")
  Database.initialize_table(conn)
  results = Database.select_columns(conn)
  Database.set_everything_to_false(conn)
  Database.batch_insert(conn, current_files)




  for record in results:
    existing_files[record[1]] =aFile(record[1], record[2], record[3], record[5])
  check_for_change(existing_files, current_files)

if __name__ == '__main__':
  main()
