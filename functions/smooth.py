import numpy as np
from skimage.morphology import remove_small_objects, skeletonize, remove_small_holes
from skimage.util import invert
from .general_functions import thickenline_IMAGE
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def smooth(image):

  if image.ndim == 3:  #Check if the image has color channels
    image = image.mean(axis=2)  #Calculate the mean of color channels to convert to grayscale


  # Invert the image
  image = invert(image)

  # Binarize the image
  binary = image > 0.2

  #smooth the image out a bit
  binary = remove_small_objects(binary, min_size=40)
  binary = skeletonize(binary)
  binary = binary.astype('uint8') * 255
  binary = invert(np.stack([binary, binary, binary], axis=-1)) # Stack to create 3 channels (RGB)
  binary = np.array(binary) # Convert PIL Image to NumPy array


  return binary

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def smooth_2(image):


  if image.ndim == 3:  #Check if the image has color channels
    image = image.mean(axis=2)  #Calculate the mean of color channels to convert to grayscale


  # Invert the image
  image = invert(image)

  # Binarize the image
  binary = image > 0.2

  #smooth the image out a bit
  binary = remove_small_objects(binary, min_size=40)
  binary = binary.astype('uint8') * 255
  binary = invert(np.stack([binary, binary, binary], axis=-1)) # Stack to create 3 channels (RGB)

  return binary


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

def smooth_after(image):

  image= thickenline_IMAGE(4, image)


  if image.ndim == 3:  #Check if the image has color channels
    image = image.mean(axis=2)  #Calculate the mean of color channels to convert to grayscale


  # Invert the image
  image = invert(image)

  # Binarize the image
  binary = image > 0.2

  #smooth the image out a bit
  binary = skeletonize(binary)
  binary = remove_small_holes(binary, area_threshold=20) # Corrected line
  binary = binary.astype('uint8') * 255
  binary = invert(np.stack([binary, binary, binary], axis=-1)) # Stack to create 3 channels (RGB)



  return binary