import argparse
from turtledisplayimage import Img, setup_screen
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turtle image displaying program")
    
    parser.add_argument("path", help="Path to the input image")
    parser.add_argument("--resize", action="store_true", help="Resize the image")
    parser.add_argument("--pixelate", action="store_true", help="Pixelate the image")
    parser.add_argument("--blackandwhite", action="store_true", help="Convert the image to greyscale")
    parser.add_argument("--distortion", action="store_true", help="Distort the image")
    
    args = parser.parse_args()
    # time to draw "images/Enten.jpg" -> longer than 40 minutes -> 960.000 pixel must be drawn
    # time to draw "images/EiffelTurm.jpg" -> 22 seconds -> 120.000 pixel must be drawn
    image = Img(args.path, resize=args.resize, pixelate=args.pixelate, 
                black_and_white=args.blackandwhite, distortion=args.distortion)

    # intialization of the screen where turtle draws the image
    #   parameters: width of the screen, height of the screen
    screen = setup_screen(image.width, image.height, image.name)

    # drawing the image
    #   parameters: turtle screen
    image.draw(screen)

    screen.mainloop()
