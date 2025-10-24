
from functions.findgap_loop import findgap_loop
from functions.smooth import smooth, smooth_2, smooth_after
from functions.filter_gaps import filter_gaps
from functions.cornercheck import cornercheck
from functions.general_functions import createsquare, createsquare_1, draw_on_image, thickenline_IMAGE, drawbetweenpoints
from functions.matchgaps import match_gaps
from functions.connectgaps import connectgaps
from functions.convert_to_num import convert_to_num
import streamlit as st






def model(image_import):
  placeholder = st.empty()
  image_import = convert_to_num(image_import)

  placeholder.write(':red[Image converted...]')


  image = smooth(image_import) #the same image but smaller blobs are deleted
  image_v2 = smooth_2(image_import) # lines are bit thicker
  #-----------------------------------------------
  #-----------------------------------------------
  gaps_1 = findgap_loop(image, 15)
  gaps_2 = findgap_loop(image, 20)
  gaps_3 = findgap_loop(image,24)
  gaps_4 = findgap_loop(image, 30)


  gaps_5 = findgap_loop(image_v2, 15)
  gaps_6 = findgap_loop(image_v2, 20)
  gaps_7 = findgap_loop(image_v2, 24)
  gaps_8 = findgap_loop(image_v2, 30)
  gaps_9 = findgap_loop(image_v2, 40)


  gaps = gaps_1 + gaps_2 + gaps_3 + gaps_4 + gaps_5 + gaps_6  + gaps_7 + gaps_8 + gaps_9
  placeholder.write(':red[gaps found...]')

  
  #-----------------------------------------------
  #-----------------------------------------------
  filtered_gaps = list(set(gaps))
  filtered_gaps = filter_gaps(filtered_gaps, 20, image)
  filtered_gaps = cornercheck(filtered_gaps, image_v2, 10)


  post_filtered_gaps = filtered_gaps.copy() #for visualization of gaps
  #print(post_filtered_gaps)
  #-----------------------------------------------
  #-----------------------------------------------

  matches, filtered_gaps = match_gaps(filtered_gaps, 20, 60, 140)   #(list,  farthest gap to match with,  range of angle for gaps that can be looked at, peak difference in angle)
  matches_1, filtered_gaps = match_gaps(filtered_gaps, 40, 180, 100)
  matches_2, filtered_gaps = match_gaps(filtered_gaps, 60, 180,60)
  matches_3, filtered_gaps = match_gaps(filtered_gaps, 100,90,60)
  matches_4, filtered_gaps = match_gaps(filtered_gaps, 200,50,60)

  matches_5, filtered_gaps = connectgaps(filtered_gaps, image, 20, 100, 30) #(list, image, closest possible pixel, farthest possible pixel, range of angles that pixels that be looked at)
  matches_6, filtered_gaps = connectgaps(filtered_gaps, image, 20, 100, 60)
  matches_67, filtered_gaps = connectgaps(filtered_gaps, image, 20, 60, 90)
  matches_7, filtered_gaps = connectgaps(filtered_gaps, image, 5, 40, 200)
  matches =  matches + matches_1 + matches_2 + matches_3 + matches_4 + matches_5 + matches_6 + matches_7 + matches_67 #67 lol
  

  placeholder.write(':red[gaps connected...]')
  #-----------------------------------------------
  #-----------------------------------------------
  #final image
  linelist = []

  for x in matches:
    drawbetweenpoints(x[0], x[1], linelist)

  linelist = createsquare_1(linelist, 10)
  finalimage = draw_on_image(image_v2, linelist, [0, 0, 0 ])  #[255, 0, 0 ] = red,  [0,0,0] = black
  finalimage = smooth_after(finalimage)
  finalimage= thickenline_IMAGE(1, finalimage)
  #finalimage = back_to_image(finalimage)
  #-----------------------------------------------
  #-----------------------------------------------
  #visualization for gaps
  gaplist_squares = createsquare(post_filtered_gaps, 10)
  gapimage = draw_on_image(image, gaplist_squares, [255, 0, 0 ])  #[255, 0, 0 ] = red,  [0,0,0] = black
  #gapimage = back_to_image(gapimage)
  placeholder.empty()
  return finalimage, gapimage

    