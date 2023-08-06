from __future__ import unicode_literals, print_function

from .optimizers import Eve, Adam, linear_decay
from .util import minibatch, score_model

import random
import tqdm


class Trainer(object):
    def __init__(self, model, train_data, L2=0.0):
        self.ops = model.ops
        self.model = model
        self.optimizer = Eve(model.ops, 0.001)
        self.batch_size = 128
        self.nb_epoch = 1
        self.i = 0
        self.L2 = 0.0
        self.dropout = 0.9
        self.dropout_decay = 1e-4
        self._loss = 0.

    def __enter__(self):
        return self, self.optimizer

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.model.use_params(self.optimizer.averages)

    def __call__(self, data, gradient):
        return self.optimizer(data, gradient, L2=self.L2)

    def iterate(self, model, train_data, dev_X, dev_Y, nb_epoch=None):
        if nb_epoch is None:
            nb_epoch = self.nb_epoch
        orig_dropout = self.dropout
        for i in range(nb_epoch):
            random.shuffle(train_data)
            for batch in tqdm.tqdm(minibatch(train_data,
                                   batch_size=self.batch_size)):
                X, y = zip(*batch)
                yield X, y
                self.dropout = linear_decay(orig_dropout, self.dropout_decay,
                                            self.optimizer.nr_iter)
            acc = score_model(model, dev_X, dev_Y)
            stats = (acc, self._loss, self.dropout)
            print('Dev.: %.3f, loss %.3f. Drop %.2f' % stats)
            self._loss = 0.
