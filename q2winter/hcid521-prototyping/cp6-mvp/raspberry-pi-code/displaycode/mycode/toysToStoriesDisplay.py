#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

try:
    import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
    GPIO.setwarnings(False)  # Ignore warning for now
    GPIO.setmode(GPIO.BOARD)   # Use BCM pin numbering to match your pin definitions
    from waveshare_epd import epd2in13_V4
    from PIL import Image,ImageDraw,ImageFont
    RPI_AVAILABLE = True
    epd = epd2in13_V4.EPD()
    epd.init()
except ImportError:
    print("RPi.GPIO module not available. Running in keyboard-only mode.")
    RPI_AVAILABLE = False

import logging
import time
import traceback

# logging.basicConfig(level=logging.DEBUG)

def clear_display():
    epd.Clear(0xFF)
    # epd.sleep()

def display_toys_to_stories(word1, word2, word3, word4):
    try:
        # Drawing on the image
        font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        # draw divider lines
        draw.line([(125,0),(125,113)], fill = 0,width = 1)
        draw.line([(0,57),(250,57)], fill = 0,width = 1)
        # top row
        draw.text((16, 16), word1, font = font15, fill = 0)
        draw.text((141, 16), word2, font = font15, fill = 0)
        # bottom row
        draw.text((16, 73), word3, font = font15, fill = 0)
        draw.text((141, 73), word4, font = font15, fill = 0)
        epd.display(epd.getbuffer(image))
        
        # logging.info("Goto Sleep...")
        # epd.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in13_V4.epdconfig.module_exit()
        exit()

def display_character(name, title, id):
    if RPI_AVAILABLE:
        try:
            # Drawing on the image
            font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
            font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

            image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
            draw = ImageDraw.Draw(image)
            draw.bitmap((0,0), Image.open(os.path.join(picdir, 'toy-bmps', f"{id}.bmp")), fill=0)
            draw.text((78, 53), name + " the " + title, font = font15, fill = 0)
            epd.display(epd.getbuffer(image))
                
        except IOError as e:
            logging.info(e)
            
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd2in13_V4.epdconfig.module_exit()
            exit()
    else:
        print("RPi.GPIO module not available. Running in keyboard-only mode.")
        return

def display_loading():
    try:
        logging.info("Toys to Stories Display Control")

        # Drawing on the image
        font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)
        draw.text((16, 16), "Loading...", font = font15, fill = 0)
        epd.display(epd.getbuffer(image))
        
        logging.info("Goto Sleep...")
        # epd.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd2in13_V4.epdconfig.module_exit()
        exit()

def shutdown_display():
    epd2in13_V4.epdconfig.module_exit()