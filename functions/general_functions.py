import math
import numpy as np
from PIL import Image

#all of these functions are used within the larger functions, allowing for easier readability 
#i organized them so that all functions that have similar functionality are closer together 
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


def closest_point(target, points):

  closest_point = min(points, key=lambda point: math.hypot(target[1]-point[1], target[0]-point[0]))   #syntax of min() can be min(list, key=function applied to each element), we use a lambda function since the function is small(syntax of lambda is typically: lambda inputvalue:actual function), but we couldve defined this function in another spot if we wanted and then referenced it.
  return closest_point

#-----------------------------------------------
#-----------------------------------------------

def closest_point_for_filtering_gaps(target, points):

  closest_point = min(points, key=lambda point: math.hypot(target[1]-point[0][1], target[0]-point[0][0]))   #syntax of min() can be min(list, key=function applied to each element), we use a lambda function since the function is small(syntax of lambda is typically: lambda inputvalue:actual function), but we couldve defined this function in another spot if we wanted and then referenced it.
  distance = int(math.hypot(target[0] - closest_point[0][0], target[1] - closest_point[0][1]))
  return closest_point, distance


#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------

def tan_angle(x, y):
    angle_rad = math.atan2(y, x)
    angle_deg = math.degrees(angle_rad)
    return angle_deg % 360  #Normalize to [0, 360) range

#-----------------------------------------------
#-----------------------------------------------

def angle_in_range(alpha, lower, upper):

    alpha = alpha % 360
    lower = lower % 360
    upper = upper % 360

    if lower <= upper:

        return lower <= alpha < upper
    else:

        return lower <= alpha < 360 or 0 <= alpha < upper
    

#-----------------------------------------------
#-----------------------------------------------


def mean_angle_deg(angles):
    # Convert angles from degrees to radians
    angles_rad = np.deg2rad(angles)

    # Compute the mean of the unit vectors
    sin_sum = np.sum(np.sin(angles_rad))
    cos_sum = np.sum(np.cos(angles_rad))

    # Compute the average angle in radians
    mean_angle_rad = np.arctan2(sin_sum, cos_sum)

    # Convert back to degrees
    mean_angle_deg = np.rad2deg(mean_angle_rad)

    # Ensure result is in [0, 360)
    return mean_angle_deg % 360


#-----------------------------------------------
#-----------------------------------------------


def find_angle(gap, img, distance, bias):

    gap = (int(gap[0]), int(gap[1])) 

    pixels = np.array(img)
    pixels = np.where(pixels == 0)
    pixels = list(zip(pixels[0], pixels[1])) 

    angle_list = []

    for pixel in pixels:
      dx = pixel[1] - gap[1] #x coordinates do not need to be reversed
      dy = gap[0] - pixel[0] #y coordinates are reversed on openCV so this allows for the coordinates to be accurate when calculating angles



      if  distance - 2 < math.hypot(dx, dy) < (distance + 2):
        angle = tan_angle(dx, dy)
        if angle_in_range(angle, (bias[0])%360, (bias[1])%360) == True:
          angle_list.append(angle)



    if angle_list:
         final_angle = mean_angle_deg(angle_list)
         final_angle = (final_angle + 180)%360

    else:
        for pixel_1 in pixels:
          dx = pixel_1[1] - gap[1] #x coordinates do not need to be reversed
          dy = gap[0] - pixel_1[0] #y coordinates are reversed on openCV so this allows for the coordinates to be accurate when calculating angles

          if  distance/2 - 1 < math.hypot(dx, dy) < (distance/2 + 2):
            angle = tan_angle(dx, dy)
            if angle_in_range(angle, (bias[0])%360, (bias[1])%360) == True:
              angle_list.append(angle)


        if angle_list:
          final_angle = mean_angle_deg(angle_list)
          final_angle = (final_angle + 180)%360
        else:
          final_angle = mean_angle_deg([bias[0],bias[1]])
          final_angle = (final_angle + 180)%360

    return final_angle

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------

def save_tiles_with_coords(img, rows, cols): 
    height, width, channels = img.shape
    tile_height = height // rows
    tile_width = width // cols
    tilelist = []
    for row in range(rows):
        for col in range(cols):
            top = row * tile_height
            left = col * tile_width
            bottom = (row + 1) * tile_height
            right = (col + 1) * tile_width

            tile = img[top:bottom, left:right]

            tilelist.append((tile, (col, row)))

    return tilelist


#-----------------------------------------------
#-----------------------------------------------

def touchingboundcheck(basecoord, tile, padding, range, right, bottom, left, top):
    height, width, _ = tile.shape 

    y,x  = basecoord
    close = False

    if x + range >= width:
      right = True
    elif x - range <= 0:
      left = True
    elif y + range >= height:
      bottom = True
    elif y - range <= 0:
      top  = True

    if x + padding >= width:
      close = True
    elif x - padding <=  0:
      close = True
    elif y + padding >= height:
      close = True
    elif y - padding <= 0:
      close = True

    return right, bottom, left, top, close

#-----------------------------------------------
#-----------------------------------------------


def check_border_points(point, img, padding):
  height, width, channels = img.shape #gets height and width of the tile(channels is not used, but is expected as a variable when getting shape)

  y,x  = point


  if x + padding >= width:
    return True

  elif x - padding <=  0:
    return True

  elif y + padding >= height:
    return True

  elif y - padding <= 0:
    return True

  else:
    return False


#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


def thickenline_IMAGE(radius, image):
  RoughImages = np.array(image)
  blacklistfilter = np.where(RoughImages < 10)
  pointlist = (blacklistfilter[0].tolist(), blacklistfilter[1].tolist())
  height, width, _ = RoughImages.shape
  #--
  for n in range(len(pointlist[0])):
    xcoord = pointlist[0][n]
    ycoord = pointlist[1][n]
    for x in range(xcoord - radius, xcoord + radius + 1):
      for y in range(ycoord - radius, ycoord + radius + 1):
        if math.hypot(x - xcoord, y - ycoord) <= radius:
          if 0 <= x < height and 0 <= y < width:
              RoughImages[x, y] = [0, 0, 0]
  return RoughImages

#-----------------------------------------------
#-----------------------------------------------


#temporary use to see where gaps are
def createsquare(gaplist, squarelength):
  squarelist = []

  if isinstance(gaplist, list):
    for x in gaplist:
      coord = x[0]
      for x_offset in range(squarelength):
        for y_offset in range(squarelength):
          xcoord = coord[0] + x_offset - int(squarelength/2)
          ycoord = coord[1] + y_offset - int(squarelength/2)
          squarelist.append((xcoord, ycoord))
  else:
    coord = gaplist[0]
    for x_offset in range(squarelength):
        for y_offset in range(squarelength):
          xcoord = coord[0] + x_offset - int(squarelength/2)
          ycoord = coord[1] + y_offset - int(squarelength/2)
          squarelist.append((xcoord, ycoord))


  return squarelist

#-----------------------------------------------
#-----------------------------------------------

#temporary use to see where gaps are
def createsquare_1(gaplist, squarelength):
  squarelist = []

  if isinstance(gaplist, list):
    for x in gaplist:
      coord = x
      for x_offset in range(squarelength):
        for y_offset in range(squarelength):
          xcoord = coord[0] + x_offset - int(squarelength/2)
          ycoord = coord[1] + y_offset - int(squarelength/2)
          squarelist.append((xcoord, ycoord))
  else:
    coord = gaplist
    for x_offset in range(squarelength):
        for y_offset in range(squarelength):
          xcoord = coord[0] + x_offset - int(squarelength/2)
          ycoord = coord[1] + y_offset - int(squarelength/2)
          squarelist.append((xcoord, ycoord))


  return squarelist


#-----------------------------------------------
#-----------------------------------------------

def drawbetweenpoints(startingpoint, targetpoint, linelist):

    x0, y0 = startingpoint
    x1, y1 = targetpoint

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = (dx if dx > dy else -dy) // 2

    while True:
      linelist.append((x0, y0))

      if x0 == x1 and y0 == y1:
        break

      if math.dist((x0, y0),(x1, y1)) < 2:
        break

      e2 = err
      if e2 > -dx:
        err -= dy
        x0 += sx
      if e2 < dy:
        err += dx
        y0 += sy

    return linelist

#-----------------------------------------------
#-----------------------------------------------

def draw_on_image(image, coordinates, color):
  #Check if the image is a color image
  height, width, _ = image.shape

  image_array = np.array(image)

  for coord in coordinates:
    x, y = coord
    if 0 <= x < height and 0 <= y < width: # Check if the coordinates are within the image bounds
      image_array[coord[0], coord[1]] = color 

  image_array = image_array.astype(np.uint8)

  modified_image = Image.fromarray(image_array)

  return modified_image
