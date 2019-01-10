import tensorflow as tf
import numpy as np
If0=1  #Initial number of the network node
propre=0.5   #lamda
greedNum=20  #size of seed set
totalNum=1454 #node number of the network


def Normalized(martix):                  #W_total Normalized
    qq=martix
    for i in range(len(qq)):
        one_list = []
        for j in range(len(qq)):
            one_list.append(qq[j][i])
        Max = max(one_list)
        one_list.sort()
        for h in range(len(one_list)):

            Min=one_list[h]
            break
        for m in range(len(qq)):
            if qq[m][i]!=0 and qq[m][i]!=0:
                qq[m][i]=(qq[m][i] - Min) / (Max - Min)
    return  qq


def activated_count(nodeset,Maxrtix):   #
    tmp=0
    activated_node_ne = []
    for i in range(len(nodeset)):
        activated_node_ne.append(nodeset[i])
    length = len(activated_node_ne)
    while length != tmp:
        length = len(activated_node_ne)
        tmp_problem = 0
        for m in range(len(Maxrtix)):
            tmp_problem=0
            for node in activated_node_set:
                tmp_problem=tmp_problem+Maxrtix[node][m]
            if tmp_problem>=propre:
               activated_node_ne.append(m)
        activated_node_ne = list(set(activated_node_ne))
        tmp = len(activated_node_ne)
    return tmp


reader = tf.train.NewCheckpointReader("save/tensor_net.ckpt")   #load IPM
W1 = reader.get_tensor("weight0")
W2 = reader.get_tensor("weight1")
W3=np.dot(W1,W2)    #W_total
output = []
sortoutput=[]



for i in range(totalNum):
    sortoutput.append(sum([W3[i][x] for x in range(totalNum)]))
for ab in range(totalNum):
    output.append(sum([W3[ab][x] for x in range(totalNum)]))
sortoutput.sort(reverse = True)
abslist=[]
for h in range(greedNum):
    for m in range(len(output)):
        if sortoutput[h]==output[m]:
            abslist.append(m)



num1row=[]
nrow = len(W3)
ncol = len(W3[1])
for i in range(ncol):
    num1row.append(W3[0][i])
q=[]

q1=Normalized(W3)


greddy_node_set = []
activated_node_set=[]
max = 1

for x in range(greedNum):                       #chose and put node in seed set
    for m in range(0, totalNum):
        if m not in greddy_node_set:
            greddy_node_set.append(m)

            activated_node_set=[]
            for h in greddy_node_set:
                activated_node_set.append(h)
            templength = activated_count(activated_node_set,q1)
            if templength > max:
                max = templength
                greddynum_now=m
                if greddy_node_set.count(m)>1:
                    greddy_node_set.remove(m)
                    greddy_node_set.append(m)
                else:
                    greddy_node_set.remove(m)
            elif templength <= max:
                if greddy_node_set.count(m)>1:
                    greddy_node_set.remove(m)
                    greddy_node_set.append(m)
                else:
                    greddy_node_set.remove(m)
    if greddynum_now not in greddy_node_set:
        greddy_node_set.append(greddynum_now)

    else:
        for h in range(greedNum):
            if abslist[h] not in greddy_node_set:
                greddy_node_set.append(abslist[h])


    greddy_node_set=list(set(greddy_node_set))

    max=max
    print(greddy_node_set)
    print(max)







