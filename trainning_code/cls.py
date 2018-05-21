# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import random


units =[34,3000,34]

batch_size = 100
iteration = 100
tot_num = 3000
learn_rate = 0.01
def get_data():
    train_feature = []
    test_feature = []
    a = 0
    b = 0
    with open("trainInput_10000_030_2-4.txt", "r") as inputFile:
        for line in inputFile:  
            a+=1
            data = line.split(" ")
            data=[int(x) for x in data[:units[0]]]
            if a<=tot_num:
                train_feature.append(data[:units[0]])
            elif a<=tot_num+tot_num:
                test_feature.append(data[:units[0]])
    train_label = []
    test_label = []
    with open("trainOotput_10000_030_2-4.txt", "r") as outputFile:
        for line in outputFile: 
            b+=1
            data=[]
            data = line.split(" ")
            data=[int(x) for x in data[:units[0]]]
            if b<=tot_num:
                train_label.append(data[:units[0]])
            elif b<=tot_num+tot_num:
                test_label.append(data[:units[0]])
    return train_feature,test_feature, train_label,test_label

def get_batch_data(batch_size):
    train_feature,test_feature, train_label,test_label = get_data()
    rand_idx = np.random.permutation(tot_num)
    x_train_batch,x_test_batch,y_train_batch,y_test_batch = [], [], [], []
    for i in range(batch_size):
        x_train_batch.append(train_feature[rand_idx[i]])
        y_train_batch.append(train_label[rand_idx[i]])
    for i in range(batch_size):
        x_test_batch.append(test_feature[rand_idx[i]])
        y_test_batch.append(test_label[rand_idx[i]])
    return x_train_batch,x_test_batch, y_train_batch,y_test_batch
W=[]
b=[]
for i in range(len(units)-1):
    W.append(tf.Variable(tf.truncated_normal([units[i], units[i+1]], stddev=0.1),name="weight"+str(i)))
    b.append(tf.Variable(tf.zeros([units[i+1]]),name="bias"+str(i)))
x = tf.placeholder(tf.float32, [None, units[0]],name="x")
y_ = tf.placeholder(tf.float32, [None, units[-1]],name="y_")
keep_prob = tf.placeholder(tf.float32,name="keep_prob")
hidden=[]
hidden.append(x)
for i in range(len(units)-2):
    hidden.append(tf.nn.relu(tf.matmul(hidden[-1], W[i]) + b[i]))
hidden_drop = tf.nn.dropout(hidden[-1], keep_prob)
y = tf.matmul(hidden_drop, W[-1]) + b[-1]


cross_entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=y,labels=y_)
loss = tf.reduce_mean(cross_entropy)
training_op = tf.train.AdamOptimizer(learn_rate).minimize(loss)
logits = tf.cast(tf.greater(tf.nn.sigmoid(y), tf.fill([tf.shape(x)[0], units[-1]], 0.5)), tf.float32,name="answer")
precision = tf.metrics.precision(y_,logits)
recall = tf.metrics.recall(y_,logits)
"""
org_p = tf.reduce_mean(tf.cast(tf.equal(tf.reduce_sum(y_, axis=1), tf.ones([tf.shape(y)[0]],tf.float32)), tf.float32))
now_p = tf.reduce_mean(tf.cast(tf.equal(tf.reduce_sum(logits, axis=1), tf.ones([tf.shape(y)[0]],tf.float32)), tf.float32))
p_n = tf.reduce_mean(tf.cast(tf.equal(tf.reduce_sum(y_-logits, axis=1), tf.ones([tf.shape(y)[0]],tf.float32)), tf.float32))
p_p = tf.reduce_sum(org_p-p_n)
recall=tf.div(p_p,org_p)
precision = tf.div(p_p,now_p)
"""
correct = tf.equal(tf.reduce_sum(logits-y_, axis=1), tf.zeros([tf.shape(y)[0]],tf.float32))
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))
saver = tf.train.Saver(write_version=tf.train.SaverDef.V2)
init = tf.global_variables_initializer()
tf.add_to_collection('answer', logits)

with tf.Session() as sess:
    init.run()
    sess.run(tf.local_variables_initializer())
    for iter in range(iteration):
        x_train_batch,x_test_batch, y_train_batch,y_test_batch = get_batch_data(batch_size)
        sess.run(training_op, feed_dict={x: x_train_batch, y_:y_train_batch, keep_prob:0.5})
        train = sess.run([accuracy,precision,recall,loss], feed_dict={x: x_train_batch, y_:y_train_batch, keep_prob:0.5})
        test = sess.run([accuracy,precision,recall,loss], feed_dict={x: x_test_batch, y_:y_test_batch, keep_prob:1.0})
        saver_path = saver.save(sess, "save/tensor_net.ckpt")
        print("iteration ", iter, ",Train_accuracy_loss=", train, ",Test_accuracy_loss=", test)
