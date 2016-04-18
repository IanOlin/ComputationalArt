""" 
Ian Paul
Computational Art Project
Softdes 2016
"""

import random, math
from PIL import Image


#functions in lambda form
prod = lambda q, w, t: q * w
avg = lambda q, w, t : .5 * (q + w)
x = lambda q, w, t: q
y = lambda q, w, t: w
cos_pi = lambda q: math.cos(math.pi * q)
sin_pi = lambda q: math.sin(math.pi * q)
invt = lambda q: -q
half = lambda q: .5 * q
timef = lambda q, w, t: t

functions = [prod, avg, x, y, cos_pi, sin_pi, invt, half, timef]
two_args = [prod, avg, x, y, timef]
'''
These are the functions that build random funciton can choose from
prod(q,w) = qw
avg(q,w) = .5(q+w)
x(q,w) = q
y(q,w) = w
cos_pi(q) = cos(pi*q)
sin_pi(q) = sin(pi*q)
invt(q) = -q
half(q) = .5q
'''


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: The evaluation of a randomly generated function
    """
    choice = random.choice(functions) #chooses which function to implement


    #decision to end

    if min_depth < 1: #minimum depth has been reached, will choose to end or not
    	if random.choice([True, False]): #flip a coin to end
    		return random.choice([x,y, timef]) #returning only x or y to simplify evaluation
    if max_depth == 0 : #max depth reached, will end
        return random.choice([x, y, timef])#returning x or y to simplyfy evalutation

    #Recursion to generate functions

    if choice in two_args: #if the chosen function takes two arguments
        function1 = build_random_function(min_depth-1, max_depth-1)
        function2 = build_random_function(min_depth-1, max_depth-1)
    	res_function = lambda q, w, t : choice(function1(q, w, t), function2(q, w, t), timef(q,w,t))
    else: #only one argument
    	function1 = build_random_function(min_depth-1, max_depth-1)
        res_function = lambda q, w, t: choice(function1(q, w, t))

    return res_function


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    scale = abs(float((output_interval_end - output_interval_start))/float((input_interval_start - input_interval_end)))
    #find the scaling between the two intervals
    shift = (val-input_interval_start)*scale
    #find the ofset between the two intervals
    return shift+output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def generate_art(basename, time, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    frames = range(time)
    for frame in frames:
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                t = remap_interval(frame, 0, time, -1, 1)
                pixels[i, j] = (
                        color_map(red_function(x, y, t)),
                        color_map(green_function(x, y, t)),
                        color_map(blue_function(x, y, t))
                        )
        filename = basename + '_frame_{:3d}'.format(frame) + '.png'
        im.save(filename)

def generate_bulk_art(basename,number):
    """
    Generate a bulk set of computational art and save them as .pngs.

    basename: a string that will have a number appended to it (title of set)
    number: number of pieces to generate
    """
    for i in range(number):
        generate_art(basename + str(i) + '.png',1920,1080)

def generate_movie(basename,frames):
    """
    Generate a bulk set of computational art and save them as .pngs.

    basename: a string that will have a number appended to it (title of set)
    frames: number of pieces to generate
    """
    generate_art(basename,frames, 400,400)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    movie_length = 200
    generate_movie('movie_test', movie_length)

