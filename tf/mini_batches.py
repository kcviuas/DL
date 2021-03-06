import tensorflow as tf
import numpy as np 
import sklearn
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing() 
m, n = housing.data.shape 
housing_data_plus_bias = np.c_[np.ones((m, 1)), housing.data]


n_epochs = 1000
learning_rate = 0.01

batch_size = 5500
n_batches = int(np.ceil(m / batch_size))

# transform the data to let all of its fratures' mean=0 and std=1
transformer = sklearn.preprocessing.StandardScaler().fit(housing_data_plus_bias)
scaled_housing_data_plus_bias = transformer.transform(housing_data_plus_bias)

# create node and computing graph
X = tf.placeholder(tf.float32, shape=(None, n + 1), name="X") 
y = tf.placeholder(tf.float32, shape=(None, 1), name="y")
theta = tf.Variable(tf.random_uniform([n + 1, 1], -1.0, 1.0), name="theta")
y_pred = tf.matmul(X, theta, name="predictions")
error = y_pred - y
mse = tf.reduce_mean(tf.square(error), name="mse")      # total loss


optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate, momentum=0.9)
training_op = optimizer.minimize(mse)

# fetch_batch should return batch in a random order, for simplicity this demo avoid it.
def fetch_batch(epoch, batch_index, batch_size):
    m,_ = scaled_housing_data_plus_bias.shape

    if (batch_index+1)*batch_size > m:
        to = m
    else:
        to = (batch_index+1)*batch_size

    X_batch = scaled_housing_data_plus_bias[batch_index*batch_size:to]
    y_batch = housing.target.reshape(-1, 1)[batch_index*batch_size:to]
    return X_batch, y_batch


init = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(n_epochs):
        for batch_index in range(n_batches):
            X_batch, y_batch = fetch_batch(epoch, batch_index, batch_size)
            sess.run(training_op, feed_dict={X:X_batch, y:y_batch})
            print("epoch", epoch, "batches", batch_index, " MSE=", mse.eval(feed_dict={X:X_batch, y:y_batch}))
    
    best_theta = theta.eval()

print(best_theta)