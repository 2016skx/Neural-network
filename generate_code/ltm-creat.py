import networkx as nx
import logging, os
import operator, collections
import random


class ltm:
    def __init__(self):
        self.dir_name = "input"
        self.file_name = "11.txt"  #data set/social network
        self.totalNum = 34         #node num
        self.trainNum = 10000     #training sample num
        self.nodesheld = {}

        self.edge_to_weight_dict = {}
        self.node_to_incoming_edge_dict = {}
        self.node_to_activation_count_dict = {}
        self.node_to_activated_nodes_set_dict = {}
        self.node_list = {}
        self.total_activated_nodes_set = set()
        self.top_nodes_with_activation_count = collections.OrderedDict()  

    def run_main(self):
        self.open_file()
        self.load_graph()
        self.close_file()
        self.pre_processing()
        self.train()

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
            for line in open("xxxx.txt",'r',encoding='utf-8'):                                      #read threshold
                if line.split(" ", 2)[0] == node:
                    nodesheld = line.split(" ", 2)[1].strip()
                    self.nodesheld[node] = nodesheld
                    break

    def train(self):
        list1 = []
        for m in range(0, self.trainNum):                            #Start generating training sample
            trainInput = [0 for x in range(0, self.totalNum)]        #Input vector
            self.activated_node_set = []
            seedsetNum = random.randint(2, 5)          #|S|=(2,mim(self.totalNum/6,15)
            print(seedsetNum)
            self.activated_node_neighbour = []

            for i in range(seedsetNum):
                self.activated_node_set.append(str(random.randint(1, self.totalNum )))  # a <= n <= b
                trainInput[int(self.activated_node_set[i]) - 1] = 1
            print(self.activated_node_set)


            f2 = open('xxxxxxx.txt', 'a', encoding='utf-8')               #training set input file
            for num in range(len(trainInput)):
                f2.write(str(trainInput[num]))
                f2.write(' ')
            f2.write('\r')
            f2.close()
            self.run()

    def run(self):
        tmp = 0
        trainOutput = [0 for x in range(0, self.totalNum)]
        length = len(self.activated_node_set)
        while length != tmp:
            length = len(self.activated_node_set)
            for node in self.activated_node_set:
                neighbors_list = self.G.neighbors(str(node))
                if len(neighbors_list) == 0:
                    continue
                for neighbor in neighbors_list:
                    if neighbor not in self.activated_node_set:
                        self.activated_node_neighbour.append(neighbor)
                self.activated_node_neighbour = list(set(self.activated_node_neighbour))
            for node in self.activated_node_neighbour:
                is_activated = self.check_if_is_activated(str(node))
                if is_activated and node not in self.activated_node_set and node not in self.total_activated_nodes_set:
                    self.activated_node_set.append(node)
            self.activated_node_set = list(set(self.activated_node_set))
            tmp = len(self.activated_node_set)

            self.node_to_activation_count_dict = {}
            self.node_to_activated_nodes_set_dict = {}
        self.post_processing()
        for i in self.activated_node_set:
            trainOutput[int(i)-1] = 1                                 #this data set start from node 1
        f3 = open('xxxxxxxx.txt', 'a', encoding='utf-8')              ##training set out file
        for num in range(len(trainOutput)):
            f3.write(str(trainOutput[num]))
            f3.write(' ')
        f3.write('\r')
        f3.close()

    def check_if_is_activated(self, node):                              #check a node if is activated
        total_edge_weight = 0
        total_edge = 0;
        incoming_edge_list = self.node_to_incoming_edge_dict.get(node)
        if not incoming_edge_list:
            return False
        for edge in incoming_edge_list:
            nodeNum = edge.encode('utf-8').decode('utf-8-sig').split("TO", 2)[0]
            if not node:
                continue
            if nodeNum in self.activated_node_set:
                edge_weight = float(1 / len(incoming_edge_list))
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
        print('#############################')



if __name__ == "__main__":
    ltm_obj = ltm()
    ltm_obj.run_main()
