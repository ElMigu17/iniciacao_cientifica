from abc import ABC, abstractclassmethod, abstractmethod

class Objective_function(ABC):

	@abstractmethod
	def best_order(current_best_order, candidate_order, additional_info):
		pass

	@abstractmethod
	def objective_diferences(self, vehicle, new_vehicle, additional_info):
		pass
	
	@abstractmethod
	def best_diferences(self, best_diferences, restrictions_diferences):
		pass

	@abstractmethod
	def solution_value(self, solution):
		pass
	
	@abstractmethod
	def best_solution_value(self, solution):
		pass


class Objective_function_imp(Objective_function):
	def best_order(self, route1, route2, additional_info):
		if route1 is None and route2 is None:
			return None
		elif route1 is None and route2 is not None:
			return route2
		elif route2 is None and route1 is not None:
			return route1
		
		edges_time = additional_info["edges_time"]
		total_time_route1 = route1.total_edges(edges_time)
		total_time_route2 = route2.total_edges(edges_time)
		
		if total_time_route1 < total_time_route2:
			return route1
		elif total_time_route1 > total_time_route2:
			return route2
		else:
			edges_distance = additional_info["edges_distances"]
			total_distance_route1 = route1.total_edges(edges_distance)
			total_distance_route2 = route2.total_edges(edges_distance)				
			if total_distance_route1 < total_distance_route2:
				return route1
			elif total_distance_route1 >= total_distance_route2:
				return route2

	def objective_diferences(self, vehicle, new_vehicle, additional_info):
		edges_time = additional_info["edges_time"]
		edges_distance = additional_info["edges_distances"]

		time_diference = new_vehicle.total_edges(edges_time) - vehicle.total_edges(edges_time)
		distance_diference = new_vehicle.total_edges(edges_distance) - vehicle.total_edges(edges_distance)
				
		return {"time_diference": time_diference, "distance_diference": distance_diference}

	def best_diferences(self, best_diferences, new_diferences):
		if best_diferences["time_diference"] > new_diferences["time_diference"]:
			return new_diferences
		elif best_diferences["time_diference"] < new_diferences["time_diference"]:
			return best_diferences
		else:
			if best_diferences["distance_diference"] > new_diferences["distance_diference"]:
				return new_diferences
			elif best_diferences["distance_diference"] <= new_diferences["distance_diference"]:
				return best_diferences
	
	def solution_value(self, solution):
		solution_time = 0
		solution_distance = 0 
		for v in solution.get_vehicles():
			solution_time += v.total_edges(solution.get_additional_info()["edges_time"])
			solution_distance += v.total_edges(solution.get_additional_info()["edges_distances"])
		return {"time": solution_time, "distance" : solution_distance}

	def best_solution_value(self, value_solution1, value_solution2):
		if value_solution1["time"] < value_solution2["time"]:
			return value_solution1
		elif value_solution1["time"] > value_solution2["time"]:
			return value_solution2
		
		if value_solution1["distance"] < value_solution2["distance"]:
			return value_solution1
		elif value_solution1["distance"] > value_solution2["distance"]:
			return value_solution2
		
		