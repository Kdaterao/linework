import numpy as np
from .findgaps import findgaps
from .general_functions import closest_point



def findgap_loop(img, squarelength):
  all_gaps = []
  pixels = np.array(img)
  pixels = np.where(pixels == 0)
  pixels = list(zip(pixels[0], pixels[1]))
  #-----------------------------------------------
  #-----------------------------------------------
  #img = img (adding this for my sanity)
  img_offset_top_left = img[int(squarelength/2):,int(squarelength/2):,:] #offsets image down and to the left
  img_offset_top_left = np.pad(img_offset_top_left, pad_width=((0, int(squarelength/2)), (0, int(squarelength/2)), (0,0)), mode='constant', constant_values=255) #makes the offset part a blank white area(wont be touched)


  img_offset_top_right = img[int(squarelength/2):, :-int(squarelength/2), :]
  img_offset_top_right = np.pad(img_offset_top_right, pad_width=((0, int(squarelength/2)), (int(squarelength/2), 0), (0,0)), mode='constant', constant_values=255)





  #-----------------------------------------------
  #-----------------------------------------------

  gaplist= findgaps(img, squarelength) #returns a list of objects: (gap coordinate within a tile, tile coordinate in context of wholle image, bias(used later when finding line angles))
  gaplist_offset_top_left = findgaps(img_offset_top_left, squarelength)
  gaplist_offset_top_right = findgaps(img_offset_top_right, squarelength)



  #-----------------------------------------------
  #-----------------------------------------------
  half_squarelength = squarelength/2

  for x in gaplist:
    adjusted_gap = (((x[0][1] + (squarelength * x[1][1])), (x[0][0] + (squarelength * x[1][0]))))
    adjusted_gap = closest_point(adjusted_gap, pixels)
    all_gaps.append(((int(adjusted_gap[0]), int(adjusted_gap[1])), x[2]))


  for x in gaplist_offset_top_left:
    adjusted_gap = (((x[0][1] + (squarelength * x[1][1]) + half_squarelength), (x[0][0] + (squarelength * x[1][0])) + half_squarelength))
    adjusted_gap = closest_point(adjusted_gap, pixels)
    all_gaps.append(((int(adjusted_gap[0]), int(adjusted_gap[1])), x[2]))


  for x in gaplist_offset_top_right:
      adjusted_gap = ((x[0][1] + (squarelength * x[1][1]) + half_squarelength),  (x[0][0] + (squarelength * x[1][0]) - half_squarelength))
      adjusted_gap = closest_point(adjusted_gap, pixels)
      all_gaps.append(((int(adjusted_gap[0]), int(adjusted_gap[1])), x[2]))





  return all_gaps #returns a list of objects: (gap coordinate, angle of gap)
