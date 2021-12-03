from structures import Request
from restriction import (Time_window, Distance, Capacity)

from tests import Test
class Remove_requests():
	def __init__(self) -> None:
		pass

	def new_orders(self, solution):
		self.solution = solution
		for vehicle in solution.get_vehicles():
			removeble_requests = self.removeble_requests(vehicle)
			solution.add_requests(removeble_requests)


	def removeble_requests(self, vehicle):
		i = vehicle.pos_first_location()

		is_fixed = self.fixed_locations(i, vehicle)
		
		removeble_requests = self.select_non_fixed_requests(is_fixed, vehicle, i)


		return 	removeble_requests
		
	def fixed_locations(self, first_pos, vehicle):
		pos_last_visited = vehicle.get_pos_last_visited()
		i = first_pos
		is_fixed = [False]*len(vehicle.get_order())
		is_fixed[0] = True

		while i <= pos_last_visited:
			is_fixed[i] = True
			id_delivery = vehicle.get_order()[i].get_delivery()
			if  vehicle.get_order()[i].is_pick_up():
				is_fixed[vehicle.fast_node_pos(id_delivery, i)] = True
			i += 1
		
		return is_fixed

	def select_non_fixed_requests(self, is_fixed, vehicle, i):
		requests_selected = []
		qtd_locations = len(vehicle.get_order())

		while i < qtd_locations:
			if not is_fixed[i]:
				id_delivery = vehicle.get_order()[i].get_delivery()
				if vehicle.get_order()[i].get_pick_up() == 0:
					i += 1
					continue
				if vehicle.get_order()[i].is_pick_up() and self.delivery_is_not_depot(id_delivery):
					pos_delivery = vehicle.fast_node_pos(id_delivery, i)
					poped_delivery = vehicle.get_order().pop(pos_delivery)
					is_fixed.pop(pos_delivery)

					pair = Request(vehicle.get_order().pop(i), poped_delivery)
					is_fixed.pop(i)

					requests_selected.append(pair)
				else:
					aux = vehicle.get_order().pop(i)
					is_fixed.pop(i)
					requests_selected.append(aux)

				qtd_locations = len(vehicle.get_order())
			else:
				i += 1

		return requests_selected

	def delivery_is_not_depot(self, id_delivery):
		return id_delivery != 0