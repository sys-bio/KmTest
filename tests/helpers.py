from SBviper.simple_sbml import constants as cn
from SBviper.simple_sbml.simple_sbml import SimpleSBML

import libsbml
import os

DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(DIR, "test_file.xml")


def getSimple():
    return SimpleSBML(TEST_PATH)
