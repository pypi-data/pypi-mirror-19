# -*- coding: utf-8 -*-
"""
pyweblib.sslenv.py - retrieve SSL data from environment vars
(C) 1998-2015 by Michael Ströder <michael@stroeder.com>

This module is distributed under the terms of the
GPL (GNU GENERAL PUBLIC LICENSE) Version 2
(see http://www.gnu.org/copyleft/gpl.html)
"""

# File specific
__revision__ = '$Revision: 1.13 $'.split(' ')[1]
__info__ = '$Id: sslenv.py,v 1.13 2015/01/10 14:15:51 michael Exp $'


from forms import escapeHTML

import sys,os,re,string

def GetAllSSLEnviron(env=None):
  """
  Get all SSL-related environment vars and return mod_ssl
  compatible dictionary.

  mod_ssl compatible names are preferred. ApacheSSL names
  are used as fallback.
  """
  env = env or os.environ
  if env.get('HTTPS','off')!='on':
    return {}
  SSLEnv = {}
  SSLEnv['SSL_CIPHER_ALGKEYSIZE'] = \
    env.get('SSL_CIPHER_ALGKEYSIZE',
    env.get('HTTPS_KEYSIZE',
    env.get('SSL_KEYSIZE',
    env.get('SSL_SERVER_KEY_SIZE',
    None))))
  SSLEnv['SSL_CIPHER_EXPORT'] = \
    env.get('SSL_CIPHER_EXPORT',
    env.get('HTTPS_EXPORT',
    env.get('SSL_EXPORT',
    None)))
  SSLEnv['SSL_CIPHER'] = \
    env.get('SSL_CIPHER',
    env.get('HTTPS_CIPHER',
    None))
  SSLEnv['SSL_CIPHER_USEKEYSIZE'] = \
    env.get('SSL_CIPHER_USEKEYSIZE',
    env.get('HTTPS_SECRETKEYSIZE',
    env.get('SSL_SECKEYSIZE',
    None)))
  SSLEnv['SSL_CLIENT_A_SIG'] = \
    env.get('SSL_CLIENT_A_SIG',
    env.get('SSL_CLIENT_SIGNATURE_ALGORITHM',
    None))
  SSLEnv['SSL_CLIENT_CERT'] = \
    env.get('SSL_CLIENT_CERT',
    env.get('SSL_CLIENT_CERTIFICATE',
    None))
  SSLEnv['SSL_CLIENT_I_DN'] = \
    env.get('SSL_CLIENT_I_DN',
    env.get('SSL_CLIENT_IDN',
    None))
  SSLEnv['SSL_CLIENT_I_DN_CN'] = \
    env.get('SSL_CLIENT_I_DN_CN',
    env.get('SSL_CLIENT_ICN',
    None))
  SSLEnv['SSL_CLIENT_I_DN_C'] = \
    env.get('SSL_CLIENT_I_DN_C',
    env.get('SSL_CLIENT_IC',
    None))
  SSLEnv['SSL_CLIENT_I_DN_Email'] = \
    env.get('SSL_CLIENT_I_DN_Email',
    env.get('SSL_CLIENT_IEMAIL',
    None))
  SSLEnv['SSL_CLIENT_I_DN_L'] = \
    env.get('SSL_CLIENT_I_DN_L',
    env.get('SSL_CLIENT_IL',
    None))
  SSLEnv['SSL_CLIENT_I_DN_O'] = \
    env.get('SSL_CLIENT_I_DN_O',
    env.get('SSL_CLIENT_IO',
    None))
  SSLEnv['SSL_CLIENT_I_DN_OU'] = \
    env.get('SSL_CLIENT_I_DN_OU',
    env.get('SSL_CLIENT_IOU',
    None))
  SSLEnv['SSL_CLIENT_I_DN_SP'] = \
    env.get('SSL_CLIENT_I_DN_SP',
    env.get('SSL_CLIENT_ISP',
    None))
  SSLEnv['SSL_CLIENT_M_SERIAL'] = \
    env.get('SSL_CLIENT_M_SERIAL',
    env.get('SSL_CLIENT_CERT_SERIAL',
    None))
  SSLEnv['SSL_CLIENT_S_DN'] = \
    env.get('SSL_CLIENT_S_DN',
    env.get('SSL_CLIENT_DN',
    None))
  SSLEnv['SSL_CLIENT_S_DN_CN'] = \
    env.get('SSL_CLIENT_S_DN_CN',
    env.get('SSL_CLIENT_CN',
    None))
  SSLEnv['SSL_CLIENT_S_DN_C'] = \
    env.get('SSL_CLIENT_S_DN_C',
    env.get('SSL_CLIENT_C',
    None))
  SSLEnv['SSL_CLIENT_S_DN_Email'] = \
    env.get('SSL_CLIENT_S_DN_Email',
    env.get('SSL_CLIENT_EMAIL',
    None))
  SSLEnv['SSL_CLIENT_S_DN_L'] = \
    env.get('SSL_CLIENT_S_DN_L',
    env.get('SSL_CLIENT_L',
    None))
  SSLEnv['SSL_CLIENT_S_DN_O'] = \
    env.get('SSL_CLIENT_S_DN_O',
    env.get('SSL_CLIENT_O',
    None))
  SSLEnv['SSL_CLIENT_S_DN_OU'] = \
    env.get('SSL_CLIENT_S_DN_OU',
    env.get('SSL_CLIENT_OU',
    None))
  SSLEnv['SSL_CLIENT_S_DN_SP'] = \
    env.get('SSL_CLIENT_S_DN_SP',
    env.get('SSL_CLIENT_SP',
    None))
  SSLEnv['SSL_CLIENT_V_END'] = \
    env.get('SSL_CLIENT_V_END',
    env.get('SSL_CLIENT_CERT_END',
    None))
  SSLEnv['SSL_CLIENT_V_START'] = \
    env.get('SSL_CLIENT_V_START',
    env.get('SSL_CLIENT_CERT_START',
    None))
  SSLEnv['SSL_PROTOCOL'] = \
    env.get('SSL_PROTOCOL',
    env.get('SSL_PROTOCOL_VERSION',
    None))
  SSLEnv['SSL_SERVER_A_SIG'] = \
    env.get('SSL_SERVER_A_SIG',
    env.get('SSL_SERVER_SIGNATURE_ALGORITHM',
    None))
  SSLEnv['SSL_SERVER_CERT'] = \
    env.get('SSL_SERVER_CERT',
    env.get('SSL_SERVER_CERTIFICATE',
    None))
  SSLEnv['SSL_SERVER_I_DN_CN'] = \
    env.get('SSL_SERVER_I_DN_CN',
    env.get('SSL_SERVER_ICN',
    None))
  SSLEnv['SSL_SERVER_I_DN_C'] = \
    env.get('SSL_SERVER_I_DN_C',
    env.get('SSL_SERVER_IC',
    None))
  SSLEnv['SSL_SERVER_I_DN_Email'] = \
    env.get('SSL_SERVER_I_DN_Email',
    env.get('SSL_SERVER_IEMAIL',
    None))
  SSLEnv['SSL_SERVER_I_DN_L'] = \
    env.get('SSL_SERVER_I_DN_L',
    env.get('SSL_SERVER_IL',
    None))
  SSLEnv['SSL_SERVER_I_DN_O'] = \
    env.get('SSL_SERVER_I_DN_O',
    env.get('SSL_SERVER_IO',
    None))
  SSLEnv['SSL_SERVER_I_DN'] = \
    env.get('SSL_SERVER_I_DN',
    env.get('SSL_SERVER_IDN',
    None))
  SSLEnv['SSL_SERVER_I_DN_OU'] = \
    env.get('SSL_SERVER_I_DN_OU',
    env.get('SSL_SERVER_IOU',
    None))
  SSLEnv['SSL_SERVER_I_DN_SP'] = \
    env.get('SSL_SERVER_I_DN_SP',
    env.get('SSL_SERVER_ISP',
    None))
  SSLEnv['SSL_SERVER_M_SERIAL'] = \
    env.get('SSL_SERVER_M_SERIAL',
    env.get('SSL_SERVER_CERT_SERIAL',
    None))
  SSLEnv['SSL_SERVER_S_DN'] = \
    env.get('SSL_SERVER_S_DN',
    env.get('SSL_SERVER_DN',
    None))
  SSLEnv['SSL_SERVER_S_DN_CN'] = \
    env.get('SSL_SERVER_S_DN_CN',
    env.get('SSL_SERVER_CN',
    None))
  SSLEnv['SSL_SERVER_S_DN_C'] = \
    env.get('SSL_SERVER_S_DN_C',
    env.get('SSL_SERVER_C',
    None))
  SSLEnv['SSL_SERVER_S_DN_Email'] = \
    env.get('SSL_SERVER_S_DN_Email',
    env.get('SSL_SERVER_EMAIL',
    None))
  SSLEnv['SSL_SERVER_S_DN_L'] = \
    env.get('SSL_SERVER_S_DN_L',
    env.get('SSL_SERVER_L',
    None))
  SSLEnv['SSL_SERVER_S_DN_O'] = \
    env.get('SSL_SERVER_S_DN_O',
    env.get('SSL_SERVER_O',
    None))
  SSLEnv['SSL_SERVER_S_DN_OU'] = \
    env.get('SSL_SERVER_S_DN_OU',
    env.get('SSL_SERVER_OU',
    None))
  SSLEnv['SSL_SERVER_S_DN_SP'] = \
    env.get('SSL_SERVER_S_DN_SP',
    env.get('SSL_SERVER_SP',
    None))
  SSLEnv['SSL_SERVER_V_END'] = \
    env.get('SSL_SERVER_V_END',
    env.get('SSL_SERVER_CERT_END',
    None))
  SSLEnv['SSL_SERVER_V_START'] = \
    env.get('SSL_SERVER_V_START',
    env.get('SSL_SERVER_CERT_START',
    None))
  SSLEnv['SSL_VERSION_LIBRARY'] = \
    env.get('SSL_VERSION_LIBRARY',
    env.get('SSL_SSLEAY_VERSION',
    None))
  return SSLEnv


def SecLevel(env,acceptedciphers,valid_dn_regex='',valid_idn_regex=''):
  """
  Determine Security Level of SSL session.

  Returns:
  0  no SSL at all
  1  SSL-connection and cipher used is in acceptedciphers
  2  like 1 but client also has sent client certificate
     matching valid_dn_regex and valid_idn_regex.
  """
  https_env = GetAllSSLEnviron(env)
  if https_env and https_env.get('SSL_CIPHER','') in acceptedciphers:
    ssl_client_s_dn = https_env.get('SSL_CLIENT_S_DN','')
    if ssl_client_s_dn:
      ssl_client_i_dn = https_env.get('SSL_CLIENT_I_DN','')
      dn_rm = re.compile(valid_dn_regex).match(ssl_client_s_dn)
      idn_rm = re.compile(valid_idn_regex).match(ssl_client_i_dn)
      if (dn_rm) and (idn_rm):
        return 2
      else:
        return 1
    else:
      return 1
  else:
    return 0


def PrintSecInfo(env,acceptedciphers,valid_dn_regex='',valid_idn_regex='',f=sys.stdout):
  """
  Print the SSL data in HTML format
  """
  seclevel = SecLevel(env,acceptedciphers,valid_dn_regex,valid_idn_regex)
  https_env = GetAllSSLEnviron(env)
  f.write("""<h3>Security level</h3>
<p>Current security level is: <strong>%d</strong></p>
<table cellspacing="5%%" summary="Possible SSL/TLS security levels">
<tr>
  <td align=center width=10%%>0</td>
  <td>no encryption at all</td>
</tr>
<tr>
  <td align=center>1</td>
  <td>Session is encrypted with SSL and cipher is accepted</td>
</tr>
<tr>
  <td align=center>2</td>
  <td>
    Client presented valid certificate,
    the DN of the certified object matches &quot;<code>%s</code>&quot;
    and the DN of the certifier matches &quot;<code>%s</code>&quot;
  </td>
</tr>
</table>
   """ % (seclevel,valid_dn_regex,valid_idn_regex))

  if seclevel>=1:
    SSL_PROTOCOL = https_env.get('SSL_PROTOCOL')
    SSL_CIPHER_ALGKEYSIZE = https_env.get('SSL_CIPHER_ALGKEYSIZE')
    SSL_CIPHER = https_env.get('SSL_CIPHER')
    SSL_CIPHER_USEKEYSIZE = https_env.get('SSL_CIPHER_USEKEYSIZE')
    SSL_SERVER_S_DN = https_env.get('SSL_SERVER_S_DN')
    SSL_SERVER_I_DN = https_env.get('SSL_SERVER_I_DN')

    f.write("""<p><strong>%s</strong> connection with cipher <strong>%s</strong>,
key size <strong>%s Bit</strong>, actually used key size <strong>%s Bit</strong>.</p>
<h3>Server certificate</h3>
<dl>
  <dt>Subject-DN:</dt>
  <dd>%s</dd>
  <dt>Issuer-DN:</dt>
  <dd>%s</dd>
</dl>
""" % (
  SSL_PROTOCOL,
  SSL_CIPHER,
  SSL_CIPHER_ALGKEYSIZE,
  SSL_CIPHER_USEKEYSIZE,
  escapeHTML(SSL_SERVER_S_DN),
  escapeHTML(SSL_SERVER_I_DN),
))

  if seclevel>=2:

    SSL_CLIENT_I_DN = https_env.get('SSL_CLIENT_I_DN',https_env.get('SSL_CLIENT_IDN','')
    )
    SSL_CLIENT_S_DN = https_env.get('SSL_CLIENT_S_DN',https_env.get('SSL_CLIENT_DN',''))

    f.write("""<h3>Your client certificate</h3>
<dl>
  <dt>Subject-DN:</dt>
  <dd>%s</dd>
  <dt>Issuer-DN:</dt>
  <dd>%s</dd>
</dl>
""" % (
  escapeHTML(SSL_CLIENT_S_DN),
  escapeHTML(SSL_CLIENT_I_DN),
))

