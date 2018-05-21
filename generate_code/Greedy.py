import networkx as nx
import logging, os
import operator, collections
import random


class ltm:
    def __init__(self):
        self.dir_name = "input"
        self.file_name = "11.txt"
        self.totalNum = 34
        #self.NODE_THRESHOLD = 12
        self.GreedyNum=15

        self.nodesheld={}

        self.edge_to_weight_dict = {}
        self.node_to_incoming_edge_dict = {}
        self.node_to_activation_count_dict = {}
        self.node_to_activated_nodes_set_dict = {}
        self.node_list = {}
        self.total_activated_nodes_set = set()
        self.activated_node_set=[]
        self.top_nodes_with_activation_count = collections.OrderedDict()  # Final data structure which hold the results

    def run_main(self):
        self.open_file()
        self.load_graph()
        self.close_file()
        self.pre_processing()
        self.Greedy()

    def open_file(self):
        self.fd = open(os.path.join(self.dir_name, self.file_name), 'rb')

    def load_graph(self):
        self.G = nx.read_edgelist(self.fd, create_using=nx.DiGraph())
        self.nodes_list = self.G.nodes()

    def close_file(self):
        self.fd.close()

    def pre_processing(self):
        for node in self.nodes_list:
            if not node:
                continue
            neighbors_list = self.G.neighbors(node)
            if len(neighbors_list) == 0:
                continue
            for neighbor in neighbors_list:
                edge_name = node + "TO" + neighbor

                self.node_to_incoming_edge_dict.setdefault(neighbor, []).append(edge_name)
            for line in open("xxxxxxxx.txt",'r',encoding='utf-8'):  #threshold.txt
                if line.split(" ", 2)[0] == node:
                    nodesheld = line.split(" ", 2)[1].strip()
                    self.nodesheld[node] = nodesheld
                    break




    def Greedy(self):
        greedy_node_set = []

        max = 1
        for x in range(self.GreedyNum):
            for m in range(1, self.totalNum+1):
                if m not in greedy_node_set:
                    greedy_node_set.append(m)
                    self.activated_node_set=[]
                    for h in greedy_node_set:
                        self.activated_node_set.append(h)
                    templength = self.activated_count()
                    if templength > max:
                        max = templength
                        greedynum_now=m
                        if greedy_node_set.count(m)>1:
                            greedy_node_set.remove(m)
                            greedy_node_set.append(m)
                        else:
                            greedy_node_set.remove(m)
                    elif templength <= max:
                        if greedy_node_set.count(m)>1:
                            greedy_node_set.remove(m)
                            greedy_node_set.append(m)
                        else:
                            greedy_node_set.remove(m)
            greedy_node_set.append(greedynum_now)
            greedy_node_set=list(set(greedy_node_set))
            max=max
            print(greedy_node_set)
            print(max)





    def activated_count(self):
        tmp = 0
        self.activated_node_neighbour = []
        length = len(self.activated_node_set)
        while length != tmp:
            length = len(self.activated_node_set)
            for node in self.activated_node_set:
                neighbors_list = self.G.neighbors(str(node))
                if len(neighbors_list) == 0:
                    continue
                for neighbor in neighbors_list:
                    if int(neighbor) not in self.activated_node_set:
                        self.activated_node_neighbour.append(neighbor)
                self.activated_node_neighbour = list(set(self.activated_node_neighbour))
            for node in self.activated_node_neighbour:
                is_activated = self.check_if_is_activated(str(node))
                if is_activated and int(node) not in self.activated_node_set and node not in self.total_activated_nodes_set:
                    self.activated_node_set.append(int(node))
            self.activated_node_set = list(set(self.activated_node_set))

            tmp = len(self.activated_node_set)
        return tmp



    def check_if_is_activated(self, node):
        total_edge_weight = 0
        total_edge = 0;
        incoming_edge_list = self.node_to_incoming_edge_dict.get(node)
        if not incoming_edge_list:
            return False
        for edge in incoming_edge_list:
            nodeNum = edge.encode('utf-8').decode('utf-8-sig').split("TO", 2)[0]
            if not node:
                continue
            if int(nodeNum) in self.activated_node_set:
                edge_weight=float(1/len(incoming_edge_list))
                total_edge = total_edge + 1
                if not edge_weight:
                    continue
                total_edge_weight = float(edge_weight) + float(total_edge_weight)
        if float(total_edge_weight) > float(self.nodesheld[str(node)]):
            return True
        return False


    def post_processing(self):
        print(self.activated_node_set)
        print(len(self.activated_node_set))


if __name__ == "__main__":
    ltm_obj = ltm()
    ltm_obj.run_main()
