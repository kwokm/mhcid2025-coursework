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
        shutdown_display()
        exit()

def display_character(name, title, id, new=False):
    if RPI_AVAILABLE:
        try:
            # Drawing on the image
            font16 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
            font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
            font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
            
            bg = Image.new('1', (epd.height, epd.width), 0)  # 255: clear the frame
            bg_draw = ImageDraw.Draw(bg)
            bg_draw.rectangle((0,0,122,122), fill = 0)
            bg_draw.rectangle((136,40,250,84), fill = 0)
            bg_draw.bitmap((0,0), Image.open(os.path.join(picdir, 'toy-bmp', f"{id}.bmp")), fill=255)
            bg_draw.text((136, 40), name, font = font16, fill = 255)
            bg_draw.text((136, 54), "the", font = font12, fill = 255)
            bg_draw.text((136, 68), title, font = font16, fill = 255)
            epd.display(epd.getbuffer(bg))
                
        except IOError as e:
            logging.info(e)
            
        except KeyboardInterrupt:    
            shutdown_display()
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
        
        # epd.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        shutdown_display()
        exit()

def shutdown_display():
    clear_display()
    epd2in13_V4.epdconfig.module_exit()