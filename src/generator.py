import net
import tensorflow as tf


class Generator(net.Net):
    def __init__(self):
        net.Net.__init__(self)
        print("Initialized new 'Generator' instance")

    def build(self, z, x, oc=2):
        """

        :param z: gaussian noise tensor
        :param x: conditional tensor
        :param oc: number of output channels
        :return:
        """
        with tf.variable_scope('generator'):
            inputs = tf.concat(3, [z, x])

            # Encoder
            self.conv1e = self.conv_layer(inputs, 64, act=None, norm=False, name='conv1e')
            self.conv2e = self.conv_layer(self.conv1e, 128, act=self.leaky_relu, name='conv2e')
            self.conv3e = self.conv_layer(self.conv2e, 256, act=self.leaky_relu, name='conv3e')
            self.conv4e = self.conv_layer(self.conv3e, 512, act=self.leaky_relu, name='conv4e')
            self.conv5e = self.conv_layer(self.conv4e, 512, act=self.leaky_relu, name='conv5e')
            self.conv6e = self.conv_layer(self.conv5e, 512, act=self.leaky_relu, name='conv6e')
            self.conv7e = self.conv_layer(self.conv6e, 512, act=self.leaky_relu, name='conv7e')
            self.conv8e = self.conv_layer(self.conv7e, 512, act=self.leaky_relu, name='conv8e')

            # U-Net decoder
            self.conv1d = self.__residual_layer(self.conv8e, self.conv7e, 512, drop=True, name='conv1d')
            self.conv2d = self.__residual_layer(self.conv1d, self.conv6e, 512, drop=True, name='conv2d')
            self.conv3d = self.__residual_layer(self.conv2d, self.conv5e, 512, drop=True, name='conv3d')
            self.conv4d = self.__residual_layer(self.conv3d, self.conv4e, 512, name='conv4d')
            self.conv5d = self.__residual_layer(self.conv4d, self.conv3e, 256, name='conv5d')
            self.conv6d = self.__residual_layer(self.conv5d, self.conv2e, 128, name='conv6d')
            self.conv7d = self.__residual_layer(self.conv6d, self.conv1e, 64, name='conv7d')
            self.output = self.__upsample_layer(self.conv7d, oc, tf.nn.sigmoid, norm=False, name='output')

    def __upsample_layer(self, inputs, out_size, act, name, norm=True, drop=False):
        with tf.variable_scope(name):
            in_size = inputs.get_shape().as_list()[3]
            filters_shape = self.filter_shape + [out_size] + [in_size]
            filters = tf.Variable(tf.truncated_normal(filters_shape, stddev=.02), name='filters')

            # Get dimensions to use for the deconvolution operator
            shape = tf.shape(inputs)
            out_height = shape[1] * self.sample_level
            out_width = shape[2] * self.sample_level
            out_size = filters_shape[2]
            out_shape = tf.pack([shape[0], out_height, out_width, out_size])

            # Deconvolve and normalize the biased outputs
            conv_ = tf.nn.conv2d_transpose(inputs, filters, output_shape=out_shape, strides=self.stride)
            bias = tf.Variable(tf.constant(.1, shape=[out_size]), name='bias')
            conv = tf.nn.bias_add(conv_, bias)

            # Training related ops
            conv = self.instance_normalize(conv) if norm else conv
            conv = tf.nn.dropout(conv, keep_prob=self.dropout_keep) if drop else conv
            activations = act(conv)
            return activations

    def __residual_layer(self, inputs, skip, out_size, name, act=tf.nn.relu, norm=True, drop=False):
        """
        Upsamples a given input tensor and concatenates another given tensor to the output

        :param inputs:
        :param skip:
        :param out_size:
        :param name:
        :param act:
        :param norm:
        :param drop:
        :return:
        """

        conv_ = self.__upsample_layer(inputs, out_size, act, name, norm=norm, drop=drop)
        conv = tf.concat(3, [conv_, skip])
        return conv
