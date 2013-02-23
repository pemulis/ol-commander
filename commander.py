"""OpenLibraryCommander - Command Line Interpreter

This class contains a few methods that make it easier to work on 
OpenLibrary from the command line.

Author: John Shutt <john.d.shutt@gmail.com>
"""

import cmd
import textwrap
from olapi import OpenLibrary
# secrets.py holds the login info, and is excluded from version control
from secrets import login_name, password

ol = OpenLibrary()

# Log in.
logged_in = False
print 'Trying to log in...'
for attempt in range(5):
    try:
        ol.login(login_name, password)
        logged_in = True
        print 'Login successful.'
        break
    except:
        print 'ol.login() error; retrying'
if not logged_in:
    sys.exit('Failed to log in.')

# Define a command interpreter class, to get user input.
class OpenLibraryCommander(cmd.Cmd):
  prompt = '> '

  def do_exit(self, line):
    return True

  def do_get_by_olid(self, olid):
    work = ol.get("/works/" + olid)
    title = work["title"]
    print "Title:"
    print "\"" + title + "\""
    print "Author(s):"
    if work.has_key("authors"):
      authors = work["authors"]
      print authors
    elif work.has_key("author"):
      authors = work["author"]
      print authors
    else:
      print "No author for this work!"
    print "Description:"
    if work.has_key("description"):
      description = work["description"]
      print textwrap.fill(description)
    else:
      print "No description for this work!"

  def do_get_by_title(self, title):
    work = ol.query({"type": "/type/work", "title": title})
    for key in work:
      print key

# Start the command interpreter up.
OpenLibraryCommander().cmdloop()
