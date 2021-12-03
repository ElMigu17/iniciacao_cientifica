from basic_insertion import Basic_insertion
from simple_insertion import Simple_insertion
from remove_requests import Remove_requests
from colorama import Fore, Back, Style

class Non_fixed_location(Basic_insertion):
	def __init__(self, restrictions, objective_function):
		super().__init__(restrictions, objective_function)
		self._simple_insertion = Simple_insertion(restrictions, objective_function)

	#override
	def insert(self, graph):
		remover = Remove_requests()
		remover.new_orders(graph)
		self._simple_insertion.additional_info = graph.get_additional_info()
		self.complements = self.remove_after_last_visited(graph)

		self.verify_viability(graph)

		super().insert(graph)
		self.insert_complements(graph)

	def verify_viability(self, graph):
		bi = Basic_insertion(self._restrictions, self._objective_function)
		bi.additional_info = graph.get_additional_info()

		for v in graph.get_vehicles():
			if not bi.is_route_viably(v, 0):
				raise ValueError ("route is not viably")
		
	def insert_complements(self, graph):
		tam = len(graph.get_vehicles())
		
		for i in range(tam):
			if self.complements[i] == []:
				continue

			for complement in self.complements[i]:
				new_vehicle = self.insert_one_complement(graph.get_vehicles()[i], complement)
				
				if new_vehicle is not None:
					graph.get_vehicles()[i] = new_vehicle
				

				
	def insert_one_complement(self, vehicle, complement):
		forward, backard = self._simple_insertion.insert_forward_and_backward(vehicle, complement)
		best_order = self._objective_function.best_order(forward, backard, self._simple_insertion.additional_info)
		 
		if best_order is not None and best_order is not vehicle:
			return best_order
		return None
				
	def remove_after_last_visited(self, graph):
		all_removed = []
		for v in graph.get_vehicles():
			removed_in_one_vehicle = []
			i = v.get_pos_last_visited() + 1
			while i < len(v.get_order()):
				removed_in_one_vehicle.append(v.get_order().pop(i))
			all_removed.append(removed_in_one_vehicle)
		return all_removed
	
	#override
	def is_route_viably(self, candidate_route, insertion_pos):
		for restriction in self._restrictions:
			if not restriction.aply_restrition(candidate_route, insertion_pos, self.additional_info):
				return False
		return self.is_possibly_to_insert_complements(candidate_route)

	def is_possibly_to_insert_complements(self, vehicle):
		vehicle_copy = vehicle.copy()
		for complement in self.complements[vehicle.get_id()]:
			vehicle_copy = self.insert_one_complement(vehicle_copy, complement)
			if vehicle_copy is None:
				return False
		return True

	def try_to_insert_complement(self, vehicle, new_node):
		end_not_found = True
		end = len(vehicle.get_order())

		insertion_pos = vehicle.get_pos_last_visited() + 1

		while end_not_found:
			candidate_route = vehicle.copy()
			candidate_route.get_order().insert(insertion_pos, new_node.copy())

			if self._simple_insertion.is_route_viably(candidate_route, insertion_pos) :
				return True

			insertion_pos = candidate_route.next(insertion_pos)

			if insertion_pos == end:
				end_not_found = False
		return False