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
    new_saver = tf.train.import_meta_graph('save/tensor_net.ckpt.meta')
    new_saver.restore(sess, "save/tensor_net.ckpt")
    f1 = open('xxxxxxx.txt', 'w', encoding='utf-8')
    greddy_node_set = []
    max = 1
  
    for x in range(GreddyNum):                                                            #NeuGreedy
        check = 0
        for m in range(1, totalNum+1 ):  # 
            if m not in greddy_node_set:
                greddy_node_set.append(m)
                activated_node_set = []
                for h in greddy_node_set:
                    activated_node_set.append(h)
                trainInput = [0 for x in range(0, totalNum)]
                trainOutput = [0 for x in range(0, totalNum)]
                trainOutput_double = [[]]
                for i in activated_node_set:
                    trainInput[i-1]=1

                graph = tf.get_default_graph()                                                          #use IPM to predict
                x = graph.get_operation_by_name('x').outputs[0]
                y = tf.get_collection("answer")[0]
                keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]
                trainOutput_double.append( sess.run(y, feed_dict={x:[trainInput], keep_prob: 1.0}))
                trainOutput =trainOutput_double[1]
                templength=0



                for ab in trainOutput:
                    for abc in ab:
                        if abc==1:
                            templength=templength+1         
                if templength > max:  
                    max = templength
                    greddynum_now = m
                    check=1
                    if greddy_node_set.count(m) > 1:
                        greddy_node_set.remove(m)
                        greddy_node_set.append(m)
                    else:
                        greddy_node_set.remove(m)
                elif templength <= max:
                    if greddy_node_set.count(m) > 1:
                        greddy_node_set.remove(m)
                        greddy_node_set.append(m)
                    else:
                        greddy_node_set.remove(m)



        if bool(check)==False:                                              
            trainInput = [0 for x in range(0, totalNum)]
            trainOutput = [0 for x in range(0, totalNum)]
            trainOutput_double = [[]]
            for i in activated_node_set:
                trainInput[i-1] = 1

            graph = tf.get_default_graph()
            x = graph.get_operation_by_name('x').outputs[0]
            y = tf.get_collection("answer")[0]
            keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]
            trainOutput_double.append(sess.run(y, feed_dict={x: [trainInput], keep_prob: 1.0}))
            trainOutput = trainOutput_double[1]

            for mm in range(1, totalNum+1 ):                            ##Seventh line of NeuGreedy pseudo code,mm is the highest index node not yet in greddy_node_set
                if mm not in activated_node_set and trainOutput[0][mm-1]!=1 :            
                    greddynum_now=mm
                    break

        greddy_node_set.append(greddynum_now)
        greddy_node_set = list(set(greddy_node_set))
        max = max
        print(greddy_node_set)
        print(max)
        for h in greddy_node_set:
            f1.write(str(h))
            f1.write(' ')
        f1.write('\r\n')
    f1.close()




