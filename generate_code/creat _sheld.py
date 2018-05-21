import networkx as nx
import logging, os
import operator, collections
import random

class ltm:

    def __init__(self):
        self.dir_name = "input"
        self.file_name = "11.txt"
        self.totalNum=34
        self.trainNum=10000
        self.shel=0.2
        self.NODE_THRESHOLD = 12
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

    def open_file(self):
        self.fd = open(os.path.join(self.dir_name, self.file_name), 'rb')

    def load_graph(self):
        self.G  = nx.read_edgelist(self.fd, create_using=nx.DiGraph())
        self.nodes_list = self.G.nodes()

    def close_file(self):
        self.fd.close()

    def pre_processing(self):
        f1 = open('xxxxxxxxxxxxxxxxx', 'w', encoding='utf-8')              #Generate a threshold for each node
        for node in self.nodes_list:
            if not node:
                continue
            nodesheld = round(random.uniform(0, 1),2)
            f1.write(node)
            f1.write(' ')
            f1.write(str(nodesheld))
            f1.write('\r\n')
        f1.close()


if __name__ == "__main__":
    ltm_obj = ltm()
    ltm_obj.run_main()
