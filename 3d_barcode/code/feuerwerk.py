"""feuerwerk.py — Easter Egg for the 3D-Barcode project.

This script is the hidden payload encoded in example/demo_readme_encoded.png.
Decode it with:
  python3 code/3D_Bilddatenuebertragung.py example/demo_readme_encoded.png decoded.py --decode
  python3 decoded.py

Proof of concept: any binary file — text, code, or executable — can be packed
into a pixel image. This is just the fun, harmless demonstration.
Click anywhere in the fireworks window to exit.
"""
import turtle
import random

screen = turtle.Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("3D-Barcode Easter Egg — Off-Grid ;) !?")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

colors = ["red", "yellow", "blue", "green", "white", "orange", "cyan", "magenta"]

for _ in range(30):
    t.penup()
    t.goto(random.randint(-250, 250), random.randint(-200, 200))
    t.pendown()
    t.color(random.choice(colors))
    for _ in range(36):
        t.forward(30)
        t.backward(30)
        t.right(10)

# Exit button in corner
btn = turtle.Turtle()
btn.hideturtle()
btn.penup()
btn.goto(220, 265)
btn.color("white")
btn.write("[ EXIT ]", align="right", font=("Arial", 11, "bold"))

screen.onclick(lambda x, y: turtle.bye())
turtle.done()
