import csv
import math
from PIL import Image, ImageDraw, ImageFont

PADDING = 200
#BASEHEIGHT = 200
WIDTH = 1200
HEIGHT = 1200

MAXDIMENSION = 'w'

TITLE_FONT = 'fonts/GOTHAM-BLACK.TTF'
LOCATION_FONT = 'fonts/GOTHAM-LIGHT.TTF'
DESCRIPTION_FONT = 'fonts/GOTHAM-LIGHTITALIC.TTF'

RACE = {
'ASIAN': (118,140,170,255),
'BLACK': (22,46,73,255),
'HISPANIC': (65,85,120,255),
'NATIVE': (160,181,204,255),
'UNKNOWN': (211,211,211,255),
'WHITE': (196,314,234,255)
}

BORDER_WIDTH = 120

MIN_BAR_WIDTH = 20
MAX_BAR_WIDTH = 80
BAR_AREA_WIDTH = (WIDTH*math.sqrt(2)/3)
MIN_AGE = 13
MAX_AGE = 70

age = 70
age_ratio = min(1.0,max(0.0,(age-MIN_AGE)/(MAX_AGE-MIN_AGE)))
bar_width = math.floor(MIN_BAR_WIDTH+(age_ratio*(MAX_BAR_WIDTH-MIN_BAR_WIDTH)))

#BAR_WIDTH = 20
#IMG = 'images/52.jpg'
#IMG = 'images/2210.jpg'
IMG = 'images/2278.jpg'

title_font = ImageFont.truetype(TITLE_FONT, size=20)
location_font = ImageFont.truetype(LOCATION_FONT, size=14)

with Image.new('RGBA', ((2*PADDING)+WIDTH,(2*PADDING)+HEIGHT), (255,255,255,255)) as im:
  img = Image.open(IMG).convert('RGBA')
  w,h = img.size
  if h > w:
    MAXDIMENSION = 'h'
  
  if MAXDIMENSION == 'w':
    ratio = (WIDTH*math.sqrt(2)-(WIDTH/10))/w
  else:
    ratio = (HEIGHT*math.sqrt(2)-(HEIGHT/10))/h

  img = img.resize((int(ratio*w),int(ratio*h)))
  img = img.rotate(315, expand=True)
  w,h = img.size

  draw = ImageDraw.Draw(im)
  draw.rectangle((PADDING,PADDING,PADDING+WIDTH,PADDING+HEIGHT), fill=(88,88,88))
#  im.paste(img,box=(int(PADDING-(w/2)+(WIDTH/2)+(BORDER_WIDTH/2)),int(PADDING-(h/2)+(HEIGHT/2)+(BORDER_WIDTH/2))))
  im.paste(img,box=(int(PADDING-(w/2)+(WIDTH/2)),int(PADDING-(h/2)+(HEIGHT/2))))

  #Draw Age Bars
  i = 0
  while (i*bar_width) < BAR_AREA_WIDTH:
    fill = (255,255,255) if i%2 else (0,0,0)
    draw.line((PADDING+(BORDER_WIDTH/2),PADDING+BORDER_WIDTH+(i*bar_width),PADDING+BORDER_WIDTH+(i*bar_width),PADDING+(BORDER_WIDTH/2)), fill=fill, width=bar_width)
    print(i*bar_width)
    i += 1

#  draw.line((375,625,625,375), fill=(255,255,255), width=50)
#  draw.line((475,675,675,475), fill=RACE['NATIVE'], width=200)  

  #Black Border Text
  draw.rectangle((PADDING,PADDING,PADDING+BORDER_WIDTH,PADDING+HEIGHT), fill=(0,0,0,255))
  draw.rectangle((PADDING,PADDING,PADDING+WIDTH,PADDING+BORDER_WIDTH), fill=(0,0,0,255))
  draw.text((PADDING+(BORDER_WIDTH/2),205),'Test Title', font=title_font, fill=(255,255,255))
  verttext = Image.new('RGBA',(HEIGHT,BORDER_WIDTH), (0,0,0,0))
  vertdraw = ImageDraw.Draw(verttext)
  vertdraw.text((BORDER_WIDTH,5),'Location Title', font=location_font, fill=(255,255,255))
  verttext = verttext.rotate(270, expand=True)
  im.alpha_composite(verttext,dest=(PADDING,PADDING))

  cropped = im.crop((PADDING,PADDING,PADDING+WIDTH,PADDING+HEIGHT))
  out = cropped.rotate(45, expand=True)

  w,h = out.size
  out = out.resize((int(w/3),int(h/3)))

  #cropped.save('test.png')
  out.save('test.png')
