import numpy as np
from .general_functions import closest_point, save_tiles_with_coords, touchingboundcheck, find_angle

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#This is the main function
def findgaps(roughimage, squarelength):
  gaps = []
  checkedtiles = 0
  if squarelength < 25:
    padding = 5
    closepadding = 5
  else:
    padding = 8
    closepadding = 8
  #-----------------------------------------------
  #-----------------------------------------------
  cutup_images_rough = save_tiles_with_coords(roughimage, int(1080 / squarelength), int(1920 / squarelength)) #returns a list of objects which each contain (tile image, tile coordinate in context of full image)
  for x in cutup_images_rough:
      right = False
      bottom = False
      left = False
      top = False
      right_1 = False
      bottom_1 = False
      left_1 = False
      top_1 = False
      closepixels = 0
      close = False
      #-----------------------------------------------
      #-----------------------------------------------
      blackpixels = np.array(x[0])
      blackpixels = np.where(blackpixels == 0)
      blackpixels = list(zip(blackpixels[0], blackpixels[1]))
      #-----------------------------------------------
      #-----------------------------------------------
      if len(blackpixels) > 40:
        checkedtiles += 1
        for b in blackpixels:
          right, bottom, left, top, close = touchingboundcheck(b, x[0], closepadding , padding , right, bottom, left, top) #(pixel, image, padding for checking closeness, range of checking siedes, right, bottom, left, top)

          if close == True:
            closepixels += 1

          if top == True:
            top_1 = True

          if bottom == True:
            bottom_1 = True

          if left == True:
            left_1 = True

          if right == True:
            right_1 = True


          right = False
          bottom = False
          left = False
          top = False
          close = False
        #-----------------------------------------------
        #-----------------------------------------------
        variables = [right_1, bottom_1, left_1, top_1]
        if variables.count(True) == 1 and closepixels < 0.90*len(blackpixels): #checks if pixels only touch one side and that most pixels are not right next to that one side
          
          if top_1 == True:
            bias = (0, 180) #bias is used later on when we check the actual direction of the line(increases angle accuracy)
            bias_coord = (int(squarelength), int(squarelength/2))
          elif bottom_1 == True:
            bias = (180, 360)
            bias_coord = (0, int(squarelength/2))
          elif left_1 == True:
            bias = (90, 270)
            bias_coord = (int(squarelength/2), int(squarelength))
          elif right_1 == True:
            bias = (270, 90)
            bias_coord = (int(squarelength/2), int(0))

          point = closest_point(bias_coord, blackpixels)

          angle = find_angle(point, x[0], 10, bias)


          gaps.append((point, x[1], angle))



  return gaps