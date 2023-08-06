# -*- coding: utf-8 -*-
"""
pyweblib.session - server-side web session handling
(C) 1998-2015 by Michael Ströder <michael@stroeder.com>

This module implements server side session handling stored in
arbitrary string-keyed dictionary objects

This module is distributed under the terms of the
GPL (GNU GENERAL PUBLIC LICENSE) Version 2
(see http://www.gnu.org/copyleft/gpl.html)
"""

# File specific
__revision__ = '$Revision: 1.31 $'.split(' ')[1]
__info__ = '$Id: session.py,v 1.31 2015/01/10 14:15:51 michael Exp $'


import string,re,random,time,pickle

SESSION_ID_CHARS=string.letters+string.digits+'-._'

SESSION_CROSSCHECKVARS = (
  """
  List of environment variables assumed to be constant throughout
  web sessions with the same ID if existent.
  These env vars are cross-checked each time when restoring an
  web session to reduce the risk of session-hijacking.

  Note: REMOTE_ADDR and REMOTE_HOST might not be constant if the client
  access comes through a network of web proxy siblings.
  """
  # REMOTE_ADDR and REMOTE_HOST might not be constant if the client
  # access comes through a network of web proxy siblings.
  'REMOTE_ADDR','REMOTE_HOST',
  'REMOTE_IDENT','REMOTE_USER',
  # If the proxy sets them but can be easily spoofed
  'FORWARDED_FOR','HTTP_X_FORWARDED_FOR',
  # These two are not really secure
  'HTTP_USER_AGENT','HTTP_ACCEPT_CHARSET',
  # SSL session ID if running on SSL server capable
  # of reusing SSL sessions
  'SSL_SESSION_ID',
  # env vars of client certs used for SSL strong authentication
  'SSL_CLIENT_V_START','SSL_CLIENT_V_END',
  'SSL_CLIENT_I_DN','SSL_CLIENT_IDN',
  'SSL_CLIENT_S_DN','SSL_CLIENT_SDN',
  'SSL_CLIENT_M_SERIAL','SSL_CLIENT_CERT_SERIAL',
)

##############################################################################
# Exception classes
##############################################################################

class SessionException(Exception):
  """Raised if """
  def __init__(self, *args):
    self.args = args

class CorruptData(SessionException):
  """Raised if data was corrupt, e.g. UnpicklingError occured"""
  def __str__(self):
    return "Error during retrieving corrupted session data. Session deleted."

class GenerateIDError(SessionException):
  """Raised if generation of unique session ID failed."""
  def __init__(self, maxtry):
    self.maxtry = maxtry
  def __str__(self):
    return "Could not create new session id. Tried %d times." % (self.maxtry)

class SessionExpired(SessionException):
  """Raised if session is expired."""
  def __init__(self, timestamp, session_data):
    self.timestamp = timestamp
    self.session_data = session_data
  def __str__(self):
    return "Session expired %s." % (time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(self.timestamp)))

class SessionHijacked(SessionException):
  """Raised if hijacking of session was detected."""
  def __init__(self, failed_vars):
    self.failed_vars = failed_vars
  def __str__(self):
    return "Crosschecking of the following env vars failed: %s." % (
      self.failed_vars
    )

class MaxSessionCountExceeded(SessionException):
  """Raised if maximum number of sessions is exceeded."""
  def __init__(self, max_session_count):
    self.max_session_count = max_session_count
  def __str__(self):
    return "Maximum number of sessions exceeded. Limit is %d." % (
      self.max_session_count
    )

class BadSessionId(SessionException):
  """Raised if session ID not found in session dictionary."""
  def __init__(self, session_id):
    self.session_id = session_id
  def __str__(self):
    return "No session with key %s." % (self.session_id)

class InvalidSessionId(SessionException):
  """Raised if session ID not found in session dictionary."""
  def __init__(self, session_id):
    self.session_id = session_id
  def __str__(self):
    return "No session with key %s." % (self.session_id)

try:
  import threading
  from threading import Lock as ThreadingLock

except ImportError:
  # Python installation has no thread support
  class ThreadingLock:
    """
    mimikri for threading.Lock()
    """
    def acquire(self):
      pass
    def release(self):
      pass

else:

  class CleanUpThread(threading.Thread):
    """
    Thread class for clean-up thread
    """
    def __init__(self,sessionInstance,interval=60):
      self._sessionInstance = sessionInstance
      self._interval = interval
      self._stop_event = threading.Event()
      self._removed = 0
      threading.Thread.__init__(self,name=self.__class__.__module__+self.__class__.__name__)

    def run(self):
      """Thread function for cleaning up session database"""
      while not self._stop_event.isSet():
        self._removed += self._sessionInstance.cleanUp()
        self._stop_event.wait(self._interval)

    def __repr__(self):
      return '%s: %d sessions removed' % (
        self.getName(),self._removed
      )

    def join(self,timeout=0.0):
      self._stop_event.set()
      threading.Thread.join(self,timeout)


class WebSession:
  """
  The session class which handles storing and retrieving of session data
  in a dictionary-like sessiondict object.
  """

  def __init__(
    self,
    dictobj=None,
    expireDeactivate=0,
    expireRemove=0,
    crossCheckVars=None,
    maxSessionCount=None,
    sessionIDLength=12,
    sessionIDChars=None,
  ):
    """
    dictobj
        has to be a instance of a dictionary-like object
        (e.g. derived from UserDict or shelve)
    expireDeactivate
        amount of time (secs) after which a session
        expires and a SessionExpired exception is
        raised which contains the session data.
    expireRemove
        Amount of time (secs) after which a session
        expires and the session data is silently deleted.
        A InvalidSessionId exception is raised in this case if
        the application trys to access the session ID again.
    crossCheckVars
        List of keys of variables cross-checked for each
        retrieval of session data in retrieveSession(). If None
        SESSION_CROSSCHECKVARS is used.
    maxSessionCount
        Maximum number of valid sessions. This affects
        behaviour of retrieveSession() which raises.
        None means unlimited number of sessions.
    sessionIDLength
        Exact integer length of the session ID generated
    sessionIDChars
        String containing the valid chars for session IDs
        (if this is zero-value the default is SESSION_ID_CHARS)
    """
    if dictobj is None:
      self.sessiondict = {}
    else:
      self.sessiondict = dictobj
    self.expireDeactivate = expireDeactivate
    self.expireRemove = expireRemove
    self._session_lock = ThreadingLock()
    if crossCheckVars is None:
      crossCheckVars = SESSION_CROSSCHECKVARS
    self.crossCheckVars = crossCheckVars
    self.maxSessionCount = maxSessionCount
    self.sessionCounter = 0
    self.session_id_len = sessionIDLength
    self.session_id_chars = sessionIDChars or SESSION_ID_CHARS
    self.session_id_re = re.compile('^[%s]+$' % (re.escape(self.session_id_chars)))
    return # __init__()

  def sync(self):
    """
    Call sync if self.sessiondict has .sync() method
    """
    if hasattr(self.sessiondict,'sync'):
      self.sessiondict.sync()

  def close(self):
    """
    Call close() if self.sessiondict has .close() method
    """
    if hasattr(self.sessiondict,'close'):
      # Close e.g. a database
      self.sessiondict.close()
    else:
      # Make sessiondict inaccessible
      self.sessiondict = None

  def _validateSessionIdFormat(self,session_id):
    """
    Validate the format of session_id. Implementation
    has to match IDs produced in method _generateSessionID()
    """
    if len(session_id)!=self.session_id_len or self.session_id_re.match(session_id) is None:
      raise BadSessionId(session_id)
    return

  def _crosscheckSessionEnv(self,stored_env,current_env):
    """
    Returns a list of keys of items which differ in
    stored_env and current_env.
    """
    return [
      k
      for k in stored_env.keys()
      if stored_env[k]!=current_env.get(k,None)
    ]

  def _generateCrosscheckEnv(self,current_env):
    """
    Generate a dictionary of env vars for session cross-checking
    """
    crosscheckenv = {}
    for k in self.crossCheckVars:
      if current_env.has_key(k):
        crosscheckenv[k] = current_env[k]
    return crosscheckenv

  def _generateSessionID(self,maxtry=1):
    """
    Generate a new random and unique session id string
    """
    def choice_id():
      return ''.join([ random.choice(SESSION_ID_CHARS) for i in range(self.session_id_len) ])
    newid = choice_id()
    tried = 0
    while self.sessiondict.has_key(newid) and (not maxtry or tried<maxtry):
      newid = choice_id()
      tried = tried+1
    if maxtry and tried>=maxtry:
      raise GenerateIDError(maxtry)
    else:
      return newid

  def storeSession(self,session_id,session_data):
    """
    Store session_data under session_id.
    """
    self._session_lock.acquire()
    try:
      # Store session data with timestamp
      self.sessiondict[session_id] = (time.time(),session_data)
      self.sync()
    finally:
      self._session_lock.release()
    return session_id

  def deleteSession(self,session_id):
    """
    Delete session_data referenced by session_id.
    """
    # Delete the session data
    self._session_lock.acquire()
    try:
      if self.sessiondict.has_key(session_id):
        del self.sessiondict[session_id]
      if self.sessiondict.has_key('__session_checkvars__'+session_id):
        del self.sessiondict['__session_checkvars__'+session_id]
      self.sync()
    finally:
      self._session_lock.release()
    return session_id

  def retrieveSession(self,session_id,env={}):
    """
    Retrieve session data
    """
    self._validateSessionIdFormat(session_id)
    session_vars_key = '__session_checkvars__'+session_id
    # Check if session id exists
    if not (
      self.sessiondict.has_key(session_id) and \
      self.sessiondict.has_key(session_vars_key)
    ):
      raise InvalidSessionId(session_id)
    # Read the timestamped session data
    try:
      self._session_lock.acquire()
      try:
        session_checkvars = self.sessiondict[session_vars_key]
        timestamp,session_data = self.sessiondict[session_id]
      finally:
        self._session_lock.release()
    except pickle.UnpicklingError:
      self.deleteSession(session_id)
      raise CorruptData
    current_time = time.time()
    # Check if session data is already expired
    if self.expireDeactivate and \
       (current_time>timestamp+self.expireDeactivate):
      # Remove session entry
      self.deleteSession(session_id)
      # Check if application should be able to allow relogin
      if self.expireRemove and \
         (current_time>timestamp+self.expireRemove):
        raise InvalidSessionId(session_id)
      else:
        raise SessionExpired(timestamp,session_data)
    failed_vars = self._crosscheckSessionEnv(session_checkvars,env)
    if failed_vars:
      # Remove session entry
      raise SessionHijacked(failed_vars)
    # Everything's ok => return the session data
    return session_data

  def newSession(self,env=None):
    """
    Store session data under session id
    """
    env = env or {}
    if self.maxSessionCount and len(self.sessiondict)/2+1>self.maxSessionCount:
      raise MaxSessionCountExceeded(self.maxSessionCount)
    self._session_lock.acquire()
    try:
      # generate completely new session data entry
      session_id=self._generateSessionID(maxtry=3)
      # Store session data with timestamp if session ID
      # was created successfully
      self.sessiondict[session_id] = (
        # Current time
        time.time(),
        # Store a dummy string first
        '_created_',
      )
      self.sessiondict['__session_checkvars__'+session_id] = self._generateCrosscheckEnv(env)
      self.sync()
      self.sessionCounter += 1
    finally:
      self._session_lock.release()
    return session_id

  def cleanUp(self):
    """
    Search for expired session entries and delete them.

    Returns integer counter of deleted sessions as result.
    """
    current_time = time.time()
    result = 0
    for session_id in self.sessiondict.keys():
      if not session_id.startswith('__'):
        try:
          session_timestamp = self.sessiondict[session_id][0]
        except InvalidSessionId:
          # Avoid race condition. The session might have been
          # deleted in the meantime. But make sure everything is deleted.
          self.deleteSession(session_id)
        else:
          # Check expiration time
          if session_timestamp+self.expireRemove<current_time:
            self.deleteSession(session_id)
            result += 1
    return result

# Initialization
random.seed()
