"""
Codigo de simple insertion inspirado no código de simple insertion do Holborn, 2013 - Cap 6.4 Cap 3.4
Principal diferença: não há uso de minimo local, pois é necessário comparar
"""


#from colorama import Fore, Back, Style
from basic_insertion import Basic_insertion 

class Simple_insertion(Basic_insertion):
	def __init__(self, restrictions, objective_function):
		super().__init__(restrictions, objective_function)

