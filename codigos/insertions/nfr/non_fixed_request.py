from basic_insertion import Basic_insertion
from remove_requests import Remove_requests
from tests import Test

class Non_fixed_request(Basic_insertion):
	def __init__(self, restrictions, objective_function):
		super().__init__(restrictions, objective_function)

	#overriding
	def insert(self, graph):
		remover = Remove_requests()
		remover.new_orders(graph)
		self.verify_viability(graph)
		
		return super().insert(graph)

	def verify_viability(self, graph):
		bi = Basic_insertion(self._restrictions, self._objective_function)
		bi.additional_info = graph.get_additional_info()

		for v in graph.get_vehicles():
			if not bi.is_route_viably(v, 0):
				raise ValueError ("route is not viably")
		
