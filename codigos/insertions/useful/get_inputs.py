from structures import (Node, Vehicle, Solution, Request)
import json


class Get_inputs():           

    def get_inputs(self, input_json):
        with open(input_json) as f:
            en = list(json.load(f).items())

        en = en[0][1]
        data = en[0]

        graph = data['graph']
        vehicles = self.build_array_vehicles(graph['vehicles'])
        requests = self.build_array_request(graph['new_requests'])

        graph = Solution(graph["additional_info"], requests, vehicles)
        

        self.build_capacity(graph)
        return graph

    def build_array_vehicles(self, vehicles):
        these_vehicles = []

        for v in vehicles:
            nodes_in_vehicle = self.build_array_nodes(v['order'])
            these_vehicles.append(Vehicle(v['id'], nodes_in_vehicle, v['pos_last_visited'], v['restriction_info']))
        return these_vehicles

    def build_array_nodes(self, this_nodes):
        nodes_built = []
        
        for nd in this_nodes:
            nodes_built.append(Node(nd['id'], nd["pick_up"], nd["delivery"], nd['restriction_info']))
        return nodes_built

    def build_array_request(self, requests):
        these_requests = []
        for r in requests:
            a = self.dictionary_to_node_request(r) 
            these_requests.append(a)
        return these_requests

    def dictionary_to_node_request(self, r):
        a = []
        if "pick_up" in r:
            a.append(Node(r["pick_up"]["id"], r["pick_up"]["pick_up"], r["pick_up"]["delivery"], r["pick_up"]["restriction_info"]))
        if "delivery" in r:
            a.append(Node(r["delivery"]["id"], r["delivery"]["pick_up"], r["delivery"]["delivery"], r["delivery"]["restriction_info"]))
        if len(a) == 2:
            a = Request(a[0], a[1])
        else:
            a = a[0]
        return a

    #non generic function
    def build_capacity(self, graph):
        for v in graph.get_vehicles():
            total_now = 0
            for n in v.get_order():
                n.get_restriction_info()["begin_service_capacity"] = total_now
                if n.get_id() == 0:
                    total_now = 0
                else:
                    total_now += n.get_restriction_info()["package_size"]
