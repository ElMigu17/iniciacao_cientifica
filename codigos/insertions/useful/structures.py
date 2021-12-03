class Node:
	def __init__(self, id, pick_up, delivery, restriction_info): #ri = restriction_info
		self._id = id
		self._pick_up = pick_up
		self._delivery = delivery
		self._restriction_info = restriction_info

	def get_id(self):
		return self._id

	def get_pick_up(self):
		return self._pick_up

	def get_delivery(self):
		return self._delivery

	def get_restriction_info(self):
		return self._restriction_info

	def is_pick_up(self):
		return self._pick_up is None

	def is_delivery(self):
		return self._delivery is None

	#non generic function
	def show(self):
		print("id:",self._id)
		if self._pick_up is not None:
			print("pick_up:", self._pick_up)
		if self._delivery is not None:
			print("delivery:", self._delivery)
		print("restriction_info:", self._restriction_info)

	def copy(self):
		return Node(self._id, self._pick_up, self._delivery, self._restriction_info.copy())

class Vehicle:
	def __init__(self, id, order, pos_last_visited, restriction_info):
		self._id = id
		self._order = order
		self._pos_last_visited = pos_last_visited
		self._restriction_info = restriction_info
		self.pu_last_inserted = None
		self.de_last_inserted = None

	def get_id(self):
		return self._id

	def get_order(self):
		return self._order

	def get_pos_last_visited(self):
		return self._pos_last_visited
	
	def set_pos_last_visited(self, post_last_visited):
		self._pos_last_visited = post_last_visited

	def get_restriction_info(self):
		return self._restriction_info

	#non generic function
	def show(self):
		print("id:", self.get_id())
		print("order:")
		for node in self.get_order():
			print(node)
			node.show()
		print("pos_last_visited:",self.get_pos_last_visited())
		print("restrition_info:", self.get_restriction_info())

	def copy(self):
		orders_copy = []
		for node in self._order:
			orders_copy.append(node.copy())
		vehicles_copy = Vehicle(self._id, orders_copy, self._pos_last_visited, self._restriction_info)
		vehicles_copy.pu_last_inserted = self.pu_last_inserted
		vehicles_copy.de_last_inserted = self.de_last_inserted
		return vehicles_copy

	def nodes_id_in_order(self):
		nodes = []
		for node in self._order:
			nodes.append(node.get_id())
		return nodes
			
	def next_forward_and_backward(self, current_pos, is_forward):
		if is_forward:
			if len(self._order)-1 == current_pos:
				return 0
			else:
				return current_pos+1
		else:
			if current_pos == 0:
				return len(self._order)-1
			else:
				return current_pos - 1

	def next(self, current_pos):
		if len(self._order)-1 == current_pos:
			return 0
		else:
			return current_pos+1

	def before(self, current_pos):
		if 0 == current_pos:
			return len(self._order)-1
		else:
			return current_pos-1

	def total_edges(self, matrix):
		total = 0
		i = 0
		for i in range(len(self._order)):
			node = self._order[i].get_id()
			if i != len(self._order)-1:
				next = self._order[i+1].get_id()
			else:
				next = 0
			total += matrix[node][next]
		return total

	def node_pos(self, id):
		return self.fast_node_pos(id, 0)
		
	def fast_node_pos(self, id, start):
		i = start
		order_size = len(self._order)
		for i in range(order_size):
			if self._order[i].get_id() == id:
				return i
		return None
	
	def pos_first_location(self):
		return 1

class Solution:
	def __init__(self, additional_info, new_requests, vehicles):
		self._additional_info = additional_info
		self._new_requests = new_requests
		self._vehicles = vehicles

	def get_additional_info(self):
		return self._additional_info

	def get_new_requests(self):
		return self._new_requests

	def get_vehicles(self):
		return self._vehicles

	def set_new_requests(self, requests):
		self._new_requests = requests

	def add_requests(self, additional_requests):
		self._new_requests += additional_requests

	def add_empty_vehicle(self):
		model_vehicle = self._vehicles[0]

		deposit_node = model_vehicle.get_order()[0].copy()
		restriction_info = model_vehicle.get_restriction_info().copy()
		self._vehicles.append(Vehicle(len(self._vehicles), [deposit_node], 0, restriction_info))

	def remove_last_vehicle(self):
		self._vehicles.pop()

	def qtd_avalible_requests(self):
		total = 0
		for v in self._vehicles:
			total += len(v.get_order()) - v.get_pos_last_visited()
		return total

	def copy(self):
		all_nr = []
		for nr in self._new_requests:
			all_nr.append(nr.copy())

		all_v = []
		for v in self._vehicles:
			all_v.append(v.copy())

		return Solution(self._additional_info.copy(), all_nr, all_v)

	#non generic function
	def show(self):
		print("additional_info:")
		for info in self._additional_info:
			print(info)
		print("new_requests:")
		i = 0
		for r in self._new_requests:
			print("request nº", i)
			r.show()
			i += 1
		print("vehicles:")
		for r in self._vehicles:
			r.show()


class Request:
	
	def __init__(self, *args):
		self._pick_up = args[0]
		self._delivery = args[1]
	
	def get_pick_up(self):
		return self._pick_up

	def get_delivery(self):
		return self._delivery

	def copy(self):
		copy_pick_up = self._pick_up.copy()
		copy_delivery = self._delivery.copy()
		return Request(copy_pick_up, copy_delivery)

	#non generic function
	def show(self):
		self._pick_up.show()
		self._delivery.show()

