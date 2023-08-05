##############################################################################
##
## This file is part of Sardana
##
## http://www.sardana-controls.org/
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""This module contains macros that demonstrate the usage of macro parameters"""

from sardana.macroserver.macro import *

__all__ = ["pt0", "pt1", "pt2", "pt3", "pt4", "pt5", "pt6", "pt7", "pt8",
           "pt9"]

class pt0(Macro):
    """Macro without parameters. Pretty dull"""

    param_def = []
    
    def run(self):
        pass
    
class pt1(Macro):
    """Macro with one float parameter: Each parameter is described in the 
    param_def sequence as being a sequence of four elements: name, type, 
    default value and description"""
    
    param_def = [ [ 'value', Type.Float, None, 'some bloody float'] ]
    
    def run(self, f):
        pass

class pt2(Macro):
    """Macro with one Motor parameter: Each parameter is described in the 
    param_def sequence as being a sequence of four elements: name, type, 
    default value and description"""

    param_def = [ [ 'motor', Type.Motor, None, 'some bloody motor'] ]
    
    def run(self, m):
        pass

class pt3(Macro):
    """Macro with a list of numbers as parameter: the type is a sequence of
    parameter types which is repeated. In this case it is a repetition of a 
    float so only one parameter is defined.
    By default the repetition as a semantics of 'at least one'"""

    param_def = [
       [ 'numb_list', [ [ 'pos', Type.Float, None, 'value'] ], None, 'List of values'],
    ]
    
    def run(self, *args, **kwargs):
        pass

class pt4(Macro):
    """Macro with a list of motors as parameter: the type is a sequence of
    parameter types which is repeated. In this case it is a repetition of a 
    motor so only one parameter is defined.
    By default the repetition as a semantics of 'at least one'"""

    param_def = [
       [ 'motor_list', [ [ 'motor', Type.Motor, None, 'motor name'] ], None, 'List of motors'],
    ]
    
    def run(self, *args, **kwargs):
        pass

class pt5(Macro):
    """Macro with a motor parameter followed by a list of numbers"""

    param_def = [
       [ 'motor', Type.Motor, None, 'Motor to move'],
       [ 'numb_list', [ [ 'pos', Type.Float, None, 'value'] ], None, 'List of values'],
    ]
    
    def run(self, *args, **kwargs):
        pass

class pt6(Macro):
    """Macro with a motor parameter followed by a list of numbers. The list as
    explicitly stated an optional last element which is a dictionary that defines the
    min and max values for repetitions"""

    param_def = [
       [ 'motor', Type.Motor, None, 'Motor to move'],
       [ 'numb_list', [ [ 'pos', Type.Float, None, 'value'], { 'min' : 1, 'max' : None } ], None, 'List of values'],
    ]
    
    def run(self, *args, **kwargs):
        pass
    
class pt7(Macro):
    """Macro with a list of pair Motor,Float"""

    param_def = [
       [ 'm_p_pair', [ [ 'motor', Type.Motor, None, 'Motor to move'],
                       [ 'pos',   Type.Float, None, 'Position to move to'] ],
         None, 'List of motor/position pairs']
    ]
    
    def run(self, *args, **kwargs):
        pass

class pt8(Macro):
    """Macro with a list of pair Motor,Float. The min and max elements have been
    explicitly stated"""
    
    param_def = [
       [ 'm_p_pair', [ [ 'motor', Type.Motor, None, 'Motor to move'],
                       [ 'pos',   Type.Float, None, 'Position to move to'],
                       { 'min' : 1, 'max' : 2 } ],
         None, 'List of motor/position pairs']
    ]
    
    def run(self, *args, **kwargs):
        pass

class pt9(Macro):
    """Same as macro pt7 but with old style ParamRepeat. If you are writing
    a macro with variable number of parameters for the first time don't even
    bother to look at this example since it is DEPRECATED."""

    param_def = [
       ['m_p_pair',
        ParamRepeat(['motor', Type.Motor, None, 'Motor to move'],
                    ['pos',  Type.Float, None, 'Position to move to'], min=1, max= 2),
        None, 'List of motor/position pairs'],
    ]
    
    def run(self, *args, **kwargs):
        pass

class pt10(Macro):
    """Macro with list of numbers followed by a motor parameter. The repeat
    parameter may be defined as first one."""

    param_def = [
       ['numb_list', [['pos', Type.Float, None, 'value']], None, 'List of values'],
       ['motor', Type.Motor, None, 'Motor to move']
    ]

    def run(self, *args, **kwargs):
        pass


class pt11(Macro):
    """Macro with list of numbers followed by a motor parameter. The repeat
    parameter may be defined as first one."""

    param_def = [
       ['counter', Type.ExpChannel, None, 'Counter to count'],
       ['numb_list', [['pos', Type.Float, None, 'value']], None, 'List of values'],
       ['motor', Type.Motor, None, 'Motor to move']
    ]

    def run(self, *args, **kwargs):
        pass


class pt12(Macro):
    """Macro with list of motors followed by list of numbers. Two repeat
    parameters may defined."""

    param_def = [
       ['numb_list', [['pos', Type.Float, None, 'value']], None, 'List of values'],
       ['motor_list', [['motor', Type.Motor, None, 'Motor to move']], None, 'List of motors']
    ]

    def run(self, *args, **kwargs):
        pass


class pt13(Macro):
    """Macro with list of motors groups, where each motor group is a list of 
    motors. Repeat parameters may be defined as nested."""

    param_def = [
       ['motor_group_list',
        [['motor_list', [['motor', Type.Motor, None, 'Motor to move']], None, 'List of motors']],
        None, 'Motor groups']
    ]

    def run(self, *args, **kwargs):
        pass


class twice(Macro):
    """A macro that returns a float that is twice its input. It also sets its 
    data to be a dictionary with 'in','out' as keys and value,result 
    as values, respectively"""

    # uncomment the following lines as necessary. Otherwise you may delete them
    param_def = [ [ "value", Type.Float, 23, "value to be doubled" ] ]
    result_def = [ [ "result", Type.Float, None, "the double of the given value" ] ]
    #hints = {}
    #env = (,)
    
    # uncomment the following lines if need prepare. Otherwise you may delete them
    #def prepare(self):
    #    pass
        
    def run(self, n):
        ret = 2*n
        self.setData({'in':n, 'out':ret})
        return ret
