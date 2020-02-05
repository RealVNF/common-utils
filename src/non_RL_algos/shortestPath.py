import argparse
from collections import defaultdict
import logging
import os
import random
from datetime import datetime
from spinterface import SimulatorAction
from common.common_functionalities import normalize_scheduling_probabilities, create_input_file
from siminterface.simulator import Simulator
from shutil import copyfile
from pathlib import Path

log = logging.getLogger(__name__)
DATETIME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def copy_input_files(target_dir, network_path, service_path, sim_config_path):
    """Create the results directory and copy input files"""
    new_network_path = f"{target_dir}/{os.path.basename(network_path)}"
    new_service_path = f"{target_dir}/{os.path.basename(service_path)}"
    new_sim_config_path = f"{target_dir}/{os.path.basename(sim_config_path)}"

    os.makedirs(target_dir, exist_ok=True)
    copyfile(network_path, new_network_path)
    copyfile(service_path, new_service_path)
    copyfile(sim_config_path, new_sim_config_path)


def get_ingress_nodes_and_cap(network):
    """
    Gets a NetworkX DiGraph and returns a list of ingress nodes in the network and the largest capacity of nodes
    Parameters:
        network: NetworkX Digraph
    Returns:
        ing_nodes : a list of Ingress nodes in the Network
        node_cap : the single largest capacity of all the nodes of the network
    """
    ing_nodes = []
    node_cap = {}
    for node in network.nodes(data=True):
        node_cap[node[0]] = node[1]['cap']
        if node[1]["type"] == "Ingress":
            ing_nodes.append(node[0])
    return ing_nodes, node_cap


def get_project_root():
    """Returns project's root folder."""
    return str(Path(__file__).parent.parent.parent)


def next_neighbour(index, num_vnfs_filled, node, placement, closest_neighbours, sf_list, nodes_cap, ingress_nodes):
    while len(placement[closest_neighbours[node][index]]) > num_vnfs_filled[0] or \
            nodes_cap[closest_neighbours[node][index]] == 0:
        index += 1
        if index == len(closest_neighbours[node]):
            num_vnfs_filled[0] += 1
            index = 0
        if num_vnfs_filled[0] > len(sf_list):
            index = 0
            break
    return index


def get_placement_schedule(network, nodes_list, sf_list, sfc_list, ingress_nodes, nodes_cap):
    """
        '''
        Schedule is of the following form:
            schedule : dict
                {
                    'node id' : dict
                    {
                        'SFC id' : dict
                        {
                            'SF id' : dict
                            {
                                'node id' : float (Inclusive of zero values)
                            }
                        }
                    }
                }
        '''

    Parameters:
        network
        nodes_list
        sf_list
        sfc_list
        ingress_nodes
        nodes_cap

    Returns:
        - a placement Dictionary with:
              key = nodes of the network
              value = list of all the SFs in the network
        - schedule of the form shown above
    """
    placement = defaultdict(list)
    schedule = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(float))))
    for src in nodes_list:
        for sfc in sfc_list:
            for sf in sf_list:
                for dstn in nodes_list:
                    schedule[src][sfc][sf][dstn] = 0
    all_pair_shortest_paths = network.graph['shortest_paths']
    closest_neighbours = defaultdict(list)
    for source in nodes_list:
        neighbours = defaultdict(int)
        for dest in nodes_list:
            if source != dest:
                delay = all_pair_shortest_paths[(source, dest)][1]
                neighbours[dest] = delay
        sorted_neighbours = [k for k, v in sorted(neighbours.items(), key=lambda item: item[1])]
        closest_neighbours[source] = sorted_neighbours

    for ingress in ingress_nodes:
        node = ingress
        num_vnfs_filled = [0]
        # Placing the 1st VNF of the SFC on the ingress nodes if the ingress node has some capacity
        # Otherwise we find the closest neighbour of the Ingress that has some capacity and place the 1st VNF on it
        if nodes_cap[ingress] > 0:
            if sf_list[0] not in placement[node]:
                placement[node].append(sf_list[0])
            schedule[node][sfc_list[0]][sf_list[0]][node] += 1
        else:
            # Finding the next neighbour which is not an ingress node and has some capacity
            index = next_neighbour(0, num_vnfs_filled, ingress, placement, closest_neighbours, sf_list, nodes_cap,
                                   ingress_nodes)
            while num_vnfs_filled[0] == 0 and closest_neighbours[ingress][index] in ingress_nodes:
                if index + 1 >= len(closest_neighbours[ingress]):
                    break
                index = next_neighbour(index + 1, num_vnfs_filled, ingress, placement, closest_neighbours,
                                       sf_list, nodes_cap, ingress_nodes)
            node = closest_neighbours[ingress][index]
            if sf_list[0] not in placement[node]:
                placement[node].append(sf_list[0])
            schedule[ingress][sfc_list[0]][sf_list[0]][node] += 1

        for j in range(len(sf_list)-1):
            index = next_neighbour(0, num_vnfs_filled, node, placement, closest_neighbours, sf_list, nodes_cap,
                                   ingress_nodes)
            while num_vnfs_filled[0] == 0 and closest_neighbours[node][index] in ingress_nodes:
                if index + 1 >= len(closest_neighbours[node]):
                    break
                index = next_neighbour(index + 1, num_vnfs_filled, node, placement, closest_neighbours,
                                       sf_list, nodes_cap, ingress_nodes)
            new_node = closest_neighbours[node][index]
            if sf_list[j+1] not in placement[new_node]:
                placement[new_node].append(sf_list[j+1])
            schedule[node][sfc_list[0]][sf_list[j+1]][new_node] += 1
            node = new_node

    for src in nodes_list:
        for sfc in sfc_list:
            for sf in sf_list:
                unnormalized_probs_list = list(schedule[src][sfc][sf].values())
                normalized_probs = normalize_scheduling_probabilities(unnormalized_probs_list)
                for i in range(len(nodes_list)):
                    schedule[src][sfc][sf][nodes_list[i]] = normalized_probs[i]
    return placement, schedule


def parse_args():
    parser = argparse.ArgumentParser(description="Load Balance Algorithm")
    parser.add_argument('-i', '--iterations', required=False, default=10, dest="iterations", type=int)
    parser.add_argument('-s', '--seed', required=False, dest="seed", type=int)
    parser.add_argument('-n', '--network', required=True, dest='network')
    parser.add_argument('-sf', '--service_functions', required=True, dest="service_functions")
    parser.add_argument('-c', '--config', required=True, dest="config")
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()
    if not args.seed:
        args.seed = random.randint(1, 9999)
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(filename="logs/{}_{}_{}.log".format(os.path.basename(args.network),
                                                            DATETIME, args.seed), level=logging.INFO)
    logging.getLogger("coordsim").setLevel(logging.WARNING)

    # Creating the results directory variable where the simulator result files will be written
    network_stem = os.path.splitext(os.path.basename(args.network))[0]
    service_function_stem = os.path.splitext(os.path.basename(args.service_functions))[0]
    simulator_config_stem = os.path.splitext(os.path.basename(args.config))[0]

    results_dir = f"{get_project_root()}/results/{network_stem}/{service_function_stem}/{simulator_config_stem}" \
                  f"/{DATETIME}_seed{args.seed}"

    # creating the simulator
    simulator = Simulator(os.path.abspath(args.network),
                          os.path.abspath(args.service_functions),
                          os.path.abspath(args.config), test_mode=True, test_dir=results_dir)
    init_state = simulator.init(args.seed)
    log.info("Network Stats after init(): %s", init_state.network_stats)
    nodes_list = [node['id'] for node in init_state.network.get('nodes')]
    sf_list = list(init_state.service_functions.keys())
    sfc_list = list(init_state.sfcs.keys())
    ingress_nodes, nodes_cap = get_ingress_nodes_and_cap(simulator.network)
    # getting the placement and schedule
    placement, schedule = get_placement_schedule(simulator.network, nodes_list, sf_list, sfc_list, ingress_nodes,
                                                 nodes_cap)
    action = SimulatorAction(placement, schedule)
    # iterations define the number of time we wanna call apply()
    for i in range(args.iterations):
        apply_state = simulator.apply(action)
        log.info("Network Stats after apply() # %s: %s", i + 1, apply_state.network_stats)
    copy_input_files(results_dir, os.path.abspath(args.network), os.path.abspath(args.service_functions),
                     os.path.abspath(args.config))
    create_input_file(results_dir, len(ingress_nodes), "LoadBalance")


if __name__ == '__main__':
    main()
