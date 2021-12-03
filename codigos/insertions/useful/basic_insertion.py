"""
Codigo de simple insertion inspirado no código de simple insertion do Holborn, 2013 - Cap 6.4 Cap 3.4
Principal diferença: não há uso de minimo local, pois é necessário comparar
"""


#from colorama import Fore, Back, Style
from structures import (Request, Node) 

class Basic_insertion():
	def __init__(self, restrictions, objective_function):
		self._restrictions = restrictions
		self._objective_function = objective_function
		
	def insert(self, graph):
		self.additional_info = graph.get_additional_info() 

		i = 0
		copy_requests = graph.get_new_requests().copy()
		for request in copy_requests:
			if self.was_incerted_in_vehicle(graph, request):
				graph.get_new_requests().pop(i)
			else:
				i += 1

	def was_incerted_in_vehicle(self, graph, request):
		best_vehicle_to_insert = None
		best_rd = None

		for vehicle in graph.get_vehicles():
			vehicle_insert_forward, vehicle_insert_backward = self.insert_forward_and_backward(vehicle, request)
			best_vehicle_to_insert, best_rd = self.compare(vehicle_insert_forward, vehicle_insert_backward, vehicle, best_vehicle_to_insert, best_rd)

		if best_vehicle_to_insert != None:
			graph.get_vehicles()[best_vehicle_to_insert.get_id()] = best_vehicle_to_insert
			return True
		return False

	def insert_forward_and_backward(self, vehicle, new_request):
		vehicle_insert_forward = self.insert_request(vehicle, new_request, True)
		vehicle_insert_backward = self.insert_request(vehicle, new_request, False)
		return vehicle_insert_forward, vehicle_insert_backward

	def compare(self, vehicle_insert_forward, vehicle_insert_backward, original_vehicle, best_vehicle_to_insert, best_rd):
		vehicle_with_insertions = self._objective_function.best_order(vehicle_insert_forward, vehicle_insert_backward, self.additional_info) 
		
		if vehicle_with_insertions != None:
			new_rd = self._objective_function.objective_diferences(original_vehicle, vehicle_with_insertions, self.additional_info)
		
			if best_rd is None or new_rd == self._objective_function.best_diferences(best_rd, new_rd):
				return vehicle_with_insertions, new_rd
		
		return best_vehicle_to_insert, best_rd

	def insert_request(self, vehicle, request, is_forward):
		vehicle_copy = vehicle.copy()

		new_nodes, start, end = self.insertion_data(request, vehicle, is_forward)

		if type(request) == Node:
			vehicle_copy, last_insertion = self.insert_in_best_position(vehicle_copy, start, new_nodes, end, is_forward)
			return vehicle_copy
		else:
			vehicle_copy, last_insertion = self.insert_in_best_position(vehicle_copy, start, new_nodes[0], end, is_forward)
			if vehicle_copy != None:
				vehicle_copy, last_insertion = self.insert_in_best_position(vehicle_copy, last_insertion, new_nodes[1], end, is_forward)
				if vehicle_copy != None:
					return vehicle_copy
			return None

	def insertion_data(self, request, vehicle, is_forward):
		new_nodes = None
		if is_forward:
			if type(request) == Request:
				new_nodes = []
				new_nodes.append(request.get_pick_up().copy())
				new_nodes.append(request.get_delivery().copy())
			else:
				new_nodes = request.copy()
			start = vehicle.get_pos_last_visited()
			end = 0
		else:
			if type(request) == Request:
				new_nodes = []
				new_nodes.append(request.get_delivery().copy())
				new_nodes.append(request.get_pick_up().copy())
			else:
				new_nodes = request.copy()
			start = 0
			end = vehicle.get_pos_last_visited()
		return new_nodes, start, end

	def insert_in_best_position(self, vehicle, start, new_node, end, is_forward):
		best_route = None
		end_not_found = True
		best_insertion_pos = None

		insertion_pos = self.first_pos(start, vehicle.get_order(), is_forward)

		while end_not_found:
			candidate_route = vehicle.copy()
			candidate_route.get_order().insert(insertion_pos, new_node.copy())

			if ( self.is_route_viably(candidate_route, insertion_pos) and 
			(candidate_route == self._objective_function.best_order(best_route, candidate_route, self.additional_info)) ) : 
				best_route = candidate_route
				best_insertion_pos = insertion_pos
				
			insertion_pos = candidate_route.next_forward_and_backward(insertion_pos, is_forward)

			if insertion_pos == end:
				end_not_found = False
		return best_route, best_insertion_pos
		
	def is_route_viably(self, candidate_route, insertion_pos):
		for restriction in self._restrictions:
			if not restriction.aply_restrition(candidate_route, insertion_pos, self.additional_info):
				return False
		return True
	
	def first_pos(self, start, order, is_forward):
		if is_forward:
			return start + 1
		else:
			if start == 0:
				return len(order)
			else:
				return start
