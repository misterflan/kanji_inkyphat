import requests
from random import choice
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
from bs4 import BeautifulSoup
from font_fredoka_one import FredokaOne

inky_display = InkyPHAT("red")

# Scrape and get informationi
urls = ['http://www.kanji-a-day.com/level1/index.php', 'http://www.kanji-a-day.com/level2/index.php', 'http://www.kanji-a-day.com/level3/index.php', 'http://www.kanji-a-day.com/level4/index.php']
res = requests.get(choice(urls))
soup = BeautifulSoup(res.content, "lxml")
kanji = soup.find("div", {"class":"glyph"})
kun = soup.find("ul", {"class":"kun-reading"})
meaning = soup.find("ul", {"class":"meaning"})

# split meaning up so it can fit
mean = (meaning.contents[3].text).split(",")
pmean = "Meaning: \n" + mean[0] + "," + mean[1]

# Select Kanji for printing
ka = kanji.contents[0]

# Select Hirigana
ku = ((kun.contents[3].text).strip().split('\xa0')[0])

# Define fonts and sizes
kanjifont=ImageFont.truetype("corp_round_v1.ttf",50)
unicodefont=ImageFont.truetype("corp_round_v1.ttf",30)
normal=ImageFont.truetype(FredokaOne,22)

# Do drawing things
image = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(image)

y_top = int(inky_display.HEIGHT * (5.0 / 10.0))
y_bottom = y_top + int(inky_display.HEIGHT * (4.0 / 10.0))

# Paint it black
for y in range(0, inky_display.height):
    for x in range(0, inky_display.width):
        image.putpixel((x, y), inky_display.BLACK)

# Write the text
draw.text((100,-30), ka, inky_display.RED, font=kanjifont)
draw.text((10,15), ku, inky_display.RED, font=unicodefont)
draw.text((10,45), pmean, inky_display.WHITE, font=normal)

# Display the text!
inky_display.set_image(image)
inky_display.show()
