# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import turtle as t

def draw_square():
    window = t.Screen()
    window.bgcolor("red")
    
    brad = t.Turtle()
    brad.shape(name = "turtle")
    brad.speed(2)
    brad.color("yellow")
    
    brad.fd(100)
    brad.right(90)
    brad.fd(100)
    brad.right(90)
    brad.fd(100)
    brad.right(90)
    brad.fd(100)
    
    angle = t.Turtle()
    angle.shape("Arrow")
    angle.color("blue")
    angle.circle(100)
    
    
    window.exitonclick()
    
    
draw_square()