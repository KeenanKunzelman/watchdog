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
  
  changes = False
  for curFile in db:
    master_dict[curFile] = db[curFile]
  for curFile in currWalk:
    master_dict[curFile] = currWalk[curFile]

  for curFile in master_dict:
    if (curFile in db and curFile not in currWalk):
      deleted_file = db[curFile]
      print(deleted_file.name + " was deleted")
      changes = True
      #file was deleted
    elif (curFile not in db and curFile in currWalk):
      added_file = currWalk[curFile]
      print(added_file.name + " was added")
      changes = True
      #new file was added
    elif (curFile in db and curFile in currWalk):
     
      #file was either modified or unchanged
      new_file = currWalk[curFile]
      old_file = db[curFile]
      if new_file.timestamp != old_file.timestamp:
        print(new_file.name + " was modified at " + new_file.timestamp)
        changes = True
      if str(new_file.permissions) != str(old_file.permissions):
        print(new_file.name + "'s permissions were modified from " + str(old_file.permissions) + " to " + str(new_file.permissions))
        changes = True
      if new_file.file_hash != old_file.file_hash:
        print("File hashes do not match if time stamps were not changed you may have malicious code in your system")
        changes = True
  if changes == False:
    print("No files have changed")
    
"""
initializes the dictionaries 
"""
def initialize_files(path):
 

  for dirName, subdirList, fileList in os.walk(path):
    for name in fileList:
      file_hash = hash_file(dirName + '/' + name)
      permissions = os.stat(dirName + '/' + name)[stat.ST_MODE]
      timestamp = time.ctime(os.path.getmtime(dirName + '/' + name))

      current_files[dirName + '/' + name] = aFile(dirName + '/' + name, timestamp, permissions, file_hash)


"""
creates md5 file hash
"""
def hash_file(path):
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
    print("Number of files in db " + str(len(results)))
    print("Unique timestamp \t Name of File \t\t\t Last Modified \t Permissions \t New File? \t FIle Hash")
    for i in range(len(results)):
      print(results[i])
    exit()

  cmd = input("Please enter either s, m, h, d, w\n\ts = Poll every 5 seconds\n\tm = Poll every minute\n\th = Poll every hour\n\td = Poll every day\n\tw = Poll every week\n")
  # while True:
  while True:
  
    initialize_files(path)
    conn = Database.create_connection("test2.db")
    Database.initialize_table(conn)
    results = Database.select_columns(conn)
    Database.set_everything_to_false(conn)
    Database.batch_insert(conn, current_files)
    
    if len(current_files) == 0:
      Database.set_everything_to_false(conn)
      conn.commit()
    conn.close()

    for record in results:
      existing_files[record[1]] = aFile(record[1], record[2], record[3], record[5])
    check_for_change(existing_files, current_files)
    
    if cmd == "m":
      time.sleep(60)
    elif cmd == "s":
      time.sleep(5)
    elif cmd == "h":
      time.sleep(3600)
    elif cmd == "d":
      time.sleep(86400)
    elif cmd == "w":
      time.sleep(604800)
    else:
      os.system('cls' if os.name == 'nt' else 'clear')
      cmd = input("Please enter either s, m, h, d, w\n\ts = Poll every 5 seconds\n\tm = Poll every minute\n\th = Poll every hour\n\td = Poll every day\n\tw = Poll every week\n")
    current_files.clear()
    master_dict.clear()
    existing_files.clear()
    
if __name__ == '__main__':
  main()