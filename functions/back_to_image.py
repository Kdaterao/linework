from PIL import Image

def back_to_image(Generated_image):

  #print(Generated_image)
  
  # converts numpy array into an actual image
  converted_image = Image.fromarray(Generated_image)

  return converted_image