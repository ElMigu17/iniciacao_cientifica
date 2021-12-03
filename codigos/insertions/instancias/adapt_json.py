import json
import sys
import random

sys.path.append("..")
sys.path.append("../insertions")
sys.path.append("useful")
sys.path.append("instancias")

class Adapter:
    def __init__(self, randomise):
        self.randomise = randomise

    def adapt(self, input_json, qtd):
        with open(input_json) as f:
            en = list(json.load(f).items())

        distance_matrix = self.create_matrix(en[3][1])
        time_matrix = self.create_matrix(en[4][1])
        capacity = en[5][1]
        time_horizon = en[10][1]

        if self.randomise:
            new_request = self.rand_generate_request(en)
        else:
            new_request = self.generate_request(en)
        vehicles = self.generate_empty_vehicles(qtd, time_horizon, capacity)

        output = {
            "entrace": [{
            "graph": {
                "additional_info": {"edges_distances": distance_matrix, "edges_time": time_matrix},
                "new_requests": new_request,
                "vehicles": vehicles
                }
            }
            ]
            }
        json_object = json.dumps(output, indent = 4)

        with open("../useful/inputs.json", "w") as outfile:
            outfile.write(json_object)

    def generate_empty_vehicles(self, qtd, time_horizon, capacity):
        vehicles = []
        for i in range(qtd):
            vehicles.append({
                        "id": i,
                        "order": [
                            {
                                "id": 0,
                                "delivery": None, 
                                "pick_up": None,
                                "restriction_info":{
                                    "start_tw": 0,
                                    "end_tw": 0,
                                    "service_time": 0,
                                    "begin_service": 0,
                                    "package_size":0
                                }

                            }
                        ],
                        "pos_last_visited": 0,
                        "restriction_info":{
                            "time_horizon": time_horizon,
                            "capacity":capacity
                        }
                    })
        return vehicles

    def create_matrix(self, matrix):
        output_matrix = []
        i = 0
        while i < len(matrix):
            output_row = []
            j = 0
            while j < len(matrix[str(i)]):
                output_row.append(matrix[str(i)][str(j)])
                j += 1
            output_matrix.append(output_row)
            i += 1
        return output_matrix

    def generate_request(self, en):
        pickup_delivery = en[6][1]
        
        i = 0
        saida = []
        for a in pickup_delivery:

            saida.append({
                        "pick_up":{
                            "id": a[0],
                            "delivery": a[1], 
                            "pick_up": None,
                            "restriction_info":{
                                "start_tw": en[9][1][str(a[0])][0],
                                "end_tw": en[9][1][str(a[0])][1],
                                "service_time": en[8][1][str(a[0])],
                                "begin_service": -1,
                                "package_size": en[7][1][str(a[0])]
                            }
                        },
                        "delivery":{
                            "id": a[1],
                            "delivery": None, 
                            "pick_up": a[0],
                            "restriction_info":{
                                "start_tw": en[9][1][str(a[1])][0],
                                "end_tw": en[9][1][str(a[1])][1],
                                "service_time": en[8][1][str(a[1])],
                                "begin_service": -1,
                                "package_size": en[7][1][str(a[1])]
                            }
                        }

                    })
            i += 1
        return saida

    def rand_generate_request(self, en):
        pickup_delivery = en[6][1]
        
        i = 0
        saida = []
        for a in pickup_delivery:
            if random.randrange( 1, 100) < 70:
                saida.append({
                            "pick_up":{
                                "id": a[0],
                                "delivery": a[1], 
                                "pick_up": None,
                                "restriction_info":{
                                    "start_tw": en[9][1][str(a[0])][0],
                                    "end_tw": en[9][1][str(a[0])][1],
                                    "service_time": en[8][1][str(a[0])],
                                    "begin_service": -1,
                                    "package_size": en[7][1][str(a[0])]
                                }
                            },
                            "delivery":{
                                "id": a[1],
                                "delivery": None, 
                                "pick_up": a[0],
                                "restriction_info":{
                                    "start_tw": en[9][1][str(a[1])][0],
                                    "end_tw": en[9][1][str(a[1])][1],
                                    "service_time": en[8][1][str(a[1])],
                                    "begin_service": -1,
                                    "package_size": en[7][1][str(a[1])]
                                }
                            }

                        })
            else:
                saida.append(
                    {
                        "pick_up":{
                            "id": a[0],
                            "delivery": 0, 
                            "pick_up": None,
                            "restriction_info":{
                                "start_tw": en[9][1][str(a[0])][0],
                                "end_tw": en[9][1][str(a[0])][1],
                                "service_time": en[8][1][str(a[0])],
                                "begin_service": -1,
                                "package_size": en[7][1][str(a[0])]
                            }
                        }
                    }
                )
                saida.append(
                    {
                        "delivery":{
                            "id": a[1],
                            "delivery": None, 
                            "pick_up": 0,
                            "restriction_info":{
                                "start_tw": en[9][1][str(a[1])][0],
                                "end_tw": en[9][1][str(a[1])][1],
                                "service_time": en[8][1][str(a[1])],
                                "begin_service": -1,
                                "package_size": en[7][1][str(a[1])]
                            }
                        }
                    }
                )
            i += 1
        return saida


def get_randomise(arguments):
    try:
        choice = arguments[2]
        if choice == "T":
            return True
        elif choice == "F":
            return False
        else:
            raise ValueError("Must have second argument as T or F")
    except(IndexError):
        raise IndexError

def get_qtd_nodes(arguments, qtds_vehicle):
    try:
        qtd_nodes = int(arguments[1])
        if qtds_vehicle.get(qtd_nodes) == None:
            possible_choices = str(qtds_vehicle.keys())
            possible_choices = possible_choices.split("[")[1].split("]")[0]
            raise ValueError("The first argument value must be one of these: " + possible_choices)
        return int(qtd_nodes)

    except(IndexError):
        raise IndexError
  


if __name__ == "__main__":
    qtds_vehicle = { 10: 4, 200: 24, 300: 30, 400: 43}
    random_choice = {True: "random", False: "not random"}

    try:
        qtd_nodes = get_qtd_nodes(sys.argv, qtds_vehicle)
        randomise = get_randomise(sys.argv)
    except IndexError as erro:
        print(str(erro) + "This program must have two argument: one of these numbers: " + str(qtds_vehicle.keys()).split("[")[1].split("]")[0] +" and F or T")
    except ValueError as erro:
        print("ValueErro:\n     "+str(erro))

      
    else:
        adapt_machine = Adapter(randomise)
        print("Your choices was", qtd_nodes, "and", random_choice[randomise])
        adapt_machine.adapt("br-mg-bh-"+str(qtd_nodes)+"_input.json", qtds_vehicle[qtd_nodes])
