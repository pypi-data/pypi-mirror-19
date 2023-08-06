#!/bin/python

import os
import sys
from flask_script import Server, Manager, Shell
import unittest
import json
import shutil
import time
import git
from openedoo_cli import app
from utils import *

manager = Manager(app)

BASE_DIR = os.path.dirname(os.path.realpath(__name__))
BASE = os.path.join(BASE_DIR, 'openedoo')

@manager.command
def run():
    """ run server with wekezeug """
    pass

@manager.command
def test():
    """unit_testing"""
    print "no problemo"
    pass

@manager.command
def install():
    print download(name=name)


def main():
    manager.run()
