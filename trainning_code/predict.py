import tensorflow as tf
import numpy as np
import networkx as nx
import logging, os
import operator, collections
import random
import re


totalNum = 34               #data set num
GreedyNum = 15                 #|S|
activated_node_set=[]   


with tf.Session() as sess:
    new_saver = tf.train.import_meta_graph('save/tensor_net.ckpt.meta')         #read model
    new_saver.restore(sess, "save/tensor_net.ckpt")
    greedy_node_set = []
    max = 1
    for x in range(GreedyNum):                                #NeuGreedy
        for m in range(1, totalNum + 1):
            if m not in greedy_node_set:
                greedy_node_set.append(m)
                activated_node_set = []
                for h in greedy_node_set:
                    activated_node_set.append(h)
                trainInput = [0 for x in range(0, totalNum)]
                trainOutput = [0 for x in range(0, totalNum)]
                trainOutput_double = [[]]
                for i in activated_node_set:
                    trainInput[i-1]=1

                graph = tf.get_default_graph()
                x = graph.get_operation_by_name('x').outputs[0]
                y = tf.get_collection("answer")[0]    
                keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]
                trainOutput_double.append( sess.run(y, feed_dict={x:[trainInput], keep_prob: 1.0}))
                trainOutput =trainOutput_double[1]                 #predit influence
                templength=0
                for ab in trainOutput:
                    for abc in ab:
                        if abc==1:
                            templength=templength+1
                if templength > max:
                    max = templength
                    greedynum_now = m
                    if greedy_node_set.count(m) > 1:
                        greedy_node_set.remove(m)
                        greedy_node_set.append(m)
                    else:
                        greedy_node_set.remove(m)
                elif templength <= max:
                    if greedy_node_set.count(m) > 1:
                        greedy_node_set.remove(m)
                        greedy_node_set.append(m)
                    else:
                        greedy_node_set.remove(m)
        greedy_node_set.append(greedynum_now)
        greedy_node_set = list(set(greedy_node_set))
        max = max
        print(greedy_node_set)
        print(max)





