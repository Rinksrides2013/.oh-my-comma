#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import psutil
import difflib
import argparse
import subprocess
if __package__ is None:
  from os import path
  sys.path.append(path.abspath(path.join(path.dirname(__file__), '../py_utils')))
  from py_utils.colors import COLORS
else:
  from py_utils.colors import COLORS

SYSTEM_BASHRC_PATH = '/home/.bashrc'
COMMUNITY_PATH = '/data/community'
COMMUNITY_BASHRC_PATH = '/data/community/.bashrc'
OH_MY_COMMA_PATH = '/data/community/.oh-my-comma'
UPDATE_PATH = '{}/update.sh'.format(OH_MY_COMMA_PATH)
UNINSTALL_PATH = '{}/uninstall.sh'.format(OH_MY_COMMA_PATH)
OPENPILOT_PATH = '/data/openpilot'


class ArgumentParser(argparse.ArgumentParser):
  def error(self, message):
    raise Exception('error: {}'.format(message))


class BaseFunctions:
  def print_commands(self, error_msg=None, ascii_art=False):
    if ascii_art:
      print(EMU_ART)

    if error_msg is not None:
      error(error_msg)
    max_cmd = max([len(_c) for _c in self.commands]) + 1
    for idx, cmd in enumerate(self.commands):
      desc = COLORS.CYAN + self.commands[cmd].description
      print(COLORS.OKGREEN + ('- {:<%d} {}' % max_cmd).format(cmd + ':', desc))
      if hasattr(self, '_help'):
        # leading is for better differentiating between the different commands
        self._help(cmd, show_description=False, leading='')  # todo: decide if leading is better than no leading
        if idx == len(self.commands) - 1:  # removes double newlines at end of loop
          print()
    print(COLORS.ENDC, end='')

  def next_arg(self, lower=True, ingest=True):
    """
    Returns next arg and deletes arg from self.args if ingest=True
    :param lower: Returns arg.lower()
    :param ingest: Deletes returned arg from self.arg
    :return:
    """
    if len(self.args):
      arg = self.args[0]
      if lower:
        arg = arg.lower()
      if ingest:
        del self.args[0]
    else:
      arg = None
    return arg


def input_with_options(options, default=None):
  """
  Takes in a list of options and asks user to make a choice.
  The most similar option list index is returned along with the similarity percentage from 0 to 1
  """
  def str_sim(a, b):
    return difflib.SequenceMatcher(a=a, b=b).ratio()

  user_input = input('[{}]: '.format('/'.join(options))).lower().strip()
  if not user_input:
    return default, 0.0
  sims = [str_sim(i.lower().strip(), user_input) for i in options]
  argmax = sims.index(max(sims))
  return argmax, sims[argmax]


def check_output(cmd):
  """
  If cmd is a string, it is split into a list, otherwise it doesn't modify cmd.
  The status is returned, True being success, False for failure
  """
  if isinstance(cmd, str):
    cmd = cmd.split()

  try:
    return subprocess.check_output(cmd)
  except Exception as e:
    # print(e)
    return False


def run(cmd, out_file=None):
  """
  If cmd is a string, it is split into a list, otherwise it doesn't modify cmd.
  The status is returned, True being success, False for failure
  """
  if isinstance(cmd, str):
    cmd = cmd.split()

  f = None
  if isinstance(out_file, str):
    f = open(out_file, 'a')

  try:
    r = subprocess.call(cmd, stdout=f)
    return not r
  except Exception as e:
    # print(e)
    return False


def kill(procname):
  for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == procname:
      proc.kill()
      return True
  return None


def is_affirmative():
  i = None
  print(COLORS.PROMPT)
  while i not in ['y', 'n', 'yes', 'no']:
    i = input('[Y/n]: ').lower().strip()
  print(COLORS.ENDC)
  return i in ['y', 'yes']


def error(msg, end='\n', ret=False):
  """
  The following applies to error, warning, and success methods
  :param msg: The message to display
  :param end: The ending char, default is \n
  :param ret: Whether to return the formatted string, or print it
  :return: The formatted string if ret is True
  """
  e = '{}{}{}'.format(COLORS.FAIL, msg, COLORS.ENDC)
  if ret:
    return e
  print(e, end=end)


def warning(msg, end='\n', ret=False):
  w = '{}{}{}'.format(COLORS.WARNING, msg, COLORS.ENDC)
  if ret:
    return w
  print(w, end=end)


def success(msg, end='\n', ret=False):
  s = '{}{}{}'.format(COLORS.SUCCESS, msg, COLORS.ENDC)
  if ret:
    return s
  print(s, end=end)


EMU_ART = r"""            _
         -=(""" + COLORS.RED + """'""" + COLORS.CWHITE + """)
           ;;
          //
         //
        : '.---.__
        |  --_-_)__) 
        `.____,'     
           \  \      """ + COLORS.OKGREEN + """ ___ ._ _ _  _ _ """ + COLORS.CWHITE + """
         ___\  \     """ + COLORS.OKGREEN + """/ ._>| ' ' || | |""" + COLORS.CWHITE + """
        (       \    """ + COLORS.OKGREEN + """\___.|_|_|_|`___|""" + COLORS.CWHITE + """
                 \   
                 /""" + '\n'