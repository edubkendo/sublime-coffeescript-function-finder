import os

DIRS_TO_SKIP = [".git", "lib", "node_modules", "public", "vendor"]

def check_dir(dir):
 split = split_path(dir)
 
 if [skip for skip in DIRS_TO_SKIP if skip in split]:
   return False
 
 else:
   return True

def filter_dirs(dirs):
  
  filtered = []
  for path in dirs:
    split = split_path(path)
    
    if [skip for skip in DIRS_TO_SKIP if skip in split]:
      #print "Skipped", path
      pass
    
    else:
      #print "Kept", path
      filtered.append(path)
  
  return filtered

# Modified from http://stackoverflow.com/a/3167684
def split_path(path):

  folders = []
  while True:
    new_path, folder = os.path.split(path)

    if folder != "":
      folders.append(folder)
    
    elif new_path == path:
      break
    
    path = new_path

  folders.reverse()
  return folders

if __name__ == "__main__":
  test_dirs = [
    " ~/projects/projects/towerApps/towerBot/node_modules/pathfinder/node_modules/detective/node_modules/esprima/esprima.js",
    " /home/projects/projects/towerApps/towerBot/node_modules/pathfinder/node_modules/detective/node_modules/esprima/esprima.js",
    " home/projects/projects/towerApps/towerBot/node_modules/pathfinder/node_modules/detective/node_modules/esprima/esprima.js",      
    "/home/bt/.config/sublime-text-2/Packages/folder_test",
    "/home/bt/.config/sublime-text-2/Packages/lib",
    "/home/bt/.config/sublime-text-2/Packages/lib/subdir",
    "lib",
    "node_modules",
    "/node_modules",
    "/node_modules/",
    "node_modules/",
    "dont_skip",
    "safe",
    "alsosafe",
    "not_safe/lib/wow/lib",
    "safe/glib",
    "safe/libg",
    "safe/node_modules2",
    "safe/2node_modules/",
    "safe\\2node/modules\/test",
    "//\\\/\\safe\\//\\2node/modules\/test",
    "\\lib",
    "lib\\",
    "lib\\node_modules",
  ]
