from abc import ABC, abstractclassmethod, abstractmethod

class Restriction(ABC):

	@abstractmethod
	def aply_restrition(self, vehicle, current_position, additional_info):
		pass



class Time_window(Restriction):


	def aply_restrition(self, vehicle, current_pos, additional_info):
		order = vehicle.get_order()
		pos_before = vehicle.before(current_pos)
		edges_time = additional_info["edges_time"]

		while pos_before != len(order)-1: 
			before = order[pos_before]
			current = order[current_pos]

			new_bs = before.get_restriction_info()["begin_service"] + before.get_restriction_info()["service_time"] + edges_time[before.get_id()][current.get_id()] # possivel novo tempo em que o serviço de entrega é iniciado

			if new_bs < current.get_restriction_info()["end_tw"]:
				if new_bs < current.get_restriction_info()["start_tw"]:
					current.get_restriction_info()["begin_service"] = current.get_restriction_info()["start_tw"]
				else:
					current.get_restriction_info()["begin_service"] = new_bs
			else: #se n deu tempo em um mais no inicio, n vai dar tempo mais pro fim, então para
				return False
			pos_before = current_pos
			current_pos = vehicle.next(current_pos)
		if order[-1].get_restriction_info()["service_time"] + order[-1].get_restriction_info()["begin_service"] + edges_time[order[0].get_id()][order[-1].get_id()] <= vehicle.get_restriction_info()["time_horizon"]:
			return True
		else:
			return False

class Distance(Restriction):


	def aply_restrition(self, vehicle, current_position, additional_info):
		return True

class Capacity(Restriction):

	def aply_restrition(self, vehicle, current_pos, additional_info):
		order = vehicle.get_order()
		pos_before = 0
		
		order[0].get_restriction_info()["package_size"] = 0

		for node in order:
			if node.get_pick_up() == 0:
				order[0].get_restriction_info()["package_size"] += -node.get_restriction_info()["package_size"]


		current_pos = 1

		while pos_before != len(order)-1: 
			before = order[pos_before]
			current = order[current_pos]

			new_bs = before.get_restriction_info()["begin_service_capacity"] + before.get_restriction_info()["package_size"] # possivel novo tempo em que o serviço de entrega é iniciado


			if new_bs < vehicle.get_restriction_info()["capacity"]:
				current.get_restriction_info()["begin_service_capacity"] = new_bs
			else: #se n deu tempo em um mais no inicio, n vai dar tempo mais pro fim, então para
				return False
			pos_before = current_pos
			current_pos = vehicle.next_forward_and_backward(current_pos, True)
		return True