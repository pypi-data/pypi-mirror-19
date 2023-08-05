import math
import numpy as np
import tensorflow as tf
import layers as L
import tools



def build(input_tensor=None,
          n_classes=1000,
          bgr_img_mean=None,
          is_training_tensor=None,
          scope="vgg16"):

    """
    This functions creates all the tensorflow graph operations for the VGG16 network using the
    current tf.Graph() context

    Arguments:
        input_tensor:
            Reference to a tf.placeholder of shape [None, 224, 224, 3]

        n_classes:
            Number of classes to use in the final layer output (default: 1000)

        bgr_img_mean:
            Image mean to subtract from the input_tensor (default: [103.939, 116.779, 123.68])

        is_training_tensor:
            Reference to a tf.bool tensor to control whether to
            turn on dropout or not (default: False)

        scope:
            String for the name scope to place all variables and operations under in your
            tf.Graph (default: "vgg16")

    Returns:
        An "net" dictionary with access to all inference operations.

    """

    net = tools.model()

    # define image mean if none provided
    if bgr_img_mean is None:
        bgr_vgg_mean = [103.939, 116.779, 123.68]

    with tf.variable_scope(scope):

        # We assume input_tensor is 224x224x3 rgb tensor with values from 0 to 255.0
        if input_tensor is None:
            net.input_tensor = tf.placeholder(tf.float32, [None, 224, 224, 3])
        else:
            net.input_tensor = input_tensor

        # assign is_training tensor
        if is_training_tensor is None:
            net.is_training_tensor = tf.constant(False, dtype=tf.bool)
        else:
            net.is_training_tensor = is_training_tensor

        # set dropout to 0.5 as stated
        net.dropout_keep_prob = tf.select(net.is_training_tensor, 0.5, 1.0)


        # convert input image to bgr and subtract mean
        r, g, b = tf.split(split_dim=3, num_split=3, value=net.input_tensor)
        net.bgr_centered = tf.concat(3, [
            b - bgr_vgg_mean[0],
            g - bgr_vgg_mean[1],
            r - bgr_vgg_mean[2],
        ], name="bgr_centered")

        # block 1 -- outputs 112x112x64
        net.conv1_1  = L.conv(net.last, name="conv1_1", kh=3, kw=3, n_out=64)
        net.conv1_2  = L.conv(net.last, name="conv1_2", kh=3, kw=3, n_out=64)
        net.pool1    = L.pool(net.last, name="pool1", kh=2, kw=2, dw=2, dh=2)

        # block 2 -- outputs 56x56x128
        net.conv2_1  = L.conv(net.last, name="conv2_1", kh=3, kw=3, n_out=128)
        net.conv2_2  = L.conv(net.last, name="conv2_2", kh=3, kw=3, n_out=128)
        net.pool2    = L.pool(net.last, name="pool2", kh=2, kw=2, dh=2, dw=2)

        # # block 3 -- outputs 28x28x256
        net.conv3_1  = L.conv(net.last, name="conv3_1", kh=3, kw=3, n_out=256)
        net.conv3_2  = L.conv(net.last, name="conv3_2", kh=3, kw=3, n_out=256)
        net.conv3_3  = L.conv(net.last, name="conv3_3", kh=3, kw=3, n_out=256)
        net.pool3    = L.pool(net.last, name="pool3", kh=2, kw=2, dh=2, dw=2)

        # block 4 -- outputs 14x14x512
        net.conv4_1  = L.conv(net.last, name="conv4_1", kh=3, kw=3, n_out=512)
        net.conv4_2  = L.conv(net.last, name="conv4_2", kh=3, kw=3, n_out=512)
        net.conv4_3  = L.conv(net.last, name="conv4_3", kh=3, kw=3, n_out=512)
        net.pool4    = L.pool(net.last, name="pool4", kh=2, kw=2, dh=2, dw=2)

        # block 5 -- outputs 7x7x512
        net.conv5_1  = L.conv(net.last, name="conv5_1", kh=3, kw=3, n_out=512)
        net.conv5_2  = L.conv(net.last, name="conv5_2", kh=3, kw=3, n_out=512)
        net.conv5_3  = L.conv(net.last, name="conv5_3", kh=3, kw=3, n_out=512)
        net.pool5    = L.pool(net.last, name="pool5", kh=2, kw=2, dw=2, dh=2)

        # flatten
        flattened_shape = np.prod([s.value for s in net.last.get_shape()[1:]])
        net.flattened   = tf.reshape(net.last, [-1, flattened_shape], name="flattened")

        # fully connected layers
        net.fc6      = L.dense(net.last, name="fc6", n_out=4096)
        net.fc6_drop = tf.nn.dropout(net.last, net.dropout_keep_prob)
        net.fc7      = L.dense(net.last, name="fc7", n_out=4096)
        net.fc7_drop = tf.nn.dropout(net.last, net.dropout_keep_prob)
        net.fc8      = L.dense(net.last, name="fc8", n_out=n_classes)

        # output softmax probabilities and sorted class ids from highest to lowest probability
        net.probs = tf.nn.softmax(net.last, name="probs")

    return net


def restore(sess, fpath):
    """
    Loads the parameters of a vgg network from .npy file given a
    session with a graph containing the vgg network.

    Arguments:

    """

    # populate weights map
    param_map = {}
    weights = np.load(fpath).item()
    for key in sorted(weights.keys()):
        w, b = weights[key]
        param_map["vgg16/%s/weights:0" % key] = w
        param_map["vgg16/%s/bias:0" % key] = b

    # assign loaded parameters to graph nodes
    for v in sess.graph.get_collection("variables"):
        param = param_map.get(v.name)
        if param is None:
            print("could not load variable %s" % v.name)
            continue

        # we create an assign placeholder so that we don't store the actual value of the
        # parameter as a constant in the graph
        with sess.graph.as_default():
            with tf.variable_scope("loader"):
                placeholder = tf.placeholder(dtype=v.dtype, shape=v.get_shape())
                assign = v.assign(placeholder)

        sess.run(assign, feed_dict={placeholder: param})


if __name__ == '__main__':
    x = tf.placeholder(tf.float32, [10, 224, 224, 3])
    net = build(x)
    print sorted(net.keys())
    print net.last
