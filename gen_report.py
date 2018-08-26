#!/usr/bin/env python3

import yaml
from PIL import Image, ImageDraw, ImageFont

def draw_data(image_obj, imagefont_obj, v_data_content):

    d = ImageDraw.Draw(image_obj)

    # Open config-file
    CONFIG_PATH = 'config.yml'
    with open(CONFIG_PATH, 'r') as yml:
        conf = yaml.load(yml)

    # Get each-settings on config.yml
    for k_conf_attr,v_conf_pos in conf['field'].items():

        # Helper method for writing
        def write_text(x, y, txt):
            d.text((x,y), str(txt), font=imagefont_obj, fill=(0,0,0,255))

        def hoge(longtext):
            MAX_WIDTH = 40//2
            tmp = ''
            for i in range(len(longtext)//MAX_WIDTH):
                tmp += longtext[MAX_WIDTH*i:MAX_WIDTH*(i+1)] + '\n'
            return tmp

        # On 'comment' or 'work' property
        if k_conf_attr == 'comment': #or k_conf_attr == 'work':
            v_data_content[k_conf_attr] = hoge(v_data_content[k_conf_attr])           

        # On 'work' property 
        if k_conf_attr == 'work':
            for k_work_time,v_work_txt in v_data_content['work'].items():
                write_text(v_conf_pos['time']['x'], v_conf_pos['time']['y'], k_work_time)
                write_text(v_conf_pos['content']['x'], v_conf_pos['content']['y'], v_work_txt)

            continue

        # NOTE) k_conf_attr = {year, month, day, day_of_week, ...}
        write_text(v_conf_pos['x'], v_conf_pos['y'], v_data_content[k_conf_attr])


def main():
    
    # Open base-image
    IMAGE_PATH='scn_master_blank.jpeg'
    base = Image.open(IMAGE_PATH).convert('RGBA')
    
    # Open data-file
    DATA_PATH = 'data.yml'
    with open(DATA_PATH, 'r') as yml:
        data = yaml.load(yml)

    # Get each-data on data.yml
    for k_data_day,v_data_content in data.items():

        # Generate image for text
        txt = Image.new('RGBA', base.size)
        # FONT_PATH='/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc'
        FONT_PATH='/Users/tkoyama/Desktop/osaka/Osaka/OsakaMono.ttf'
        fnt = ImageFont.truetype(FONT_PATH, 100)

        # Bind text on base-image
        draw_data(image_obj=txt, imagefont_obj=fnt, v_data_content=v_data_content)

        # Generate new-image
        out = Image.alpha_composite(base, txt)

        # For debug
        out.show()

        # out.save("hoge.png", "PNG")


if __name__ == '__main__':
    main()
