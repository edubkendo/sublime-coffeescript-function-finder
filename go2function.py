import sublime, sublime_plugin
import subprocess
import re
import functools
import os
from filter_dirs import check_dir

#borrowed from Git Plugin by David Lynch
#https://github.com/kemayo/sublime-text-2-git/
def do_when(conditional, callback, *args, **kwargs):
  if conditional():
      return callback(*args, **kwargs)
  sublime.set_timeout(functools.partial(do_when, conditional, callback, *args, **kwargs), 50)

#Gets current word and performs a grep on project folders
#to see if it has a function definition or not
class GoFunctionCommand(sublime_plugin.TextCommand):
  def run(self, text):
    view = self.view

    #get current word
    selection_region = view.sel()[0]
    word_region = view.word(selection_region)
    word = view.substr(word_region).strip()
    word = re.sub('[\(\)\{\}\s]', '', word)

    #get folders to search
    window = sublime.active_window()
    proj_folders = window.folders()

    if word != "":
      print "[Go2Function] Searching for 'function "+word+"'..."

      for dir in proj_folders:
        resp = self.doGrep(word, dir)

        if len(resp) > 0:
          self.openFileToDefinition(resp)
          break

      #if not found show error (ie loop ends without a break)
      else:
        print "[Go2Function] "+word+" not found"
        sublime.error_message("could not find function definition for "+word)

  #actually do the grep
  #well, actually use the native python functions, not grep...
  def doGrep(self, word, directory):
    out = ()

    for r,d,f in os.walk(directory):
      #don't bother to look in git dirs
      if check_dir(r):

        for files in f:
          fn = os.path.join(r, files)
          search = open(fn, "r")
          lines = search.readlines()

          for n, line in enumerate(lines):
            for find in self.getSearchTerms(word):
              if re.search(find, line): #search using regex objects
                out = (fn, n)
                break

          search.close()

          if len(out) > 0:
            break

        if len(out) > 0:
          break

    return out

  def getSearchTerms(self, word):
    wordstr = str(word)
    # compile regexes
    regex1 = re.compile(wordstr + ur'\s[=]\s\(?.*\)?[-=]>')
    regex2 = re.compile(wordstr + ur'[:]\s\(?.*\)?[-=]>')

    return (regex1, regex2)


  #open the file and scroll to the definition
  def openFileToDefinition(self, response):
    file, line = response

    print "[Go2Function] Opening file "+file+" to line "+str(line)
    
    line = line - 1

    window = sublime.active_window()
    new_view = window.open_file(file)

    do_when(
      lambda: not new_view.is_loading(), 
      lambda: new_view.set_viewport_position(new_view.text_to_layout(new_view.text_point(line, 0)))
    )