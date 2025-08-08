from .general_functions import closest_point_for_filtering_gaps, check_border_points



def filter_gaps(gaplist, range, image):

  templist = gaplist.copy()

  for b in gaplist:

    checklist = []
    for c in templist:
      if c !=b:
        checklist.append(c)

    closest_point, distance = closest_point_for_filtering_gaps(b[0], checklist)

    if distance < range and closest_point != b:
      templist.remove(b)




  for x in templist:
    goodtoremove = check_border_points(x[0], image, 50)
    if goodtoremove == True:
        templist.remove(x)

  return templist