#!/usr/bin/python

import sys, os, string, types, dbm, gdbm, shelve, cgi

# Where to find own modules
sys.path.append('/home/michael/Proj/python/pyweblib')

import pyweblib.session

sessiondict = shelve.open('/tmp/test-pyweblib.session','c')

webSession = pyweblib.session.WebSession(
  sessiondict,expireDeactivate=30,expireRemove=60
)

form = cgi.FieldStorage()

if form.has_key('sessionid'):
  sessionid = form['sessionid'].value
  try:
    oldtext = webSession.retrieveSession(sessionid)
  except pyweblib.session.SessionException,e:
    sessionid = webSession.newSession()
    oldtext = '*** %s' % (str(e))
else:
  sessionid = webSession.newSession()
  oldtext = '*** Created new session.'

if form.has_key('text'):
  newtext = form['text'].value
  webSession.storeSession(sessionid,newtext)
else:
  newtext = ''

# Anzeige der eingegebenen Daten
print """Content-type: text/html
Pragma: no-cache

<html>

  <title>
  </title>

  <body>

    <p>
      sessionid = %(sessionid)s
    </p>
    <p>
      Old text restored from session cache:
    </p>
    <pre>
      %(oldtext)s
    </pre>
    <p>
      New text stored currently stored into session cache:
    </p>
    <pre>
      %(newtext)s
    </pre>
    <form action="test-session.py" method=get>
      <input type="hidden" name="sessionid" value="%(sessionid)s">
      <textarea name="text" cols=60 rows=10></textarea>
      <input type="submit" value="send">
    </form>

  </body>

</html>
""" % vars()


sessiondict.close()

sys.exit(0)
