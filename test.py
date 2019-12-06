#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: tensorpack.vgg.py
import sys

import numpy as np
from tensorpack import *

BATCH = 64  # tensorpack's "batch" is per-GPU batch.
try:
    NUM_GPU = int(sys.argv[1])
except IndexError:
    NUM_GPU = 1


class Model(ModelDesc):
    def inputs(self):
        return [tf.TensorSpec([None, 3, 28, 28], tf.float32, 'input'),
                tf.TensorSpec([None], tf.int32, 'label')]

    def build_graph(self, image, label):
        image = image / 255.0

        with argscope(Conv2D, activation=tf.nn.relu, kernel_size=3), \
             argscope([Conv2D, MaxPooling], data_format='channels_first'):
            logits = (LinearWrap(image)
                      .Conv2D('conv1_1', 64)
                      .Conv2D('conv1_2', 64)
                      .MaxPooling('pool1', 2)
                      # 14
                      .Conv2D('conv2_1', 128)
                      .Conv2D('conv2_2', 128)
                      .MaxPooling('pool2', 2)
                      # 7
                      .Conv2D('conv3_1', 256)
                      .Conv2D('conv3_2', 256)
                      .Conv2D('conv3_3', 256)
                      .MaxPooling('pool3', 7)
                      .FullyConnected('fc8', 10, activation=tf.identity)())

        cost = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=label)
        cost = tf.reduce_mean(cost, name='cost')
        return cost

    def optimizer(self):
        return tf.compat.v1.train.RMSPropOptimizer(1e-3, epsilon=1e-8)


def get_data():
    X_train = np.random.random((BATCH, 3, 28, 28)).astype('float32')
    Y_train = np.random.random((BATCH,)).astype('int32')

    def gen():
        while True:
            yield [X_train, Y_train]

    return DataFromGenerator(gen)


if __name__ == '__main__':
    dataset_train = get_data()
    config = TrainConfig(
        model=Model(),
        data=StagingInput(QueueInput(dataset_train)),
        callbacks=[],
        extra_callbacks=[ProgressBar(['cost'])],
        max_epoch=1,
        steps_per_epoch=50,
    )
    if NUM_GPU == 1:
        trainer = SimpleTrainer()
    else:
        trainer = SyncMultiGPUTrainerReplicated(NUM_GPU, mode='nccl')
    launch_train_with_config(config, trainer)
