#!/usr/bin/env python
# 2018, Patrick Wieschollek <mail@patwie.com>

import numpy as np
import tensorflow as tf
from __init__ import matrix_add

np.random.seed(42)
tf.set_random_seed(42)


class MatrixAddtest(tf.test.TestCase):

  def _forward(self, use_gpu=False, dtype=np.float32):
    matA = np.random.randn(1, 4, 4, 1).astype(dtype) * 10

    expected = matA[0:1, 0:4, 0:4, 0:1]

    matA_op = tf.convert_to_tensor(matA)

    with self.test_session(use_gpu=use_gpu, force_gpu=use_gpu) as sess:
      actual_op = matrix_add(matA_op, (1.5,1.5))
      actual = sess.run(actual_op)

#    self.assertShapeEqual(expected, actual_op)
    self.assertAllClose(expected, actual)

  def test_forward_int32(self):
    self._forward(use_gpu=False, dtype=np.int32)
    self._forward(use_gpu=True, dtype=np.int32)

  def test_forward_uint32(self):
    self._forward(use_gpu=False, dtype=np.uint32)
    self._forward(use_gpu=True, dtype=np.uint32)

  def test_forward_float(self):
    self._forward(use_gpu=False, dtype=np.float32)
    self._forward(use_gpu=True, dtype=np.float32)

  def test_forward_double(self):
    self._forward(use_gpu=False, dtype=np.float64)
    self._forward(use_gpu=True, dtype=np.float64)

  def _backward(self, use_gpu=False, dtype=np.float32):
    matA = np.random.randn(1, 2, 3, 4).astype(dtype) * 10

    expected = (matA).astype(np.float32)

    matA_op = tf.convert_to_tensor(matA)

    with self.test_session(use_gpu=use_gpu, force_gpu=use_gpu):
      actual_op = matrix_add(matA_op, (1.5, 1.5))
      err = tf.test.compute_gradient_error(
          [matA_op], [matA.shape],
          actual_op, expected.shape)

    self.assertLess(err, 1e-2)

  def test_backward_float(self):
    self._backward(use_gpu=False, dtype=np.float32)
    self._backward(use_gpu=True, dtype=np.float32)

  def test_backward_double(self):
    self._backward(use_gpu=False, dtype=np.float64)
    self._backward(use_gpu=True, dtype=np.float64)


if __name__ == '__main__':
  tf.test.main()
