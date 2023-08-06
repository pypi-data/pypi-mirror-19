# -*- coding: utf-8 -*-
"""
pyweblib.forms - class library for handling <FORM> input
(C) 1998-2015 by Michael Ströder <michael@stroeder.com>

This module is distributed under the terms of the
GPL (GNU GENERAL PUBLIC LICENSE) Version 2
(see http://www.gnu.org/copyleft/gpl.html)

Python compability note:
This module only works with Python 2.0 since all string parameters
are assumed to be Unicode objects and string methods are used instead
string module.
"""

# File specific
__revision__ = '$Revision: 1.53 $'.split(' ')[1]
__info__ = '$Id: forms.py,v 1.53 2015/01/10 14:37:17 michael Exp $'


import sys,types,re,urllib
import helper

def escapeHTML(s):
  """
  Escape all characters with a special meaning in HTML
  to appropriate character tags
  """
  s = s.replace('&','&#38;')
  s = s.replace('<','&#60;')
  s = s.replace('>','&#62;')
  s = s.replace("'",'&#39;')
  s = s.replace('"','&#34;')
  s = s.replace(':','&#58;')
  s = s.replace('=','&#61;')
  s = s.replace('{','&#123;')
  s = s.replace('}','&#125;')
  s = s.replace('(','&#40;')
  s = s.replace(')','&#41;')
  s = s.replace('`','&#96;')
  return s


class Field:
  """
  Base class for all kind of single input fields.

  In most cases this class is not used directly
  since derivate classes for most types of input fields exist.
  """

  def __init__(
    self,name,text,maxLen,maxValues,pattern,required=0,default=None,accessKey='',
  ):
    """
    name
        Field name used in <input name="..">
    text
        User-friendly text describing this field
    maxLen
        maximum length of a single input value [Bytes]
    maxValues
        maximum amount of input values
    default
        default value to be used in method inputfield()
    required
        flag which marks field as mandantory input field
    accessKey
        key for accessing this field to be displayed by method inputHTML()
    pattern
        regex pattern of valid values either as string
        or tuple (pattern,options)
    """
    self.value = []
    self.name = name
    self.text = text
    self.maxLen = maxLen
    self.maxValues = maxValues
    self.required = required
    self.accessKey = accessKey
    self.inputHTMLTemplate = r'%s'
    self.valueHTMLTemplate = r'%s'
    # Charset is the preferred character set of the browser.
    # This is set by Form.add() the something meaningful.
    self.charset = 'iso-8859-1'
    self.setDefault(default)
    self.setRegex(pattern)

  def _accessKeyAttr(self):
    if self.accessKey:
      return 'accesskey="%s"' % (self.accessKey)
    else:
      return ''

  def idAttrStr(self,id_value):
    if id_value is None:
      return ''
    else:
      return 'id="%s" ' % (id_value)

  def labelHTML(self,labelText=None,for_value=None):
    labelText = (labelText or self.text).encode(self.charset)
    return '<label for="%s">%s</label>' % (for_value or self.name,labelText)

  def getValue(self):
    """
    Returns self.value in case of multi-valued input or
    self.value[0] if only one value is allowed.
    """
    if self.maxValues>1:
      return self.value
    else:
      return self.value[0]

  def setDefault(self,default):
    """
    Set the default of a field.

    Mainly this is used by the application if self.default shall
    be changed after initializing the field object.
    """
    if type(default)==types.ListType:
      self.default = [i for i in default if i!=None]
    else:
      self.default = default or ''

  def _patternAndOptions(self,pattern):
    """
    The result is a tuple (pattern string,pattern options).

    pattern
        Either a string containing a regex pattern,
        a tuple (pattern string, pattern options) or None.
    """
    if type(pattern) is types.TupleType:
      return pattern
    else:
      return pattern, 0

  def setRegex(self,pattern):
    """
    Set the regex pattern for validating this field.

    Mainly this is used if self._re shall be changed after
    the field object was initialized.

    pattern
        Either a string containing a regex pattern,
        a tuple (pattern string, pattern options) or None.
        If None regex checking in _validateFormat is switched off
        (not recommended).
    """
    patternstring,patternoptions = self._patternAndOptions(pattern)
    if patternstring is None:
      # Regex checking is completely switched off
      self._re = None
    else:
      # This is a Unicode input field
      patternoptions = patternoptions | re.U
      self._re = re.compile('%s$' % patternstring,patternoptions)

  def _validateLen(self,value):
    """Check length of the user's value for this field."""
    if len(value)>self.maxLen:
      raise InvalidValueLen(self.name,self.text,len(value),self.maxLen)

  def _validateFormat(self,value):
    """
    Check format of the user's value for this field.

    Empty input (zero-length string) are valid in any case.
    You might override this method to change this behaviour.
    """
    if (not self._re is None) and value:
      rm = self._re.match(value)
      if rm is None:
        raise InvalidValueFormat(
          self.name,
          self.text.encode(self.charset),
          value.encode(self.charset)
        )

  def _validateMaxValue(self):
    if len(self.value)>=self.maxValues:
      raise TooManyValues(self.name,self.text,len(self.value),self.maxValues)

  def _encodeValue(self,value):
    """
    Return Unicode object or string to be stored in self.value
    """
    try:
      value = unicode(value,self.charset)
    except UnicodeError:
      # Work around buggy browsers...
      value = unicode(value,'iso-8859-1')
    return value

  def setValue(self,value):
    """
    Store the user's value into the field object.

    This method can be used to modify the user's value
    before storing it into self.value.
    """
    value = self._encodeValue(value)
    # Check if input is valid
    # Length valid?
    self._validateLen(value)
    # Format valid?
    self._validateFormat(value)
    self._validateMaxValue()
    self.value.append(value)

  def setCharset(self,charset):
    """Define the character set of the user's input."""
    self.charset = charset

  def _defaultValue(self,default):
    """returns default value"""
    return default or self.__dict__.get('default','')

  def titleHTML(self,title):
    """HTML output of default."""
    return escapeHTML(title or self.text).encode(self.charset)

  def _defaultHTML(self,default):
    """HTML output of default."""
    return escapeHTML(self._defaultValue(default)).encode(self.charset)

  def valueHTML(self):
    """
    HTML output of self.value using the HTML template string
    in self.valueHTMLTemplate.
    """
    return [
      self.valueHTMLTemplate % v
      for v in self.value
    ]


class Textarea(Field):
  """
  Multi-line input field:
  <textarea>
  """

  def __init__(
    self,name,text,maxLen,maxValues,pattern,required=0,default=None,accessKey='',
    rows=10,cols=60
  ):
    self.rows  = rows
    self.cols  = cols
    Field.__init__(
      self,name,text,maxLen,maxValues,None,required,default,accessKey
    )

  def setRegex(self,pattern):
    """
    Like Field.setRegex() but pattern options re.S and re.M are
    automatically added.
    """
    patternstring,patternoptions = self._patternAndOptions(pattern)
    # This is a Unicode input field
    patternoptions = patternoptions | re.M|re.S
    Field.setRegex(self,(patternstring,patternoptions))

  def inputHTML(self,default=None,id_value=None,title=None):
    """Returns string with HTML input field."""
    return self.inputHTMLTemplate % (
      '<textarea %stitle="%s" name="%s" %s rows="%d" cols="%d">%s</textarea>' % (
        self.idAttrStr(id_value),
        self.titleHTML(title),
        self.name,
        self._accessKeyAttr(),
        self.rows,self.cols,
        self._defaultHTML(default)
      )
    )

  def valueHTML(self):
    """
    HTML output of self.value using the HTML template string
    in self.valueHTMLTemplate.
    """
    return [
      self.valueHTMLTemplate % '<pre>%s</pre>' % v
      for v in self.value
    ]


class Input(Field):
  """
  Normal one-line input field:
  <input>
  """

  def __init__(
    self,name,text,maxLen,maxValues,pattern,required=0,default=None,accessKey='',
    size=None
  ):
    self.size = size or maxLen
    Field.__init__(
      self,name,text,maxLen,maxValues,pattern,required,default,accessKey,
    )

  def inputHTML(self,default=None,id_value=None,title=None):
    return self.inputHTMLTemplate % (
      '<input %stitle="%s" name="%s" %s maxlength="%d" size="%d" value="%s">' % (
        self.idAttrStr(id_value),
        self.titleHTML(title),
        self.name,
        self._accessKeyAttr(),
        self.maxLen,
        self.size,
        self._defaultHTML(default)
      )
    )


class HiddenInput(Input):
  """
  Hidden input field:
  <input type="hidden">
  """

  def __init__(
    self,name,text,maxLen,maxValues,pattern,required=0,default=None,accessKey=''
  ):
    Input.__init__(
      self,name,text,maxLen,maxValues,pattern,required,default,accessKey,
    )

  def inputHTML(self,default=None,id_value=None,title=None,show=0):
    default_html = self._defaultHTML(default)
    if show:
      default_str = default_html
    else:
      default_str = ''
    return self.inputHTMLTemplate % (
      '<input type="hidden" %stitle="%s" name="%s" %s  value="%s">%s' % (
        self.idAttrStr(id_value),
        self.titleHTML(title),
        self.name,
        self._accessKeyAttr(),
        default_html,
        default_str
      )
    )


class File(Input):
  """
  File upload field
  <input type="file">
  """
  mimeType='application/octet-stream'

  def _validateFormat(self,value):
    """Binary data is assumed to be valid all the time"""
    return

  def _encodeValue(self,value):
    """
    Return Unicode object or string to be stored in self.value
    """
    return value

  def inputHTML(self,default=None,id_value=None,title=None,mimeType=None):
    return self.inputHTMLTemplate % (
      '<input type="file" %stitle="%s" name="%s" %s accept="%s">' % (
        self.idAttrStr(id_value),
        self.titleHTML(title),
        self.name,
        self._accessKeyAttr(),
        mimeType or self.mimeType
      )
    )


class Password(Input):
  """
  Password input field:
  <input type="password">
  """

  def inputHTML(self,default=None,id_value=None,title=None):
    return self.inputHTMLTemplate % (
      '<input %stitle="%s" name="%s" %s maxlength="%d" size="%d" type="password" value="%s">' % (
        self.idAttrStr(id_value),
        self.titleHTML(title),
        self.name,
        self._accessKeyAttr(),
        self.maxLen,
        self.size,
        default or ''
      )
    )

  def valueHTML(self):
    """For security reasons only stars are printed"""
    return [
      self.valueHTMLTemplate % (len(v)*'*')
      for v in self.value
    ]


class Radio(Field):
  """
  Radio buttons:
  <input type="radio">
  """

  def __init__(
    self,name,text,maxValues=1,required=0,default=None,accessKey='',
    options=None
  ):
    """
    pattern and maxLen are determined from __init__ params
    Additional parameters:
    options=[]
      List of options. Either just a list of strings
      ['value1','value2',..] for simple options
      or a list of tuples of string pairs
      [('value1','description1),('value2','description2),..]
      for options with different option value and description.
    """
    self.setOptions(options)
    self.setDefault(default)
    Field.__init__(
      self,name,text,self.maxLen,maxValues,'',required,default,accessKey
    )

  def _validateFormat(self,value):
    """
    Check format of the user's value for this field.

    Empty input (zero-length string) are valid in any case.
    You might override this method to change this behaviour.
    """
    if value and (not value in self.optionValues):
      raise InvalidValueFormat(
        self.name,
        self.text.encode(self.charset),
        value.encode(self.charset)
      )

  def setOptions(self,options):
    self.optionValues = {}
    self.maxLen = 0
    if options:
      optionValues = []
      for i in options:
        if type(i) is types.TupleType:
          optionValue = i[0]
        else:
          optionValue = i
        self.optionValues[optionValue] = None
      self.maxLen = max(map(len,self.optionValues.keys()))
    self.options  = options

  def inputHTML(self,default=None,id_value=None,title=None):
    s = []
    default_value = self._defaultValue(default)
    for i in self.options:
      if type(i) is types.TupleType:
        optionValue,optionText = i
      else:
        optionValue = optionText = i
      s.append("""
        <input
          type="radio"
          %s
          title="%s"
          name="%s"
          %s
          value="%s"
          %s
        >%s<br>
        """ % (
          self.idAttrStr(id_value),
          self.titleHTML(title),
          self.name.encode(self.charset),
          self._accessKeyAttr(),
          optionValue.encode(self.charset),
          ' checked'*(optionValue==default_value),
          optionText.encode(self.charset)
        )
      )
    return self.inputHTMLTemplate % '\n'.join(s)

  def setDefault(self,default):
    """
    Set the default of a default field.

    Mainly this is used if self.default shall be changed after
    initializing the field object.
    """
    optionValues = []
    for i in self.options:
      if type(i) is types.TupleType:
        optionValues.append(i[0])
      else:
        optionValues.append(i)
    if type(default)==types.StringType and not default in optionValues:
      # Append option to list of options if singleton
      self.options.append(default)
    elif type(default)==types.ListType:
      # Extend list of options with items in default which are not in options
      self.options.extend(filter(lambda x,o=optionValues:not x in o,default))
    self.default = default


class Select(Radio):
  """
  Select field:
  <select multiple>
    <option value="value">description</option>
  </select>
  """

  def __init__(
    self,name,text,maxValues,required=0,default=None,accessKey='',
    options=None,size=1,ignoreCase=0,multiSelect=0,
  ):
    """
    Additional parameters:
    size
      Integer for the size of displayed select field.
    ignorecase
      Integer flag. If non-zero the case of input strings is ignored
      when checking input values.
    multiSelect
      Integer flag. If non-zero the select field has HTML attribute
      "multiple" set.
    """
    self.size        = size
    self.multiSelect = multiSelect
    self.ignoreCase  = ignoreCase
    Radio.__init__(
      self,name,text,maxValues,required,default,accessKey,options,
    )

  def inputHTML(self,default=None,id_value=None,title=None):
    s = ['<select %stitle="%s" name="%s" %s  size="%d" %s>' % (
      self.idAttrStr(id_value),
      self.titleHTML(title),
      self.name,
      self._accessKeyAttr(),
      self.size,
      " multiple"*(self.multiSelect>0)
    )]
    default_value = self._defaultValue(default)
    for i in self.options:
      if type(i) is types.TupleType:
        try:
          optionValue,optionText,optionTitle = i
        except ValueError:
          optionTitle = None
          optionValue,optionText = i
      else:
        optionTitle = None
        optionValue = optionText = i
      if self.multiSelect:
        option_selected = optionValue in default_value
      else:
        option_selected = (optionValue==default_value) or (self.ignoreCase and optionValue.lower()==default_value.lower())
      if optionTitle:
        optionTitle_attr = ' title="%s"' % escapeHTML(optionTitle.encode(self.charset))
      else:
        optionTitle_attr = ''
      s.append(
        '<option value="%s"%s%s>%s</option>' % (
          escapeHTML(optionValue.encode(self.charset)),
          optionTitle_attr,
          ' selected'*(option_selected),
          escapeHTML(optionText.encode(self.charset)),
        )
      )
    s.append('</select>')
    return self.inputHTMLTemplate % '\n'.join(s)


class Checkbox(Field):
  """
  Check boxes:
  <input type="checkbox">
  """

  def __init__(
    self,name,text,maxValues=1,required=0,accessKey='',
    default=None,checked=0
  ):
    """
    pattern and maxLen are determined by default
    """
    pattern = default
    maxLen = len(default or '')
    self.checked = checked
    Field.__init__(
      self,name,text,maxLen,maxValues,pattern,required,default,accessKey
    )

  def inputHTML(self,default=None,id_value=None,title=None,checked=None):
    if checked is None:
      checked = self.checked
    return self.inputHTMLTemplate % (
      '<input type="checkbox" %stitle="%s" name="%s" %s value="%s"%s>' % (
        self.idAttrStr(id_value),
        self.titleHTML(title),
        self.name,
        self._accessKeyAttr(),
        self._defaultValue(default),' checked'*(checked)
      )
    )


class Keygen(Field):
  """
  Select field for client-side key generation with
  Netscape/Mozilla/Opera browser:
  <KEYGEN>
  """

  def __init__(
    self,name,text,maxLen,maxValues,required=0,
    minKeyLength=512
  ):
    Field.__init__(
      self,name,text,maxLen,maxValues,(r'[ -z\r\n]*',re.M+re.S),required
    )
    self.minKeyLength = minKeyLength

  def _encodeValue(self,value):
    return value.replace('\n','').replace('\r','')

  def inputHTML(self,challenge,id_value=None,title=None,):
    return self.inputHTMLTemplate % (
      '<keygen %stitle="%s" name="%s" %s challenge="%s">' % (
        self.idAttrStr(id_value),
        self.titleHTML(title),
        self.name,
        self._accessKeyAttr(),
        challenge
      )
    )

  def valueHTML(self):
    return self.valueHTMLTemplate % ('%d Bytes' % (len(self.value)))


class FormException(Exception):
  """
  Base exception class to indicate form processing errors.

  Attributes:
  args          unstructured List of parameters
  """
  def __init__(self,*args,**kwargs):
    self.args = args
    for key,value in kwargs.items():
      setattr(self,key,value)
  def html(self):
    return escapeHTML(str(self))

class InvalidRequestMethod(FormException):
  """
  Exception raised when HTTP request method was invalid.

  Attributes:
  method        string containing method used
  """
  def __init__(self,method):
    self.method = method
  def __str__(self):
    return 'Invalid request method %s.' % (self.method)

class InvalidFormEncoding(FormException):
  """
  The form data is malformed.

  Attributes:
  param         name/value causing the exception
  """
  def __init__(self,param):
    self.param = param
  def __str__(self):
    return 'The form data is malformed.'

class ContentLengthExceeded(FormException):
  """
  Overall length of input data too large.

  Attributes:
  contentLength         received content length
  maxContentLength      maximum valid content length
  """
  def __init__(self,contentLength,maxContentLength):
    self.contentLength = contentLength
    self.maxContentLength = maxContentLength
  def __str__(self):
    return 'Input length of %d bytes exceeded the maximum of %d bytes.' % (
      self.contentLength,self.maxContentLength
    )

class UndeclaredFieldName(FormException):
  """
  Parameter with undeclared name attribute received.

  Attributes:
  name          name of undeclared field
  """
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return 'Unknown parameter %s.' % (self.name)

class ParamsMissing(FormException):
  """
  Required parameters are missing.

  Attributes:
  missingParamNames     list of strings containing all names of missing
                        input fields.
  """
  def __init__(self,missingParamNames):
    self.missingParamNames = missingParamNames
  def __str__(self):
    return 'Required fields missing: %s' % (
      ', '.join(
        map(
          lambda i:'%s (%s)' % (i[1],i[0]),
          self.missingParamNames
        )
      )
    )

class InvalidValueFormat(FormException):
  """
  The user's input does not match the required format.

  Attributes:
  name          name of input field (Field.name)
  text          textual description of input field (Field.text)
  value         input value received
  """
  def __init__(self,name,text,value):
    self.name = name
    self.text = text
    self.value = value
  def __str__(self):
    return 'Input value "%s" for field %s (%s) has invalid format.' % (
      self.value,self.text,self.name
    )

class InvalidValueLen(FormException):
  """
  Length of user input value invalid.

  Attributes:
  name          name of input field (Field.name)
  text          textual description of input field (Field.text)
  valueLen      integer number of received value length
  maxValueLen   integer number of maximum value length
  """
  def __init__(self,name,text,valueLen,maxValueLen):
    self.name      = name
    self.text      = text
    self.valueLen    = valueLen
    self.maxValueLen = maxValueLen
  def __str__(self):
    return 'Content too long. Field %s (%s) has %d characters but is limited to %d.' % (
      self.text,self.name,self.valueLen,self.maxValueLen
    )

class TooManyValues(FormException):
  """
  User's input contained too many values for same parameter.

  Attributes:
  name                  name of input field (Field.name)
  text                  textual description of input field (Field.text)
  valueCount            integer number of values counted with name
  maxValueCount         integer number of maximum values with name allowed
  """
  def __init__(self,name,text,valueCount,maxValueCount):
    self.name      = name
    self.text      = text
    self.valueCount    = valueCount
    self.maxValueCount = maxValueCount
  def __str__(self):
    return '%d values for field %s (%s). Limited to %d input values.' % (
      self.valueCount,self.text,self.name,self.maxValueCount
    )


class Form:
  """
  Class for declaring and processing a whole <form>
  """

  def __init__(self,inf,env):
    """
    Initialize a Form
    inf                 Read from this file object if method is POST.
    env                 Dictionary holding the environment vars.
    """
    # Dictionary of Field objects
    self.field = {}
    # Ordered list of input field names
    self.declaredFieldNames = []
    # List of parameters names received
    self.inputFieldNames = []
    # Save the environment vars
    self.env = env
    # input file object
    self.inf = inf or sys.stdin
    # Save request method
    self.request_method = env['REQUEST_METHOD']
    self.script_name = env['SCRIPT_NAME']
    # Initialize the AcceptHeaderDict objects
    self.http_accept_charset = helper.AcceptCharsetDict('HTTP_ACCEPT_CHARSET',env)
    self.http_accept_language = helper.AcceptHeaderDict('HTTP_ACCEPT_LANGUAGE',env)
    self.accept_language = self.http_accept_language.keys()
    self.http_accept_encoding = helper.AcceptHeaderDict('HTTP_ACCEPT_ENCODING',env)
    # Set the preferred character set
    self.accept_charset = self.http_accept_charset.preferred()
    # Determine query string and content length dependent on request method
    self.checkRequestMethod()
    return # Form.__init__()

  def checkRequestMethod(self):
    """
    Checks whether the HTTP request method is accepted
    """
    if not self.request_method in ['POST','GET']:
      raise InvalidRequestMethod(self.request_method)

  def getContentType(self):
    """
    Determine the HTTP content type of HTTP request
    """
    if self.request_method=='POST':
      return self.env.get('CONTENT_TYPE','application/x-www-form-urlencoded').lower() or None
    elif self.request_method=='GET':
      return 'application/x-www-form-urlencoded'

  def addField(self,f):
    """
    Add a input field object f to the form.
    """
    f.setCharset(self.accept_charset)
    self.field[f.name] = f
    if not f.name in self.declaredFieldNames:
      self.declaredFieldNames.append(f.name)
    return # Form.addField()

  def getInputValue(self,name,default=[]):
    """
    Return input value of a field defined by name if presented
    in form input. Return default else.
    """
    if name in self.inputFieldNames:
      return self.field[name].value
    else:
      return default

  def hiddenInputFields(self,outf=sys.stdout,ignoreFieldNames=None):
    """
    Output all parameters as hidden fields.

    outf
        File object for output.
    ignoreFieldNames
        Names of parameters to be excluded.
    """
    ignoreFieldNames=ignoreFieldNames or []
    for f in [
      self.field[p]
      for p in self.declaredFieldNames
      if (p in self.inputFieldNames) and not (p in ignoreFieldNames)
    ]:
      for v in f.value:
        outf.write(
          '<input type="hidden" name="%s" value="%s">\n\r' % (
            f.name.encode(f.charset),escapeHTML(v.encode(f.charset))
          )
        )
    return # Form.hiddenInputFields()

  def _parseFormUrlEncoded(self,maxContentLength,ignoreEmptyFields,ignoreUndeclaredFields,stripValues,unquote):

    if self.request_method=='POST':
      query_string = self.inf.read(int(self.env['CONTENT_LENGTH']))
    elif self.request_method=='GET':
      query_string = self.env.get('QUERY_STRING','')

    self.inf.close()

    inputlist = query_string.split('&')

    contentLength = 0

    # Loop over all name attributes declared
    for param in inputlist:

      if param:

        # Einzelne Parametername/-daten-Paare auseinandernehmen
        try:
          name,value = param.split('=',1)
        except ValueError:
          raise InvalidFormEncoding(param)
        name = unquote(name).strip()

        if not name in self.declaredFieldNames:
          if ignoreUndeclaredFields:
            continue
          else:
            raise UndeclaredFieldName(name)

        value = unquote(value)
        if stripValues:
          value = value.strip()

        contentLength += len(value)
        # Gesamtlaenge der Daten noch zulaessig?
        if contentLength > maxContentLength:
          raise ContentLengthExceeded(contentLength,maxContentLength)

        f = self.field[name]

        # input is empty string?
        if value or (not ignoreEmptyFields):
          # Input is stored in field instance
          f.setValue(value)
          # Add name of field to list of input keys
          if not name in self.inputFieldNames:
            self.inputFieldNames.append(name)

    return #_parseFormUrlEncoded()


  def _parseMultipartFormData(self,maxContentLength,ignoreEmptyFields,ignoreUndeclaredFields,stripValues,unquote):

    import cgi
    ctype, pdict = cgi.parse_header(self.env['CONTENT_TYPE'])
    parts = cgi.parse_multipart(self.inf,pdict)

    contentLength = 0

    for name in parts.keys():

      if not name in self.declaredFieldNames:
        if ignoreUndeclaredFields:
          continue
        else:
          raise UndeclaredFieldName(name)

      for value in parts[name]:

#        if stripValues:
#     value = value.strip()

        contentLength += len(value)
        # Gesamtlaenge der Daten noch zulaessig?
        if contentLength > maxContentLength:
          raise ContentLengthExceeded(contentLength,maxContentLength)

        f = self.field[name]

        # input is empty string?
        if value or (not ignoreEmptyFields):
          # Input is stored in field instance
          f.setValue(value)
          # Add name of field to list of input keys
          if not name in self.inputFieldNames:
            self.inputFieldNames.append(name)

    return # _parseMultipartFormData()


  def getInputFields(
    self,
    ignoreEmptyFields=0,
    ignoreUndeclaredFields=0,
    stripValues=1,
    unquotePlus=0,
  ):
    """
    Process user's <form> input and store the values in each
    field instance's content attribute.

    When a processing error occurs FormException (or derivatives)
    are raised.

    ignoreEmptyFields=0         Ignore fields with empty input.
    ignoreUndeclaredFields=0    Ignore fields with names not declared.
                                Normally UndeclaredFieldName is raised.
    stripValues=1               If true leading and trailing whitespaces
                                are stripped from all input values.
    unquotePlus=0
       If non-zero urllib.unquote_plus() is used instead of urllib.unquote().
    """

    unquote = {0:urllib.unquote_plus,1:urllib.unquote_plus}[unquotePlus]

    # Calculate maxContentLength
    maxContentLength = 0
    for name,f in self.field.items():
      maxContentLength += f.maxValues*f.maxLen

    content_type = self.getContentType()
    if content_type.startswith('application/x-www-form-urlencoded'):
      # Parse user's input
      self._parseFormUrlEncoded(maxContentLength,ignoreEmptyFields,ignoreUndeclaredFields,stripValues,unquote)
    elif content_type.startswith('multipart/form-data'):
      self._parseMultipartFormData(maxContentLength,ignoreEmptyFields,ignoreUndeclaredFields,stripValues,unquote)
    else:
      raise FormException('Invalid content type %s received' % (repr(content_type)))


    # Are all required parameters present?
    missing_params = []
    for n,f in self.field.items():
      if f.required and not (f.name in self.inputFieldNames):
        missing_params.append((f.name,f.text))
    if missing_params:
      raise ParamsMissing(missing_params)

    return # Form.getInputFields()
