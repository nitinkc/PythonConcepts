# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import turtle as t

def draw_square(brad):
    for i in range(4):
        brad.fd(100)
        brad.right(90)
    
def draw_circle(angle):
    angle.circle(100)
        
def main():
    
    window = t.Screen()
    window.bgcolor("red")
    
#    brad = t.Turtle()
#    brad.shape(name = "turtle")
#    brad.speed(16)
#    brad.color("yellow")
#    for i in range(1,36):
#        draw_square(brad)
#        brad.right(10)
    
    angle = t.Turtle()
    angle.shape("turtle")
    angle.color("blue")
    angle.speed(16)
    for i in range(1,72):
        draw_circle(angle)
        angle.right(5)
    
    window.exitonclick()



main()        