import numpy as np
import math
from .general_functions import tan_angle,angle_in_range

def cornercheck(gaplist, img, distance):

    pixels = np.array(img)
    pixels = np.where(pixels == 0)
    pixels = list(zip(pixels[0], pixels[1]))


    for gap in gaplist:
       angle_list = []
       upper_range = (gap[1] + 180 + 90)%360
       lower_range = (gap[1] + 180 - 90)%360
       for pixel in pixels:
        if distance - 2  < math.hypot(pixel[0] - gap[0][0], pixel[1] -gap[0][1]) < distance + 2:
          dx = pixel[1] - gap[0][1] #x coordinates do not need to be reversed
          dy = gap[0][0] - pixel[0] #y coordinates are reversed on openCV so this allows for the coordinates to be accurate when calculating angles
          angle = tan_angle(dx, dy)
          if angle_in_range(angle, lower_range, upper_range) == True:
              angle_list.append(angle)

       if angle_list:
         final_angle = (sum(angle_list) / len(angle_list))%360
         if angle_in_range(final_angle, (angle_list[0] - 15)%360, (angle_list[0] + 15)%360) == False:
            final_angle = False
            #print('corner')
            #print(gap)
            gaplist.remove(gap)

    return gaplist