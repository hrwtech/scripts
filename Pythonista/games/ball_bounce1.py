from visual import *

g=vector(0,-9.8,0)
ball=sphere(pos=(0,1,0), radius=0.05, material=materials.shiny)

ball.p=vector(0,0,0)
ball.m=0.1
t=0
dt=0.001
floor = box(length=1, width=1, height=0.05, pos=vector(0,0,0), color=color.blue)

while True:
    rate(1000)
    F=ball.m*g
    ball.p=ball.p+F*dt
    ball.pos=ball.pos+ball.p*dt/ball.m
    if (ball.pos.y+ball.radius)<(floor.pos.y +floor.height/2):
        ball.p=-ball.p
