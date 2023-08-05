class model(dict):
    """
    Creates a dict that one can access using dot notation

    usage:

        # create new model
        net = model()

        # use net.last to chain together tensor operations
        net.tensor_a = tf.constant(10)
        net.tensor_b = net.last * 100
        net.tensor_c = net.last * 1000

        # list all ops
        net.keys()

    """

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

        # we also set self.last equal to the most recent value
        # for
        self['last'] = self[attr]
