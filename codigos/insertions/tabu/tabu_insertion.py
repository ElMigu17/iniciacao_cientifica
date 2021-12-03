from colorama.ansi import Back, Fore, Style
from basic_insertion import Basic_insertion
from structures import Vehicle, Node


class Tabu_insertion(Basic_insertion):
	def __init__(self, restrictions, objective_function, tabu_set):
		super().__init__(restrictions, objective_function)
		self.tabu_set = tabu_set
    

	def vehicle_inserted(self, graph, request):
		best_vehicle_to_insert = None
		best_rd = None
		for vehicle in graph.get_vehicles():
			vehicle_insert_forward, vehicle_insert_backward = super().insert_forward_and_backward(vehicle, request)
			best_vehicle_to_insert, best_rd = super().compare(vehicle_insert_forward, vehicle_insert_backward, vehicle, best_vehicle_to_insert, best_rd)

		if best_vehicle_to_insert is not None:
			graph.get_vehicles()[best_vehicle_to_insert.get_id()] = best_vehicle_to_insert
			return best_vehicle_to_insert
		return None

	#overriding
	def insert_request(self, vehicle, request, is_forward):
		vehicle_copy = vehicle.copy()

		new_nodes, start, end = super().insertion_data(request, vehicle, is_forward)

		if type(request) == Node:
			vehicle_copy, last_insertion = super().insert_in_best_position(vehicle_copy, start, new_nodes, end, is_forward)
			if vehicle_copy is not None:
				if request.is_pick_up():
					vehicle_copy.pu_last_inserted = last_insertion
				else:
					vehicle_copy.de_last_inserted = last_insertion
				
			return vehicle_copy
		
		else:
			vehicle_copy, last_insertion_1 = super().insert_in_best_position(vehicle_copy, start, new_nodes[0], end, is_forward)
			if vehicle_copy != None:
				vehicle_copy, last_insertion_2 = super().insert_in_best_position(vehicle_copy, last_insertion_1, new_nodes[1], end, is_forward)
				if vehicle_copy != None:
					if new_nodes[0].is_pick_up():
						vehicle_copy.pu_last_inserted = last_insertion_1
						vehicle_copy.de_last_inserted = last_insertion_2
					else:
						vehicle_copy.pu_last_inserted = last_insertion_2
						vehicle_copy.de_last_inserted = last_insertion_1
					return vehicle_copy
			return None

	#overriding
	def is_route_viably(self, candidate_route, insertion_pos):
		if not self.in_tabu_set(candidate_route, insertion_pos):
			return super().is_route_viably(candidate_route, insertion_pos)
		return False

	def in_tabu_set(self, route, pos):
		node_id = route.get_order()[pos].get_id()
		route_id = route.get_id()
		tabu_item = self.make_tabu_item( route_id, node_id, pos)

		if len(self.tabu_set) == 0:
			return False

		elif tabu_item in self.tabu_set:
			return True

		return False

	def make_tabu_item(self, vehicle_id, node_id, node_pos):
		return "(" + str(vehicle_id) + "," + str(node_id) + "," + str(node_pos) + ")"
