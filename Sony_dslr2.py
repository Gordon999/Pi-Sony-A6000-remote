#!/usr/bin/env python3
import pygame, sys
from pygame.locals import *
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
out_pin = 36
GPIO.setup(out_pin,GPIO.OUT)
p = GPIO.PWM(out_pin, 40000)
p.start(0)

camera = [0,1,0,1,1,1,0,0,0,1,1,1,1]
data = ['2D','14','20','3C','38','3E','11','37','1B','32','47','3A','39','3B','48','4A','00','4B','3D','3F']
pygame.init()
windowSurfaceObj = pygame.display.set_mode((183, 400),0, 24)
img = pygame.image.load('sony_rmt_dslr2.jpg')
windowSurfaceObj.blit(img, (0, 0))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            z = 20
            control = []
            mousex, mousey = event.pos
            if mousey > 320:
                sys.exit()
            x = int((mousex-34)/44)
            y = int((mousey-40)/40)
            if x == 2 and (mousey > 98 and mousey < 173):
                if mousey < 135:
                    y = 1
                else:
                    y = 3
            z = (x*7) + y
            if z < 20:
                command = bin(int(data[z], 16))[2:].zfill(7)
                for t in range(len(command)-1,-1,-1):
                    control.append(int(command[t]))
                for t in range(0,len(camera)):
                    control.append(camera[t])
                for u in range(0,5):
                    p.ChangeDutyCycle(25) 
                    time.sleep(0.0024)
                    p.ChangeDutyCycle(0) 
                    time.sleep(0.0006)
                    for v in range(0,len(control)):
                        p.ChangeDutyCycle(25)
                        time.sleep(0.0006 + (control[v] * 0.0006))
                        p.ChangeDutyCycle(0) 
                        time.sleep(0.0006)
                    time.sleep(0.0045)
            
    
