
import tensorflow as tf


class Merge(object):
    '''
    Merge layer is used to merge the list of states from layer below into one state
    '''
    def _train_fprop(self, state_list):
        '''state_list (list): list of states to be merged
        '''
        raise NotImplementedError()

    def _test_fprop(self, state_list):
        '''Defines the forward propogation through the layer during testing,
           defaults to the same as train forward propogation
        '''
        return self._train_fprop(state_list)

    @property
    def _variables(self):
        '''Defines the trainable parameters in the layer
        '''
        return []


class Concat(Merge):
    def __init__(self, axis=1):
        self.axis = axis

    def _train_fprop(self, state_list):
        return tf.concat(self.axis, state_list)


class Mean(Merge):
    def _train_fprop(self, state_list):
        return tf.add_n(state_list) / len(state_list)


class Sum(Merge):
    def _train_fprop(self, state_list):
        return tf.add_n(state_list)


class NoChange(Merge):
    def _train_fprop(self, state_list):
        return state_list


class Multiply(Merge):
    def _train_fprop(self, state_list):
        out = state_list[0]
        for state in state_list[1:]:
            out = tf.mul(out, state)
        return out


class Select(Merge):
    def __init__(self, index=0):
        self.index = index

    def _train_fprop(self, state_list):
        return state_list[self.index]


# class Mask(Template):
#     def _train_fprop(self, state_list):
#         assert len(state_list) == 2
#         state_below, seq_len = state_list
