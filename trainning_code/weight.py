import tensorflow as tf

totalnum=34
greedNum=15
reader = tf.train.NewCheckpointReader("save/tensor_net.ckpt")
W1 = reader.get_tensor("weight0")
output = []
sortoutput=[]
nrow = len(W1)
ncol = len(W1[0])
for i in range(nrow):
    sortoutput.append(sum([abs(W1[i][x]) for x in range(ncol)]))
for ab in range(nrow):
    output.append(sum([abs(W1[ab][x]) for x in range(ncol)]))

sortoutput.sort()   #Minweight
#sortoutput.sort(reverse = True) # #NeuMax
f1 = open('xxx', 'w', encoding='utf-8')     #Minweight
#f1 = open('xxx', 'w', encoding='utf-8')    #NeuMax
for h in range(greedNum):
    for m in range(len(output)):
        if sortoutput[h]==output[m]:
            print (m+1)
            f1.write(str(m+1))
            f1.write(' ')
f1.close()


