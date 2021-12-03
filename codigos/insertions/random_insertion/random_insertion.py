from basic_insertion import Basic_insertion
from structures import Vehicle, Node
import random

class Random_insertion(Basic_insertion):
	def __init__(self, restrictions, objective_function):
		super().__init__(restrictions, objective_function)

	#overriding
	def insert(self, graph):		
		graph.set_new_requests( self.randomise_requests(graph.get_new_requests()) )

		super().insert(graph)


	def randomise_requests(self, requests):
		random_requests = []
		len_requests = len(requests)
		while len_requests != 0:
			i = random.randrange(0, len_requests)
			random_requests.append(requests.pop(i))
			len_requests = len(requests)
		return random_requests