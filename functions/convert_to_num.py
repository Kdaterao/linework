import numpy as np
import tensorflow as tf
def convert_to_num(image):
    image_bytes = image.read()
    # Decode bytes into a Tensor
    pixel = tf.image.decode_png(image_bytes, channels=3)
    pixel = tf.cast(pixel, tf.float32)
    # Convert the image to a NumPy array
    image_np = np.array(pixel)
    print('Loaded: ', image_np.shape)
    
    return image_np