import math
from .general_functions import angle_in_range, closest_point_for_filtering_gaps, tan_angle



def match_gaps(gaplist, distance, range, angle_difference):
  templist = gaplist.copy()
  matches = []
  ignorelist = []
  for x in gaplist:
    if x in ignorelist:
      continue
    upper_angle = (x[1] + 180 + int(range/2))%360
    lower_angle = (x[1] + 180 - int(range/2))%360
    potential_matches = []
    for y in templist:
      if y == x:
        continue
      if y in ignorelist:
        continue
      if angle_in_range(y[1], lower_angle, upper_angle) and math.hypot(y[0][0]-x[0][0],y[0][1]-x[0][1]) < distance:
        dx = y[0][1] - x[0][1]
        dy = x[0][0] - y[0][0]
        angle = tan_angle(dx, dy)
        if angle_in_range(angle, (x[1]-angle_difference)%360, (x[1]+angle_difference)%360) == True:
          potential_matches.append(y)

    if potential_matches:
      point, _ = closest_point_for_filtering_gaps(x[0], potential_matches)
      matches.append((x[0], point[0]))
      ignorelist.append(x)
      ignorelist.append(point)


  remaining = [g for g in templist if g not in ignorelist]
  return matches, remaining
