# author: Mark, 30.11.2022

"""
Portions of this software are copyright © 2022 The FreeType
Project (www.freetype.org).  All rights reserved.
"""

# PIL
# a library which can return information about an image
# in this program I use:
#   size of the image
#   color of every pixel in the image

# depending on which Python version the user has installed, 
# a different library must be imported

# getting the version
import sys
python_version = sys.version.split(".")[1]

# importing the image library

from PIL import Image
from turtle import *
import time, math
from datetime import timedelta

def setup_screen(image_width: int, image_height: int, title: str) -> None:
    # creating a screen
    screen = Screen()
    screen.title(title)
    # screen can not be resized by the user
    screen.cv._rootwindow.resizable(False, False)

    # color is specified in RGB
    screen.colormode(255)

    # preventing that a scroll bar appears when the width or the height of the screen is lower than 420
    if image_width < 420 or image_height < 420:
        screen.setup(420, 420)
    else:
        screen.setup(image_width, image_height)

    return screen

def turtle_set_position(turtle: Turtle, position: tuple) -> None:
    # turtle teleports to a position without drawing a line
    turtle.penup()
    turtle.setpos(position[0], position[1])
    turtle.pendown()

class Img:
    def __init__(self, path_to_image: str, resize: bool = False, pixelate: bool = False, black_and_white: bool = False, distortion: bool = False) -> None:
        self.path = path_to_image

        # draw image in grey
        self.black_and_white = black_and_white

        # create a distortion effect
        self.distortion = distortion

        # load relevant image data
        self.load(self.path)

        # reduce size of image
        if resize: 
            self.resize()

        # pixelate the image
        if pixelate:
            self.pixelate()

        # only allow spefic sizes of images
        if not 64 <= self.width <= 1900 or not 64 <= self.height <= 1000:
            print("The size of the image is not allowed")
            input()
            exit()

    def load(self, path: str) -> None:
        self.name = self.path.split("/")[-1]

        # intialization of the image in PIL
        self.image_object = Image.open(path)
        
        # creating an image which contains the RGB information of every pixel
        self.rgb_image = self.image_object.convert('RGB')

        self.width, self.height = self.image_object.size

    def resize(self) -> None:
        # downsize the image
        image = self.image_object.resize((int(self.width * 0.5), int(self.height * 0.5)))
        
        path = "images/resized_images/rs_" + self.name
        # saving resized image
        image.save(path, optimize=True, quality=95)

        self.load(path)

    def pixelate(self):
        # resize smoothly down to 64x64 pixels
        small_image = self.image_object.resize((64,64), resample=Image.Resampling.BILINEAR)

        # scale back up to original size
        result = small_image.resize((self.width, self.height), Image.Resampling.NEAREST)

        path = "images/pixelated_images/px_" + self.name

        # save
        result.save(path)

        self.load(path)

    def get_gray_pixel_color(self, pixel_color_values: tuple) -> tuple:

        cross_sum_of_the_values = pixel_color_values[0] + pixel_color_values[1] + pixel_color_values[2]

        grey_percentage = cross_sum_of_the_values / (255 * 3)
        grey_pixel_color_value = round(255 * grey_percentage)

        return (grey_pixel_color_value, grey_pixel_color_value, grey_pixel_color_value)

    def print_drawing_status(self, drawing_status_in_percent: int) -> None:
        # prints a bar which shows the progress of the drawing process
        
        # symbol representing an empty slot
        empty_symbol = "-"

        # symbol representing an occupied slot
        filled_synbol = "#"

        # number of individual symbols in the bar
        number_of_total_symbols = 10
        number_of_occupied_slots = round(drawing_status_in_percent/number_of_total_symbols)

        # printing the bar to the console
        print(">>   [", end="")
        for i in range(number_of_occupied_slots):
            # "end" does not create a line break
            print(filled_synbol, end="")

        for i in range(number_of_total_symbols - number_of_occupied_slots):
            print(empty_symbol, end="")

        # printing the status as a number
        print("] >> {} % done".format(str(drawing_status_in_percent)))

    def print_information(self) -> None:
        # printing information to the user
        print(">>   name: {}".format(self.name))
        print(">>   size: {} * {}".format(self.width, self.height))
        print(">>")

    def print_draw_time(self, starting_time: float) -> None:
        # calculating the time Turtle needed to draw the image
        drawing_time_in_seconds = round(time.perf_counter() - starting_time, 2)

        # printing information for the user
        better_time_format = str(timedelta(seconds=round(drawing_time_in_seconds)))
        print(">>")
        print(">>   Turtle finished the drawing in {}".format(better_time_format))


    def draw(self, screen: Screen) -> None:
        
        self.print_information()

        # time.perf_counter() returns a number, which increases every second
        # saving time.perf_counter() to calculate the passed time after the drawing is done
        
        starting_time = time.perf_counter()

        # creating a turtle which draws the image
        turtle = Turtle()

        # turtle is not visible on the screen
        turtle.hideturtle()

        # turtle has the fastest speed
        turtle.speed(0)

        # turtle updates the screen after every single action it does
        # in order to improve the speed of the program, 
        # turtle._tracer(0, 0) deactivates this feature of turtle
        turtle._tracer(0, 0)

        # going through every pixel by using 2 for loops
        for y in range(self.height):

            # the positions in turtle work like in a coordinate system
            # turtle starts at the top left corner and moves down the y-axis
            # every line turtle's y coordinate is reduced by 1 

            turtle_pos_y = self.height/2 - y
            turtle_pos_x = -self.width/2 + math.sin(0.5 * y) * 2 if self.distortion else -self.width/2

            turtle_set_position(turtle, (turtle_pos_x, turtle_pos_y))

            # turtle draws every pixel in the line
            for x in range(self.width):
                # do not reset the pencolor if the next pixel has the same color
                if x + y == 0 or not pixel_color == self.rgb_image.getpixel((x, y)):
                    # getting the rgb value of the pixel
                    pixel_color = self.rgb_image.getpixel((x, y))

                    # checking if user decides to draw a grey black and white image
                    if self.black_and_white:
                        # get new color
                        pixel_color = self.get_gray_pixel_color(pixel_color)
                        # setting turtle's pencolor to a new color

                    # setting turtle's pencolor to a new color
                    turtle.pencolor(pixel_color[0], pixel_color[1], pixel_color[2])

                # drawing a pixel by moving one step forward
                turtle.forward(1)

            # printing the drawing status to the console when one additional percent of the drawing is done
            if y % round(self.height * 0.01) == 0:
                # calculating the percentage
                percentage_done = round(100 * (y/self.height))

                # printing the message
                # print(">> {} % done".format(str(percentage_done + 1)))
                self.print_drawing_status(percentage_done)

            # updating the screen every 6 percent instead of every pixel because
            # turtle does not update the screen by himself
            # -> improvement of the speed of the programm
            if y % round(self.height * 0.05) == 0:
                screen.update()

        self.print_draw_time(starting_time)