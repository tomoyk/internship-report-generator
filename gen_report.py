#!/usr/bin/env python3

import yaml
import unicodedata
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

        def getCharSize(char):
            if unicodedata.east_asian_width(char) in 'FWA':
                return 2
            else:
                return 1

        def format_text(longtext, maxwidth):
            tmp_str = ''
            line_length = 0

            for c in longtext:
                tmp_str += c
                line_length += getCharSize(c)

                # Intercept return
                if c == '\n':
                    line_length = 0
                    continue

                # Return text
                if maxwidth-1 <= line_length:
                    tmp_str += '\n'
                    line_length = 0

            return tmp_str

        # On 'comment' property
        if k_conf_attr == 'comment':
            v_data_content[k_conf_attr] = format_text(longtext=v_data_content[k_conf_attr], maxwidth=v_conf_pos['w'])

        # On 'work' property 
        if k_conf_attr == 'work':
            # Buffer
            tmp_time = ''
            tmp_cont = ''

            for k_work_time,v_work_txt in v_data_content['work'].items():
                # Join content
                formated_text = format_text(longtext=v_work_txt, maxwidth=v_conf_pos['content']['w']) 
                tmp_cont += formated_text + '\n'

                # Join date
                break_lines = formated_text.count('\n')
                tmp_time += k_work_time + '\n'*(break_lines+1)

            write_text(v_conf_pos['time']['x'], v_conf_pos['time']['y'], tmp_time)
            write_text(v_conf_pos['content']['x'], v_conf_pos['content']['y'], tmp_cont)

            continue

        # NOTE) k_conf_attr = {year, month, day, day_of_week, ...}
        write_text(v_conf_pos['x'], v_conf_pos['y'], v_data_content[k_conf_attr])


def main():

    print("+++ Generating reports +++")
    
    # Open base-image
    IMAGE_PATH='scn_master_blank.jpeg'
    base = Image.open(IMAGE_PATH).convert('RGBA')
    
    # Open data-file
    DATA_PATH = 'data.yml'
    with open(DATA_PATH, 'r') as yml:
        data = yaml.load(yml)

    # Get each-data on data.yml
    for k_data_day,v_data_content in data.items():
        print("- Building: "+k_data_day)

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
        # out.show()

        out.save("out/"+k_data_day+".png", "PNG")


if __name__ == '__main__':
    main()
