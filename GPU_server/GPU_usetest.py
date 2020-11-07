import tensorflow as tf
from tensorflow.python.client import device_lib
tf.debugging.set_log_device_placement(True)

print(device_lib.list_local_devices())

try:
  with tf.device('/device:XLA_GPU:0'):
    a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    c = tf.matmul(a, b)
    print('run end')
except RuntimeError as e: #유효하지 않은 GPU 장치를 명시
  print(e)
