import tensorflow as tf

totalnum=34             #data set num
greedNum=15                #|S|
reader = tf.train.NewCheckpointReader("save/tensor_net.ckpt")    #read model
W1 = reader.get_tensor("weight0")  #read weight (between input layer and hidden layer) 
output = []
sortoutput=[]
nrow = len(W1)              #row num    
ncol = len(W1[0])           #column num
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


