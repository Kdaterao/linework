import numpy as np
import math
from .general_functions import tan_angle, angle_in_range, closest_point


def connectgaps(gaplist, img, min, distance, range):
    pixels = np.array(img)
    pixels = np.where(pixels == 0)
    pixels = list(zip(pixels[0], pixels[1]))


    matches = []
    unmatched = []
    match_1 = None
    range_calculated = range/2
    for gap in gaplist:
       potential_matches = []
       for pixel in pixels:
        if min < math.hypot(pixel[0] - gap[0][0], pixel[1] -gap[0][1]) < distance:
          dx = pixel[1] - gap[0][1] #x coordinates do not need to be reversed
          dy = gap[0][0] - pixel[0] #y coordinates are reversed on openCV so this allows for the coordinates to be accurate when calculating angles
          angle = tan_angle(dx, dy)
          if angle_in_range(angle, (gap[1] - range_calculated)%360, (gap[1] + range_calculated)%360) == True:
              potential_matches.append(pixel)

       if potential_matches:
        #print('matched')
        #print(gap)
        coordchoice = closest_point(gap[0], potential_matches)
        matches.append((gap[0], coordchoice))
       else:
          unmatched.append(gap)




    return matches, unmatched
