# -*- coding: utf-8 -*-
"""
pyweblib.helper - Misc. stuff useful in CGI-BINs
(C) 1998-2015 by Michael Ströder <michael@stroeder.com>

This module is distributed under the terms of the
GPL (GNU GENERAL PUBLIC LICENSE) Version 2
(see http://www.gnu.org/copyleft/gpl.html)
"""

# File specific
__revision__ = '$Revision: 1.17 $'.split(' ')[1]
__info__ = '$Id: helper.py,v 1.17 2015/01/10 14:15:51 michael Exp $'


import os,re,UserDict

known_browsers = {
  'MSIE':'Microsoft Internet Explorer',
  'Mozilla':'Netscape Navigator',
  'Lynx':'Lynx',
  'Opera':'Opera',
  'StarOffice':'StarOffice',
  'NCSA_Mosaic':'NCSA Mosaic',
  'NetPositive':'Net Positive',
  'Mozilla':'Firefox',
  'Mozilla':'Seamonkey',
}
known_browsers_rev = {}
for b in known_browsers.keys():
  known_browsers_rev[known_browsers[b]]=b

compatible_browsers = known_browsers.keys()
compatible_browsers.remove('Mozilla')

compatible_browsers_re = re.compile('(%s)[/ ]+([0-9.]*)' % '|'.join(compatible_browsers))
mozilla_re             = re.compile('(Mozilla)[/ ]+([0-9.]*)')


def BrowserType(http_user_agent):
  """
  Parse the HTTP_USER_AGENT environment variable and return the
  tuple (Browser,Version).

  Not sure if this succeeds in every situation since most
  browsers have very obscure HTTP_USER_AGENT entries for compability reasons.
  The following browsers are known by name:
  Netscape  Netscape Navigator, Netscape Communicator)
  MSIE    MS Internet Explorer
  Opera   Opera browser from http://www.operasoftware.com/
  StarOffice  built-in browser of Star Office
  Lynx    the text-based browser Lynx
  NetPositive Net Positive (BeOS)
  """

  if not http_user_agent:
    return ('','')
  else:
    browserrm = compatible_browsers_re.search(http_user_agent)
    if browserrm:
      return browserrm.groups()
    else:
      browserrm = mozilla_re.search(http_user_agent)
      if browserrm:
        return browserrm.groups()
      else:
        return ('','')


def guessClientAddr(env=None):
  """
  Guesses the host name or IP address of the HTTP client by looking
  at various HTTP headers mapped to CGI-BIN environment.

  env
        dictionary containing environment vars (default os.env)
  """
  env = env or os.environ
  return env.get('FORWARDED_FOR',
         env.get('HTTP_X_FORWARDED_FOR',
         env.get('REMOTE_HOST',
         env.get('REMOTE_ADDR',None))))


class AcceptHeaderDict(UserDict.UserDict):
  """
  This dictionary class is used to parse
  Accept-header lines with quality weights.

  It's a base class for all Accept-* headers described
  in sections 14.1 to 14.5 of RFC2616.
  """

  def __init__(self,envKey,env=None,defaultValue=None):
    """
    Parse the Accept-* header line.

    httpHeader
        string with value of Accept-* header line
    """
    env = env or os.environ
    UserDict.UserDict.__init__(self)
    self.defaultValue = defaultValue
    self.preferred_value = []
    try:
      http_accept_value = [
        s
        for s in env[envKey].strip().split(',')
        if len(s)
      ]
    except KeyError:
      self.data = {'*':1.0}
    else:
      if not http_accept_value:
        self.data = {'*':1.0}
      else:
        self.data = {}
        for i in http_accept_value:
          try:
            c,w=i.split(';')
          except ValueError:
            c,w = i,''
          # Normalize charset name
          c=c.strip().lower()
          try:
            q,qvalue_str=w.split('=',1)
            qvalue = float(qvalue_str)
          except ValueError:
            qvalue = 1.0
          # Add to capability dictionary
          if c:
            self.data[c] = qvalue
    return # AcceptHeaderDict.__init__()

  def __getitem__(self,value):
    """
    value
        String representing the value for which to return
        the floating point capability weight.
    """
    return self.data.get(
      value.lower(),
      self.data.get('*',0)
    )

  def items(self):
    """
    Return the accepted values as tuples (value,weigth)
    in descending order of capability weight
    """
    l = self.data.items()
    l.sort(lambda x,y:cmp(y[1],x[1]))
    return l

  def keys(self):
    """
    Return the accepted values in descending order of capability weight
    """
    l = self.items()
    return [ k for k,v in l ]


class AcceptCharsetDict(AcceptHeaderDict):
  """
  Special class for Accept-Charset header
  """

  def __init__(self,envKey='HTTP_ACCEPT_CHARSET',env=None,defaultValue='utf-8'):
    AcceptHeaderDict.__init__(self,envKey,env,defaultValue)
    # Special treating of ISO-8859-1 charset to be compliant to RFC2616
    self.data['iso-8859-1'] = self.data.get('iso-8859-1',self.data.get('*',1.0))
    return # AcceptCharsetDict.__init__()

  def preferred(self):
    """
    Return the value name with highest capability weigth
    """
    l = self.items()
    while l and l[0][0]!='*':
      try:
        u''.encode(l[0][0])
      except LookupError:
        l.pop(0)
      else:
        break
    if l:
      if self.defaultValue and l[0][0]=='*':
        return self.defaultValue
      else:
        return l[0][0]
    else:
      return self.defaultValue

