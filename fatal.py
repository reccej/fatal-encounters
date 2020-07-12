import csv
import math
import os
import textwrap
from os import path
import glob
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1200
HEIGHT = 1200

TITLE_FONT = 'fonts/GOTHAM-BLACK.TTF'
TITLE_FONT_SIZE = 60
LOCATION_FONT = 'fonts/GOTHAM-LIGHTITALIC.TTF'
LOCATION_FONT_SIZE = 42
DESCRIPTION_FONT = 'fonts/GOTHAM-LIGHT.TTF'
DESCRIPTION_FONT_SIZE = 32

RACE = {
'ASIAN': (118,140,170,255),
'BLACK': (22,46,73,255),
'HISPANIC': (65,85,120,255),
'NATIVE': (160,181,204,255),
'UNKNOWN': (211,211,211,255),
'WHITE': (196,314,234,255)
}
BORDER_COLOR = RACE['WHITE']
BORDER_WIDTH = int(WIDTH/12)
INFO_BOX_DIMENSIONS = (900,900)
INFO_BOX_PADDING = 12

OUT_DIR = 'out'
IMAGE_FOLDER = 'images'
DATA = 'fatalencounters.csv'

title_font = ImageFont.truetype(TITLE_FONT, size=TITLE_FONT_SIZE)
location_font = ImageFont.truetype(LOCATION_FONT, size=LOCATION_FONT_SIZE)
description_font = ImageFont.truetype(DESCRIPTION_FONT, size=DESCRIPTION_FONT_SIZE)

with open(DATA) as fin:
  reader = csv.DictReader(fin)
  for row in reader:
    image_matches = glob.glob(path.join(IMAGE_FOLDER,row['Unique ID'] + '.*'))
    image_path = image_matches[0] if len(image_matches) > 0 else ''
    if image_path != '':
      #Obtain race from info and choose border color accordingly
      race = row['Subject\'s race with imputations'].lower()
      if 'white' in race:
        border_color = RACE['WHITE']
      elif 'black' in race:
        border_color = RACE['BLACK']
      elif 'hispanic' in race:
        border_color = RACE['HISPANIC']
      elif 'native american' in race:
        border_color = RACE['NATIVE']
      elif 'asian' in race:
        border_color = RACE['ASIAN']
      else:
        border_color = RACE['UNKNOWN']
       
      try:
        with Image.new('RGBA', (WIDTH,HEIGHT), border_color) as im:
          draw = ImageDraw.Draw(im)

          #Background Color
          draw.rectangle((BORDER_WIDTH,BORDER_WIDTH,WIDTH-BORDER_WIDTH,HEIGHT-BORDER_WIDTH), fill=(0,0,0))
  
          #Open Image
          img = Image.open(image_path).convert('RGBA')
          #Calculate resize dimensions while preserving original image ratio
          w,h = img.size
          if h > w:
            ratio = (HEIGHT-(BORDER_WIDTH*2))/h
          else:
            ratio = (WIDTH-(BORDER_WIDTH*2))/w
          img = img.resize((int(ratio*w),int(ratio*h)))
  
          #Paste image centered in the bounding box
          w,h = img.size
          im.paste(img, box=(int((WIDTH-w)/2),int((HEIGHT-h)/2)))

          #Create info box -- use alpha value to control opacity
          with Image.new('RGBA', (INFO_BOX_DIMENSIONS[0], INFO_BOX_DIMENSIONS[1]), (255,255,255,140)) as info:
            info_draw = ImageDraw.Draw(info)

            #Textwrap.fill wraps the text with newline characters every n=width characters
            title_text = textwrap.fill(row['Subject\'s name'], width=24)
            info_draw.text((INFO_BOX_PADDING,INFO_BOX_PADDING),title_text, font=title_font, fill=(0,0,0))

            #Calculate position of text according to how many lines of text are in title
            location_text = textwrap.fill(row['Location of death (city)'] + ', ' + row['Location of death (state)'] + '. ' + row['Date of injury resulting in death (month/day/year)'], width=40)
            location_pos = (INFO_BOX_PADDING)+(TITLE_FONT_SIZE*(title_text.count('\n')+1))
            info_draw.text((INFO_BOX_PADDING,location_pos), location_text, font=location_font, fill=(0,0,0))

            description_text = textwrap.fill(row['A brief description of the circumstances surrounding the death'], width=52)
            description_pos = (INFO_BOX_PADDING*2)+(TITLE_FONT_SIZE*(title_text.count('\n')+1))+(LOCATION_FONT_SIZE*(location_text.count('\n')+1))
            info_draw.text((INFO_BOX_PADDING,description_pos),description_text, font=description_font, fill=(0,0,0))

            #Calculates approximately how many pixels of height were used in total by text to crop the description box down
            total_line_count = title_text.count('\n')+location_text.count('\n')+description_text.count('\n')
            height_padding = max(0,INFO_BOX_DIMENSIONS[1]-((INFO_BOX_PADDING*3)-(total_line_count*2))-(TITLE_FONT_SIZE*(title_text.count('\n')+1))-(LOCATION_FONT_SIZE*(location_text.count('\n')+1))-(DESCRIPTION_FONT_SIZE*(description_text.count('\n')+1)))

            #Overlay the info box on top of the image
            im.alpha_composite(info,dest=(WIDTH-INFO_BOX_DIMENSIONS[0],HEIGHT-INFO_BOX_DIMENSIONS[1]+height_padding))

          #Resize by 1/2 for anti-aliasing
          out = im.resize((int(WIDTH/2),int(HEIGHT/2)))
          out.save(path.join(OUT_DIR,row['Unique ID'] + '.png'))
      except Exception as e:
#        print(e, type(e).__name__)
        continue
