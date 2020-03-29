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

address = [1,1,1,1,0,0,0,0,0,0,0,0]
codes = ['AD','CC','CD','C8','E6','E7','A9']
pygame.init()
windowSurfaceObj = pygame.display.set_mode((96, 351),0, 24)
img = pygame.image.load('remote1.jpg')
windowSurfaceObj.blit(img, (0, 0))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            control = []
            z = 6
            mousex, mousey = event.pos
            if (mousex > 23 and mousex < 75) and (mousey > 5 and mousey < 45):
                # lock
                z = 4
            elif (mousex > 23 and mousex < 75) and (mousey > 90 and mousey < 109):
                #unlock
                z = 5
            elif (mousex > 24 and mousex < 75) and (mousey > 47 and mousey < 83):
                # shutter
                z = 0
            elif (mousex > 18 and mousex < 43) and (mousey > 138 and mousey < 186):
                if mousey < 163:
                    # zoom +
                    z = 1
                else:
                    # aoom -
                    z = 2
            elif (mousex > 54 and mousex < 77) and (mousey > 163 and mousey < 185):
                # start / stop
                z = 3
            elif mousey > 300:
                # quit
                pygame.quit()
                sys.exit()
            else:
                #focus
                z = 6
                
            if z < 7:
                if z == 0:
                    # focus before shutter
                    command = bin(int(codes[6], 16))[2:].zfill(7)
                    for t in range(len(command)-1,-1,-1):
                        control.append(int(command[t]))
                    for t in range(0,len(address)):
                        control.append(address[t])
                    for u in range(0,3):
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
                    control = []
                    time.sleep(.25)
                command = bin(int(codes[z], 16))[2:].zfill(7)
                for t in range(len(command)-1,-1,-1):
                    control.append(int(command[t]))
                for t in range(0,len(address)):
                    control.append(address[t])
                for u in range(0,3):
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

            
    
