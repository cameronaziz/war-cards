from typing import Any, Optional

import numpy as np
import numpy.typing as npt
import tensorflow as tf
import tensorflow.keras as keras


class Net(keras.Model):
    def __init__(self, n_actions: int, fc1_dims: int, fc2_dims: int):
        super(Net, self).__init__()
        self.dense1 = keras.layers.Dense(fc1_dims, activation="relu")
        self.dense2 = keras.layers.Dense(fc2_dims, activation="relu")
        self.V = keras.layers.Dense(1, activation=None)
        self.A = keras.layers.Dense(n_actions, activation=None)

    def call(
        self,
        state: npt.NDArray[np.int32],
        training: Optional[bool] = None,
        mask: Any = None,
    ):
        x = self.dense1(state)
        x = self.dense2(x)
        V = self.V(x)
        A = self.A(x)

        Q: Any = V + (A - tf.math.reduce_mean(A, axis=1, keepdims=True))

        return Q

    def advantage(self, state: npt.NDArray[np.int32]):
        x = self.dense1(state)
        x = self.dense2(x)
        A: Any = self.A(x)

        return A
