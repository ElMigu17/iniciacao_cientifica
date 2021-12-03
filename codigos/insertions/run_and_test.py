import sys
from typing import Awaitable

sys.path.append("..")
sys.path.append("../improvment")
sys.path.append("useful")
sys.path.append("simple")
sys.path.append("nfr")
sys.path.append("nfl")
sys.path.append("tabu")
sys.path.append("random_insertion")
from structures import Request
from simple_insertion import Simple_insertion as simple_insertion
from non_fixed_request import Non_fixed_request as non_fixed_request
from non_fixed_location import Non_fixed_location as non_fixed_location
from random_insertion import Random_insertion as random_insertion

from remove_requests import Remove_requests as remove_requests
from tabu_search import Tabu_search 
import time

from objective_function import  Objective_function_imp
from restriction import (Time_window, Distance, Capacity)
from tests import Test
from get_inputs import Get_inputs 

#verificar inserção dinamica pra ver se n coloca nada incorreto com relação ao tempo atual a

class Run_and_test():

    def main(self, input_json, choice):
        self.time_dinamic = 150
        get_inputs = Get_inputs()
        chosed_insertion = self.build_insertion(choice)
        print("Getting inputs")
        solution = get_inputs.get_inputs(input_json)

        self.run_test(solution)

        self.insert_half_randomly(solution)
        self.run_test(solution)
        self.improve_solution(solution)
        self.run_test(solution)

        self.insert_all_dynamically(solution, chosed_insertion)
        self.improve_solution(solution)

    def build_insertion(self, choice):

        def make_string(choices_function):
            str_values_choices_function = str(choices_function.values()).split('\'')
            str_keys_choices_function = str(choices_function.keys()).split('\'')
            i = 1
            out = ""
            while i < len(str_values_choices_function):
                function_name = str_values_choices_function[i].split(".")[0]
                out += "\n" +str_keys_choices_function[i] + " to chose " + function_name
                i += 2
            return out

        restrictions = []
        restrictions.append(Time_window())
        restrictions.append(Distance())
        restrictions.append(Capacity())
        objective_function = Objective_function_imp()
        choices_function = {'r': non_fixed_request, 'l': non_fixed_location, 'm': random_insertion, 's': simple_insertion}

        if choices_function.get(choice) is None:
            possible_choices = make_string(choices_function)
            raise ValueError("This program must have one argument, which must be one of these: " + possible_choices)


        print("Built", str(choices_function[choice]).split("\'")[1].split(".")[0])
        return choices_function[choice](restrictions, objective_function)

    def insert_half_randomly(self, solution):
        insertion_random = self.build_insertion("m")
        all_requests = solution.get_new_requests()
        part1, part2 = self.split_array(all_requests, int(len(all_requests)/2))
        solution.set_new_requests(part1) 

        print("    running random insertion")
        insertion_random.insert(solution)

        solution.set_new_requests(part2) 
        
    def insert_all_dynamically(self, solution, insertion):

        self.update_time(solution, 150)
        print("    running dynamic insertion")
        insertion.insert(solution)
        print("    finished dynamic insertion")

        self.run_test(solution)

        print("    requests not inserted:", solution.get_new_requests())

    def split_array(self, array, limit):
        part1 = []
        part2 = []
        tam = len(array)
        i = 0

        while i < tam and len(part2) < tam/2:
            node = array[i]
            if type(array[i]) is Request:
                node = node.get_pick_up()
            
            if node.get_restriction_info()["end_tw"] <= self.time_dinamic:
                part1.append(array[i])
            else:
                part2.append(array[i])
            i += 1

        while i<tam:
            part1.append(array[i])
            i += 1 


        return part1, part2

    def update_time(self, solution, time_now):

        print("Updating solution time to", time_now)

        def begin_service(order, pos):
            return order[pos].get_restriction_info()["begin_service"]

        def path_time(order, v, pos):
            return time_matrix[order[pos].get_id()][v.next(pos)]

        time_matrix = solution.get_additional_info()["edges_time"]

        i = 0
        while i < len(solution.get_new_requests()):
            new_requests = solution.get_new_requests()
            node_to_analise = None
            if type(new_requests[i]) is Request:
                node_to_analise = new_requests[i].get_pick_up()
            else:
                node_to_analise = new_requests[i]

            if node_to_analise.get_restriction_info()["end_tw"] < self.time_dinamic:
                node = new_requests.pop(i)            
                if type(node) is Request:
                    node = node.get_pick_up()
            
                if node.get_restriction_info()["end_tw"] < self.time_dinamic:
                    print(node.id())
                print("popped")
            else:
                i += 1
        
        for v in solution.get_vehicles():
            new_pos_last_visited = 0
            i = 0
            order = v.get_order()
            tam = len(order)

            while i < tam and (begin_service(order, i) + path_time(order, v, i) < time_now):
                new_pos_last_visited = i
                i += 1

            print(v.get_id(), ":", new_pos_last_visited)
            v.set_pos_last_visited(new_pos_last_visited)

    def improve_solution(self, solution):
        
        print("    running improvment")
        start = time.time()

        tabu = Tabu_search()
        tabu.tabu_move(solution)
        
        print("    finished improvment")
        print("        time took to improve:", time.time() - start)

        print("    requests not inserted at solution ",solution.get_new_requests())
        self.run_test(solution)

    def run_test(self, solution):
        print("    testing")
        test = Test(solution)
        test.main()

if __name__ == "__main__":
    run_and_test = Run_and_test()
    if 1 == len(sys.argv):
        run_and_test.main("useful/inputs.json", "a")
    else:
        run_and_test.main("useful/inputs.json", sys.argv[1])
        
