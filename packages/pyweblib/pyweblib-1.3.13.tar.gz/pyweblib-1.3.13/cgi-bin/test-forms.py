#!/usr/bin/python2.3

import sys,os,types

# Where to find own modules
sys.path.append('/home/michael/Proj/python/pyweblib')

import pyweblib

from pyweblib import forms

def ErrorExit(Msg):
  print """Content-type: text/html

<html>
  <title>
    Error
  </title>
  <body>
    <h1>Error</h1>
    <p>%s</p>
  </body>
</html>
""" % Msg

def PrintEmptyInputForm(form,Msg=''):
  print """Content-type: text/html

<html>
  <title>
    Give me some data!
  </title>
  <body>
    <h1>Give me some data!</h1>
    <form
      method="POST"
      enctype="multipart/form-data"
      action="%s"
    >
      <table border>
""" % (os.environ['SCRIPT_NAME'])
  for name in form.declaredFieldNames:
    f = form.field[name]
    print '<TR><TD>%s%s</TD><TD>%s</TD></TR>' % (
      f.labelHTML(),f.required*'<BR>required',f.inputHTML()
    )
  print """      </table>
      <input type="submit" value="Send">
    </form>
  </body>
</html>
"""

def PrintInputData(form):
  # Anzeige der eingegebenen Daten
  print """Content-type: text/html

<html>
  <title>
    Your input data
  </title>
  <body>
    <h1>Your input data</h1>
    <table border>
"""
  for i in form.inputFieldNames:
    contentlist = []
    f = form.field[i]
    if f.value != None:
      if type(f.value) is types.ListType:
        contentlist.extend(f.valueHTML())
      else:
        contentlist.append(f.valueHTML())
    else:
      contentlist.append('&nbsp;')
    print '<tr><td>%s</td><td>%s</td></tr>' % (i,'<br>'.join(contentlist))
  print """
    </table>
  </body>
</html>
"""

form = forms.Form(sys.stdin,os.environ)
form.addField(
  forms.Input(
    'param_input','Input',255,1,'abc.*',accessKey='1',
    size=25
  )
)
form.addField(
  forms.HiddenInput(
    'param_hidden','HiddenInput',255,1,'.*',default='Hidden Value',
    show=1
  )
)
form.addField(
  forms.Password(
    'param_password','Password',16,1,'.*',accessKey='3'
  )
)
form.addField(
  forms.Select(
    'param_select','Select',3,
    options=[('value1','Option 1'),'value2',('value3','Option 3')],
    default=['value2','value3'],
    size=3,multiSelect=1
  )
)
form.addField(
  forms.Radio('param_radio','Radio',default='value2',
    options=[('value1','Option 1'),'value2',('value3','Option 3')],
  )
)
form.addField(
  forms.Textarea(
    'param_textarea',
    'Additional Comments',
    1000,1,'Longer text:.*',default='Longer text:\nWrite here...',
    rows=5,cols=50
  )
)
form.addField(
  forms.Checkbox(
    'param_checkbox','Checkbox',default='Checked value'
  )
)
form.addField(
  forms.File(
    'param_file','File upload',100000,1,None,default='/etc/passwd',size=30
  )
)

try:
  form.getInputFields()
except forms.FormException,e:
  ErrorExit(e.html())

if not form.inputFieldNames:
  PrintEmptyInputForm(form,'')
else:
  PrintInputData(form)

sys.exit(0)
