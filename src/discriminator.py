import net
import tensorflow as tf


class Discriminator(net.Net):
    def __init__(self, filter_size=4):
        net.Net.__init__(self)
        print("Initialized new 'Discriminator' instance")
        self.filter_size = filter_size
        self.stride1 = [1, 2, 2, 1]
        self.stride2 = [1, 1, 1, 1]
        self.is_training = True

    def predict(self, y, x, noise=None):
        """
        Predicts the probability a given input belongs to a targeted sample distribution

        :param y: input tensor
        :param x: conditional tensor
        :param noise: regularizing gaussian noise tensor to add to xy
        :return: probability tensor, logit tensor, average probability tensor
        """

        if noise is not None:
            y += noise

        xy = tf.concat(3, [y, x])

        with tf.variable_scope('discriminator'):
            conv0 = self.conv_layer(xy, 64, act=self.leaky_relu, norm=False, pad='SAME', stride=self.stride1, name='conv0')

            conv1 = self.conv_layer(conv0, 128, act=self.leaky_relu, pad='SAME', stride=self.stride1, name='conv1')
            conv2 = self.conv_layer(conv1, 256, act=self.leaky_relu, pad='SAME', stride=self.stride1, name='conv2')
            conv3 = self.conv_layer(conv2, 512, act=self.leaky_relu, pad='SAME', stride=self.stride1, name='conv3')
            conv4 = self.conv_layer(conv3, 512, act=self.leaky_relu, pad='SAME', stride=self.stride1, name='conv4')

            conv5 = self.conv_layer(conv4, 512, act=self.leaky_relu, pad='SAME', stride=self.stride2, name='conv5')
            conv6 = self.conv_layer(conv5, 512, act=None, norm=False, pad='SAME', stride=self.stride2, name='conv6')

        tf.get_variable_scope().reuse_variables()
        return conv6
