# -*- coding: utf-8 -*-
"""
httphelper.py - basic HTTP-related functions
(C) 1998-2015 by Michael Ströder <michael@stroeder.com>

This module is distributed under the terms of the
GPL (GNU GENERAL PUBLIC LICENSE) Version 2
(see http://www.gnu.org/copyleft/gpl.html)
"""

# File specific
__revision__ = '$Revision: 1.15 $'.split(' ')[1]
__info__ = '$Id: httphelper.py,v 1.15 2015/01/10 14:15:51 michael Exp $'


import sys,time

HTTP_LINESEP = '\r\n'

def DateTimeRFC1123(secs=0):
  """
  Return seconds as RFC1123 date/time format preferred
  for HTTP 1.1 (see RFC2616)
  """
  return time.strftime(
    '%a, %d %b %Y %H:%M:%S GMT',
    time.gmtime(secs)
  )

# Write HTTP-Header
def SendHeader(
  outf=sys.stdout,
  contenttype='text/html',
  charset='ISO-8859-1',
  contentlength=None,
  expires_offset=0,
  current_datetime=None,
  additional_header=None
):
  """
  Generate HTTP header

  outf
      File object used for sending to client.
  contenttype
      MIME type of object in HTTP body. Default is 'text/html'.
  charset
      Character set used. Default is 'ISO-8859-1'.
  contentlength
      Content-Length if known and gzip-encoding is not used.
      Default is None indicating unknown length.
  expires_offset=0,
      Expiry time from current time in seconds. Default is 0.
  current_datetime
      Last modification time in seconds.
      If zero (default) 'Last-modified' header will be omitted.
  additional_header
      Dictionary containing arbitrary additional HTTP header fields
      as key/value-pairs.
  """
  additional_header = additional_header or {}
  gzip = hasattr(outf,'fileobj')
  # Get current time as GMT (seconds since epoch)
  gmt = time.time()
  # Determine times for HTTP header
  if current_datetime is None:
    current_datetime = DateTimeRFC1123(gmt)
  expires = DateTimeRFC1123(gmt+expires_offset)
  # Build list of header lines
  header_lines = []
  # Write header
  if not (contenttype is None):
    if contenttype.lower().startswith('text/'):
      header_lines.append('Content-Type: %s;charset=%s' % (contenttype,charset))
    else:
      header_lines.append('Content-Type: %s' % (contenttype))
  if not (contentlength is None):
    header_lines.append('Content-Length: %d' % (contentlength))
  if gzip:
    header_lines.append('Content-Encoding: gzip')
    header_lines.append('Vary: Accept-Encoding')
  header_lines.append('Date: %s' % (current_datetime))
  header_lines.append('Last-Modified: %s' % (current_datetime))
  header_lines.append('Expires: %s' % (expires))
  for h,v in additional_header.items():
    header_lines.append('%s: %s' % (h,v))
  # Write empty end-of-header line
  header_lines.extend(['',''])
  if gzip:
    outf.fileobj.write(HTTP_LINESEP.join(header_lines))
    outf.fileobj.flush()
  else:
    outf.write(HTTP_LINESEP.join(header_lines))
  return


def SimpleMsg(outf,msg):
  """
  Output HTML text.
  """
  SendHeader(outf)
  outf.write("""
<html>
  <head>
    <title>Note</title>
  </head>
  <body>
    %s
  </body>
</html>
    """ % (msg)
  )

def URLRedirect(outf,url,refreshtime=0,msg='Redirecting...',additional_header=None):
  """
  Output HTML text with redirecting <head> section.
  """
  SendHeader(outf)
  outf.write("""
<html>
  <head>
    <meta http-equiv="refresh" content="%d; url=%s">
  </head>
  <body>
    <a href="%s">%s</a>
  </body>
</html>
    """ % (refreshtime,url,url,msg)
  )
