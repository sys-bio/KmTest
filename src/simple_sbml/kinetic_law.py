'''Provides Information on SBML Kinetics Laws'''


from simple_sbml import constants as cn
from simple_sbml import util
from simple_sbml import exceptions

import collections
import numpy as np
import libsbml
import zipfile


class KineticLaw(object):

  def __init__(self, libsbml_kinetics, reaction):
    """
    :param libsbml.KineticLaw libsbml_kinetics:
    """
    # libsbml object for kinetics
    self.libsbml_kinetics = libsbml_kinetics
    # String version of chemical formula
    self.formula = self.libsbml_kinetics.getFormula()
    # Reaction for the kinetics law
    self.reaction = reaction
    # Parameters and chemical species
    self.symbols = self._getSymbols()

  def __repr__(self):
    return self.formula

  def _getSymbols(self):
    """
    Finds the parameters and species names for the
    kinetics law. Exposing this information requires
    a recursive search of the parse tree for the
    kinetics expression.
    :return list-str:
    """
    global cur_depth
    MAX_DEPTH = 20
    cur_depth = 0
    def augment(ast_node, result):
      global cur_depth
      cur_depth += 1
      if cur_depth > MAX_DEPTH:
        raise exceptions.BadKineticsMath(self.reaction.id)
      for idx in range(ast_node.getNumChildren()):
        child_node = ast_node.getChild(idx)
        if child_node.getName() is None:
          additions = augment(child_node, result)
          result.extend(additions)
        else:
          result.append(child_node.getName())
      return result
    # 
    ast_node = self.libsbml_kinetics.getMath()
    result = []
    return augment(ast_node, result)
    return result
