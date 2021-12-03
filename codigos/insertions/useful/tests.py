import sys


class Test():
    def __init__(self, graph):
        self.graph = graph

    def main(self):
        self.write_in_output(self.graph)
        try:
            self.verify_vehicles(self.graph)
        except ValueError as err:
            print("ValueError at" + str(err))
            sys.exit()
        else:
            print("No exception raised")



    def verify_vehicles(self, g):
        j = 0
        try:
            for v in g.get_vehicles():
                self.verify_time_window(v.get_order())
                self.verify_capacity(v)
                self.verify_begging_service_order(v.get_order(), g.get_additional_info())
                self.correspond_all_pick_ups_to_deliverys(v.get_order())
                j += 1
        except ValueError as err:
            raise ValueError(" vehicle " + str(j) + "\n" + str(err))

    def verify_time_window(self, nodes):
        j = 0
        for nd in nodes:
            if (nd.get_restriction_info()["start_tw"] > nd.get_restriction_info()["begin_service"] 
            or nd.get_restriction_info()["end_tw"] < nd.get_restriction_info()["begin_service"]) and nd.get_restriction_info()["begin_service"] != -1:
                raise ValueError("Position " + str(j) + ", with node " + str(nd.get_id()) + " begging service is out of time window")
            j += 1

    def verify_capacity(self, vehicle):
        j = 0
        vehicle_capacity = vehicle.get_restriction_info()["capacity"]
        nodes = vehicle.get_order()
        for nd in nodes:
            if nd.get_restriction_info()["begin_service_capacity"] > vehicle_capacity or nd.get_restriction_info()["begin_service_capacity"] < 0:
                raise ValueError("Position " + str(j) + ", with node " + str(nd.get_id()) + " begging service capacity is out of capacity")
            j += 1

    def verify_begging_service_order(self, nodes, additional_info):
        j = 1
        travel_time_matrix = additional_info['edges_time']
        while j < len(nodes):
            previus_node = nodes[j-1]
            current_node = nodes[j]
            
            if previus_node.get_restriction_info()["begin_service"] + previus_node.get_restriction_info()["service_time"] + travel_time_matrix[previus_node.get_id()][current_node.get_id()] > current_node.get_restriction_info()["begin_service"]:
                raise ValueError("Pos " + str(j) + ", with node " + str(current_node.get_id()) + 
                " has its begging service out of order, as it can be seen: \n" + 
                str(j) + " begin_service: " + str(current_node.ri["begin_service"]) + "\n" + 
                str(j-1) + " begin_service + time_travel + edge_time: " + 
                str(previus_node.get_restriction_info()["begin_service"]) + " " + 
                str(previus_node.get_restriction_info()["service_time"]) + " " + 
                str(travel_time_matrix[current_node.get_id()][previus_node.get_id()]))

            if  previus_node.get_restriction_info()["begin_service_capacity"] + previus_node.get_restriction_info()["package_size"] > current_node.get_restriction_info()["begin_service_capacity"]:
                raise ValueError("Node " + str(j) + ", with node " + str(current_node.get_id()) + " has its capacity out of order, as it can be seen \n" + 
                str(j-1) + " begin_service_capacity + package_size: " + str(previus_node.get_restriction_info()["begin_service_capacity"]) + "+" + str(previus_node.get_restriction_info()["package_size"]) + "\n" + 
                str(j) + " begin_service_capacity: " + str(current_node.get_restriction_info()["begin_service_capacity"]))
            j += 1

    def correspond_all_pick_ups_to_deliverys(self, order):
        i = 1
        for i in range(len(order)):
            if order[i].get_pick_up() is None:
                j = i
                found_delivery = False

                if order[i].get_id() == 0 or order[i].get_delivery() == 0:
                    found_delivery = True
                while j < len(order) and not found_delivery:
                    if order[j].get_id() == order[i].get_delivery():
                        found_delivery = True
                    j += 1
                if not found_delivery:
                    raise ValueError("There is a delivery been made before the pickup or missing")

    def write_in_output(self, solution):
        f = open("output.txt", "a")
        
        f.write("solution vehicles:\n")

        for v in solution.get_vehicles():
            f.write("  " + str(v.get_id()) + ":\n")
            for n in v.get_order():
                f.write("    " + 
                str(n.get_id())+ ": " + 
                str(n.get_restriction_info()["start_tw"]) + " " + 
                str(n.get_restriction_info()["begin_service"]) + " " + 
                str(n.get_restriction_info()["end_tw"]) + " " + 
                str(n.get_restriction_info()["begin_service_capacity"]) + " " + 
                str(n.get_restriction_info()["package_size"]) + "\n")
            f.write("  " + str(v.total_edges(solution.get_additional_info()["edges_distances"])) + "\n")


        f.write("\nend----------------------------------------------------------------\n")


