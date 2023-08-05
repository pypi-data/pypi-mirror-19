#!/usr/bin/env python3


#This script deals with color conversions, color transformations, and generating color scales.
#
#copyright (C) 2014-2017  Martin Engqvist | martin_engqvist@hotmail.com
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#LICENSE:
#
#colcol is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#colcol is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Library General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software Foundation,
#Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#





import re
import colorsys



#standard color names
colors={'aliceblue':'#F0F8FF',
'antiquewhite':'#FAEBD7',
'aqua':'#00FFFF',
'aquamarine':'#7FFFD4',
'azure':'#F0FFFF',
'beige':'#F5F5DC',
'bisque':'#FFE4C4',
'black':'#000000',
'blanchedalmond':'#FFEBCD',
'blue':'#0000FF',
'blueviolet':'#8A2BE2',
'brown':'#A52A2A',
'burlywood':'#DEB887',
'cadetblue':'#5F9EA0',
'chartreuse':'#7FFF00',
'chocolate':'#D2691E',
'coral':'#FF7F50',
'cornflowerblue':'#6495ED',
'cornsilk':'#FFF8DC',
'crimson':'#DC143C',
'cyan':'#00FFFF',
'darkblue':'#00008B',
'darkcyan':'#008B8B',
'darkgoldenrod':'#B8860B',
'darkgrey':'#A9A9A9',
'darkgreen':'#006400',
'darkkhaki':'#BDB76B',
'darkmagenta':'#8B008B',
'darkolivegreen':'#556B2F',
'darkorange':'#FF8C00',
'darkorchid':'#9932CC',
'darkred':'#8B0000',
'darksalmon':'#E9967A',
'darkseagreen':'#8FBC8F',
'darkslateblue':'#483D8B',
'darkslategrey':'#2F4F4F',
'darkturquoise':'#00CED1',
'darkviolet':'#9400D3',
'deeppink':'#FF1493',
'deepskyblue':'#00BFFF',
'dimgray':'#696969',
'dimgrey':'#696969',
'dodgerblue':'#1E90FF',
'firebrick':'#B22222',
'floralwhite':'#FFFAF0',
'forestgreen':'#228B22',
'fuchsia':'#FF00FF',
'gainsboro':'#DCDCDC',
'ghostwhite':'#F8F8FF',
'gold':'#FFD700',
'goldenrod':'#DAA520',
'gray':'#808080',
'grey':'#808080',
'green':'#008000',
'greenyellow':'#ADFF2F',
'honeydew':'#F0FFF0',
'hotpink':'#FF69B4',
'indianred':'#CD5C5C',
'indigo':'#4B0082',
'ivory':'#FFFFF0',
'khaki':'#F0E68C',
'lavender':'#E6E6FA',
'lavenderblush':'#FFF0F5',
'lawngreen':'#7CFC00',
'lemonchiffon':'#FFFACD',
'lightblue':'#ADD8E6',
'lightcoral':'#F08080',
'lightcyan':'#E0FFFF',
'lightgoldenrodyellow':'#FAFAD2',
'lightgrey':'#D3D3D3',
'lightgreen':'#90EE90',
'lightpink':'#FFB6C1',
'lightsalmon':'#FFA07A',
'lightseagreen':'#20B2AA',
'lightskyblue':'#87CEFA',
'lightslategrey':'#778899',
'lightsteelblue':'#B0C4DE',
'lightyellow':'#FFFFE0',
'lime':'#00FF00',
'limegreen':'#32CD32',
'linen':'#FAF0E6',
'magenta':'#FF00FF',
'maroon':'#800000',
'mediumaquamarine':'#66CDAA',
'mediumblue':'#0000CD',
'mediumorchid':'#BA55D3',
'mediumpurple':'#9370DB',
'mediumseagreen':'#3CB371',
'mediumslateblue':'#7B68EE',
'mediumspringgreen':'#00FA9A',
'mediumturquoise':'#48D1CC',
'mediumvioletred':'#C71585',
'midnightblue':'#191970',
'mintcream':'#F5FFFA',
'mistyrose':'#FFE4E1',
'moccasin':'#FFE4B5',
'navajowhite':'#FFDEAD',
'navy':'#000080',
'oldlace':'#FDF5E6',
'olive':'#808000',
'olivedrab':'#6B8E23',
'orange':'#FFA500',
'orangered':'#FF4500',
'orchid':'#DA70D6',
'palegoldenrod':'#EEE8AA',
'palegreen':'#98FB98',
'paleturquoise':'#AFEEEE',
'palevioletred':'#DB7093',
'papayawhip':'#FFEFD5',
'peachpuff':'#FFDAB9',
'peru':'#CD853F',
'pink':'#FFC0CB',
'plum':'#DDA0DD',
'powderblue':'#B0E0E6',
'purple':'#800080',
'rebeccapurple':'#663399',
'red':'#FF0000',
'rosybrown':'#BC8F8F',
'royalblue':'#4169E1',
'saddlebrown':'#8B4513',
'salmon':'#FA8072',
'sandybrown':'#F4A460',
'seagreen':'#2E8B57',
'seashell':'#FFF5EE',
'sienna':'#A0522D',
'silver':'#C0C0C0',
'skyblue':'#87CEEB',
'slateblue':'#6A5ACD',
'slategrey':'#708090',
'snow':'#FFFAFA',
'springgreen':'#00FF7F',
'steelblue':'#4682B4',
'tan':'#D2B48C',
'teal':'#008080',
'thistle':'#D8BFD8',
'tomato':'#FF6347',
'turquoise':'#40E0D0',
'violet':'#EE82EE',
'wheat':'#F5DEB3',
'white':'#FFFFFF',
'whitesmoke':'#F5F5F5',
'yellow':'#FFFF00',
'yellowgreen':'#9ACD32'}



def is_rgb(in_col):
	'''
	Check whether input is a valid RGB color.
	Return True if it is, otherwise False.
	'''
	if len(in_col) == 3 and type(in_col) == tuple:
		if 0<=in_col[0]<=255 and 0<=in_col[1]<=255 and 0<=in_col[2]<=255:
			return True
		else:
			return False
	else:
		return False


def is_hex(in_col):
	'''
	Check whether an input string is a valid hex value.
	Return True if it is, otherwise False.
	'''
	if type(in_col) is not str:
		return False
		
	regular_expression = re.compile(r'''^ #match beginning of string
					    [#]{1} #exactly one hash
	                         		[0-9a-fA-F]{6}	#exactly six of the hex symbols  0 to 9, a to f (big or small)
						$ #match end of string
						''', re.VERBOSE)	
	
	if regular_expression.match(in_col) == None:
		return False
	else:
		return True


def is_hsl(in_col):
	'''
	Check whether an input is a valid HSL color.
	Return True if it is, otherwise False.
	'''
	if len(in_col) == 3 and type(in_col) == tuple:
		if 0<=in_col[0]<=360 and 0<=in_col[1]<=100 and 0<=in_col[2]<=100:
			return True
		else:
			return False
	else:
		return False


	
def rgb_to_hex(rgb):
	'''
	Convert RGB colors to hex.
	Input should be a tuple of integers (R, G, B) where each is between 0 and 255.
	Output is a string representing a hex numer. For instance '#FFFFFF'.
	''' 
	#make sure input is ok
	assert is_rgb(rgb) is True, 'Error, %s is not a valid RGB color.' % str(rgb)
	
	#make conversion
	return "#%02x%02x%02x" % rgb

	
	
def hex_to_rgb(in_col):
	'''
	Convert a hex color to RGB.
	Input should be a string. For example '#FFFFFF'.
	Output is a tuple of integers (R, G, B).
	'''
	#make sure input is ok
	assert is_hex(in_col) is True, 'Error, %s is not a valid hex color.' % in_col
	
	#make the conversion
	in_col = in_col.lstrip('#')
	return tuple([int(in_col[s:s+2], 16) for s in range(0, len(in_col), 2)])
	

def rgb_to_hsl(in_col):
	'''
	Convert RGB colors to HSL.
	Input should be a tuple of integers (R, G, B) where each is between 0 and 255.
	Output is a tuple of integers where h is between 0 and 360 and s and l are between 0 and 100. For instance: (162, 47, 39).
	'''
	assert is_rgb(in_col), 'Error, %s is not a valid RGB color.' % str(in_col)

	# Convert each RGB integer to a float between 0 and 1
	r, g, b = [x/255. for x in in_col] 

	# RGB -> HLS
	h, l, s = colorsys.rgb_to_hls(r, g, b)

	#convert it back to the appropriate integers
	h = int(round(360*h))
	l = int(round(100*l))
	s = int(round(100*s))

	return (h, s, l) 


def hsl_to_rgb(in_col):
	'''
	Convert HSL colors to RGB.
	Input should be a tuple of integers where h is between 0 and 360 and s and l are between 0 and 100. For instance: (162, 47, 39).
	Output is a tuple of integers (R, G, B) where each is between 0 and 255.
	'''
	assert is_hsl(in_col), 'Error, %s is not a valid HSL color.' % str(in_col)

	#assign to variables
	h, s, l = in_col

	# Convert each HSL integer to a float between 0 and 1
	h = h/360.0
	s = s/100.0
	l = l/100.0

	# RGB -> HLS
	r, g, b = colorsys.hls_to_rgb(h, l, s)

	#convert it back to the appropriate integers
	r = int(round(255*r))
	g = int(round(255*g))
	b = int(round(255*b))

	return (r, g, b) 	



def hex_to_hsl(in_col):
	'''
	Convert a hex color to hsl.
	Input should be a string. For example '#FFFFFF'.
	Output is a tuple of ...... . For instance: (h, s, l).
	'''
	return rgb_to_hsl(hex_to_rgb(in_col))


def hsl_to_hex(in_col):
	'''
	'''
	return rgb_to_hex(hsl_to_rgb(in_col))
	


	
	
def mix_colors(col1, col2):
	'''
	Mix two colors and return the result.
	The input colors can be either RGB or hex.
	It is also possible to use one RGB value and one hex value.
	'''
	color_dict = scale(col1, col2, white_mid=False)
	return color_dict[50]
	

def complementary(in_col):
	'''
	Returns input color and its complementary color as a list of hex or rgb values, depending on what was submitted.

		O
	   x x
	  x   x
	 x     x
	  x   x
	   x x
		O

	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'

	hex_color = is_hex(in_col) #check whether input is hex
	if hex_color: #if it is, make it RGB
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	h, l, s = colorsys.rgb_to_hls(r, g, b)     

	# Rotation by 180 degrees
	h = (h+0.5)
	color = [int(round(x*255)) for x in colorsys.hls_to_rgb(h, l, s)] # H'LS -> new RGB

	if hex_color:
		colors = [rgb_to_hex(in_col), rgb_to_hex(tuple(color))]
	else:
		colors = [in_col, tuple(color)]

	return colors



def split_complementary(in_col):
	'''
	Returns input color and its split complementary colors (those adjecent to the complement) 
	as a list of of hex or rgb values, depending on what was submitted.

		x
	   O O
	  x   x
	 x     x
	  x   x
	   x x
		O


	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'

	hex_color = is_hex(in_col) #check whether input is hex
	if hex_color: #if it is, make it RGB
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	h, l, s = colorsys.rgb_to_hls(r, g, b)     

	# Rotation by 150 degrees
	angle = 150/360.0
	h_list = [(h+ang) % 1 for ang in (-angle, angle)]
	print(h)
	analagous = [[int(round(x*255)) for x in colorsys.hls_to_rgb(h, l, s)] for h in h_list] # H'LS -> new RGB

	#add all the colors together
	colors = [tuple(analagous[0]), in_col, tuple(analagous[1])]

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(s) for s in colors]

	return colors




def triadic(in_color):
	'''
	Returns input color as well as the two triadic colors as a list of hex or rgb values, depending on what was submitted.

		x
	   x x
	  O   O
	 x     x
	  x   x
	   x x
		O

	#first color is wrong!

	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'

	hex_color = is_hex(in_col) #check whether input is hex
	if hex_color: #if it is, make it RGB
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	h, l, s = colorsys.rgb_to_hls(r, g, b)     

	# Rotation by 120 degrees
	angle = 120/360.0
	h_list = [(h+ang) % 1 for ang in (-angle, angle)]
	print(h)
	analagous = [[int(round(x*255)) for x in colorsys.hls_to_rgb(h, l, s)] for h in h_list] # H'LS -> new RGB

	#add all the colors together
	colors = [tuple(analagous[0]), in_col, tuple(analagous[1])]

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(s) for s in colors]

	return colors





def square(in_col):
	'''
		O
	   x x
	  x   x
	 O     O
	  x   x
	   x x
		O
	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'

	hex_color = is_hex(in_col) #check whether input is hex
	if hex_color: #if it is, make it RGB
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	h, l, s = colorsys.rgb_to_hls(r, g, b)     

	# Rotation by 90 degrees
	angle = 90/360.0
	h_list = [(h+ang) % 1 for ang in (-angle, angle, angle*2)]
	print(h)
	analagous = [[int(round(x*255)) for x in colorsys.hls_to_rgb(h, l, s)] for h in h_list] # H'LS -> new RGB

	#add all the colors together
	colors = [tuple(analagous[0]), in_col, tuple(analagous[1]), tuple(analagous[2])]

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(s) for s in colors]

	return colors


def tetradic(in_col):
	'''


		O
	   x x
	  x   O
	 x     x
	  O   x
	   x x
		O
	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'

	hex_color = is_hex(in_col) #check whether input is hex
	if hex_color: #if it is, make it RGB
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	h, l, s = colorsys.rgb_to_hls(r, g, b)     

	# Rotation by 30 degrees
	angle = 30/360.0
	h_list = [(h+ang) % 1 for ang in (-angle*2, angle*4, angle*6)]
	print(h)
	analagous = [[int(round(x*255)) for x in colorsys.hls_to_rgb(h, l, s)] for h in h_list] # H'LS -> new RGB

	#add all the colors together
	colors = [tuple(analagous[0]), in_col, tuple(analagous[1]), tuple(analagous[2])]

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(s) for s in colors]

	return colors


def analagous(in_col):
	'''
	Returns the input color as well as its analagous colors.

		x
	   x x
	  x   x
	 x     x
	  x   x
	   O O
		O

	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'

	hex_color = is_hex(in_col) #check whether input is hex
	if hex_color: #if it is, make it RGB
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	h, l, s = colorsys.rgb_to_hls(r, g, b)     

	# Rotation by 30 degrees
	degree = 30/360.0
	h = [(h+angle) % 1 for angle in (-degree, degree)]
	analagous = [[int(round(x*255)) for x in colorsys.hls_to_rgb(hi, l, s)] for hi in h] # H'LS -> new RGB

	#add all the colors together
	colors = [tuple(analagous[0]), in_col, tuple(analagous[1])]

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(tuple(s)) for s in colors]

	return colors



def similar():
	'''
	Returns the input color as well as similar colors.
	'''
	pass



def monochromatic():
	'''
	Returns the input color as well as ....
	'''
	pass


def tints(in_col, number=10):
	'''
	Returns input color as well as tints of that color (lighter colors).
	number specifies how many new ones to return.
	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'
	assert type(number) is int, 'Error, the input number must be an integer.'
	assert (2 <= number and number <= 1000), 'Error, the input number must be between 2 and 1000'

	#check whether input is hex, if it is, make it RGB
	hex_color = is_hex(in_col) 
	if hex_color:
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b) 

	#what is the difference of 100% lightness and the current value	
	diff = 1.0-lightness 
	
	#devide the difference on a step size
	step = diff/float(number)

	#use that step size to generate the 10 increasing lightness values	
	lightness_list = [lightness + step*s for s in range(1, number+1)]

	#add the input color to a list, then build the 10 new HSL colors, convert to RGB and save in the same list
	colors = [in_col]
	colors.extend([[int(round(x*255)) for x in colorsys.hls_to_rgb(hue, l, saturation)] for l in lightness_list])

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(tuple(s)) for s in colors]

	return colors




def shades(in_col, number=10):
	'''
	Returns input color as well as shades of that color (darker colors).
	number specifies how many new ones to return.
	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'
	assert type(number) is int, 'Error, the input number must be an integer.'
	assert (2 <= number and number <= 1000), 'Error, the input number must be between 2 and 1000'

	#check whether input is hex, if it is, make it RGB
	hex_color = is_hex(in_col) 
	if hex_color:
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b) 
	
	#devide the difference on a step size
	step = lightness/float(number)

	#use that step size to generate the 10 increasing lightness values	
	lightness_list = [lightness - step*s for s in range(1, number+1)]

	#add the input color to a list, then build the 10 new HSL colors, convert to RGB and save in the same list
	colors = [in_col]
	colors.extend([[int(round(x*255)) for x in colorsys.hls_to_rgb(hue, l, saturation)] for l in lightness_list])

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(tuple(s)) for s in colors]

	return colors


def saturate(in_col, number=10):
	'''
	Returns the input color as well as more saturated versions of that color.
	number specifies how many new ones to return.
	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'
	assert type(number) is int, 'Error, the input number must be an integer.'
	assert (2 <= number and number <= 1000), 'Error, the input number must be between 2 and 1000'

	#check whether input is hex, if it is, make it RGB
	hex_color = is_hex(in_col) 
	if hex_color:
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b) 

	#what is the difference of 100% saturation and the current value	
	diff = 1.0-saturation 
	
	#devide the difference on a step size
	step = diff/float(number)

	#use that step size to generate the 10 increasing saturation values	
	saturation_list = [saturation + step*s for s in range(1, number+1)]

	#add the input color to a list, then build the 10 new HSL colors, convert to RGB and save in the same list
	colors = [in_col]
	colors.extend([[int(round(x*255)) for x in colorsys.hls_to_rgb(hue, lightness, s)] for s in saturation_list])

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(tuple(s)) for s in colors]

	return colors


def desaturate(in_col, number=10):
	'''
	Returns the input color as well as less saturated versions of that color.
	number specifies how many new ones to return.
	'''
	assert (is_rgb(in_col) or is_hex(in_col)), 'Error, the input must be a hex color string or an RGB tuple.'
	assert type(number) is int, 'Error, the input number must be an integer.'
	assert (2 <= number and number <= 1000), 'Error, the input number must be between 2 and 1000'

	#check whether input is hex, if it is, make it RGB
	hex_color = is_hex(in_col) 
	if hex_color:
		in_col = hex_to_rgb(in_col)

	#assign to  variables
	r, g, b = in_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b) 
	
	#devide the difference on a step size
	step = saturation/float(number)

	#use that step size to generate the 10 increasing saturation values	
	saturation_list = [saturation - step*s for s in range(1, number+1)]

	#add the input color to a list, then build the 10 new HSL colors, convert to RGB and save in the same list
	colors = [in_col]
	colors.extend([[int(round(x*255)) for x in colorsys.hls_to_rgb(hue, lightness, s)] for s in saturation_list])

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(tuple(s)) for s in colors]

	return colors

def scale(col1, col2, number=101, mode='rgb', white_mid=False):
	'''
	Function makes a color scale from 0 to 100 using the supplied colors.
	The variable white_mid is boolean and determines whether the colors 
	should transition over white in the middle or just smoothly run into each other.
	The function returns a dictionary of integer keys and hex color values corresponding to the scores 0 to 100.
	'''
	assert is_hex(col1) or is_rgb(col1), 'Error, the first color is not valid.'
	assert is_hex(col2) or is_rgb(col2), 'Error, the second color is not valid.'
	assert type(white_mid) is bool, 'Error, white_mid must be a boolean.'
	
	if is_hex(col1):
		col1 = hex_to_rgb(col1)
	if is_hex(col2):
		col2 = hex_to_rgb(col2)
	
	color_dict={}
	if white_mid is False:
		#determine how many points R, G and B should change with each score
		R_diff = (col2[0]-col1[0])/100.0
		G_diff = (col2[1]-col1[1])/100.0
		B_diff = (col2[2]-col1[2])/100.0

		#set starting values
		R, G, B = col1 
		for i in range(101):
			color_dict[i] = rgb_to_hex((R+int(R_diff*i), G+int(G_diff*i), B+int(B_diff*i)))
		
	elif white_mid is True:
		first_half = scale((col1), (255,255,255))
		for key in range(0, 100, 2):
			color_dict[key/2] = first_half[key]
		
		second_half = scale((255,255,255), col2)
		for key in range(0, 102, 2):
			color_dict[50+key/2] = second_half[key]

	return color_dict
	

def rainbow(start_col, end_col=False, number=10, clockwise=True):
	'''
	Returns the entire color wheel starting with the input color.
	number specifies how many new ones to return.
	'''
	assert (is_rgb(start_col) or is_hex(start_col)), 'Error, the input must be a hex color string or an RGB tuple.'
	assert type(number) is int, 'Error, the input number must be an integer.'
	assert (2 <= number and number <= 1000), 'Error, the input number must be between 2 and 1000'

	#check whether input is hex, if it is, make it RGB
	hex_color = is_hex(start_col) 
	if hex_color:
		start_col = hex_to_rgb(start_col)

	#assign to  variables
	r, g, b = start_col

	# Convert to [0, 1]
	r, g, b = [x/255. for x in [r, g, b]] 

	# RGB -> HLS
	hue, lightness, saturation = colorsys.rgb_to_hls(r, g, b) 
	
	# Rotation by defined number of degrees
	angle = (360/float(number))/360.0
	
	if clockwise is False:
            h_list = [(hue+ang) % 1 for ang in [angle*s for s in range(number)]]
            
	elif clockwise is True:
		h_list = [(hue+ang) % 1 for ang in [-angle*s for s in range(number)]]

	else:
		raise ValueError

	colors = [[int(round(x*255)) for x in colorsys.hls_to_rgb(h, lightness, saturation)] for h in h_list] # H'LS -> new RGB
	colors = [tuple(s) for s in colors]

	#if the input was hex, convert it back
	if hex_color:
		colors = [rgb_to_hex(s) for s in colors]

	return colors


def visualize(color_list=['#acc123','#ffffff','#000000', '#1ccf9c']):
	'''
	Visualizes a list of colors.
	Useful to see what one gets out of the different functions.
	'''

	#asserts.... here....


	from tkinter import Tk, Canvas, Frame, BOTH

	#check whether input is hex, if it is, make it RGB
	rgb_color = is_rgb(color_list[0]) 
	if rgb_color:
		color_list = [rgb_to_hex(s) for s in color_list]
	 

	class Example(Frame):
	  
		def __init__(self, parent, cl):
			Frame.__init__(self, parent)   

			self.parent = parent   
			self.color_list = cl     
			self.initUI()
		    
		def initUI(self):

			self.parent.title("Colors")        
			self.pack(fill=BOTH, expand=1)

			canvas = Canvas(self)

			#modify rectangle size based on how many colors there are
			rect_size = 700/float(len(color_list))

			for i in range(len(self.color_list)):
				canvas.create_rectangle(10+rect_size*i, 10, 10+rect_size*(i+1), 110, outline=self.color_list[i], fill=self.color_list[i])
			canvas.pack(fill=BOTH, expand=1)


	def main():

		root = Tk()
		ex = Example(root, color_list)
		root.geometry("720x120+250+300")
		root.mainloop()  

	main() 


    
def calculate_linear_bezier(points, t):
    '''
    Points is a list of two points, P0 and P1, in that order
    '''
    #assign values to variables
    P0, P1 = points
    
    #calculate value of bezier curve at the given t
    Bt = P0 + t*(P1 - P0)
    
    return Bt


def calculate_quadratic_bezier(points, t):
    '''
    Points is a list of three points, P0, P1 and P2, in that order
    '''
    #assign values to variables
    P0, P1, P2 = points
    
    #calculate value of bezier curve at the given t
    Bt = (1-t)*( (1-t)*P0 + t*P1 ) + t*( (1-t)*P1 + t*P2 )
    
    return Bt
    
            
def calculate_cubic_bezier(points, t):
    '''
    Points is a list of four points, P0, P1, P2 and P3, in that order
    ''' 
    #assign values to variables   
    P0, P1, P2, P3 = points
    
    #calculate value of bezier curve at the given t
    Bt = (1-t)**3 * P0 + 3*(1-t)**2 * t * P1 + 3*(1-t) * t**2 * P2 + t**3 * P3
    
    return Bt

        
def devide_and_conquer(min_t, max_t, data, target, func, tolerance=0.0001):
    '''
    min_t is the minimum bound of the variable which are being optimized
    max_t is the maximum bound of the variable which are being optimized
    data is a list of values which are needed to evaluate the variable estimate
    func is a function which is used to evaluate the variable estimate
    target is the target value for which we wish to find a corresponding variable value
    tolerance is how close the answer must be
    '''
   
    
    # determine the halfpoint of t    
    t_half = min_t + (max_t - min_t)/2.0
    
    # calculate value
    est = func(data, t_half)

    # if the guess is close enough, return the estimate
    if abs(est - target) <= tolerance:
        return t_half
    
    # if target is smaller than the 
    elif target < est:
        return devide_and_conquer(min_t, t_half, data, target, func, tolerance)

    # if target is bigger
    elif target > est:    
        return devide_and_conquer(t_half, max_t, data, target, func, tolerance)
    
   
def sequential(colors, step_num):
    '''
    Create a sequential color scale going from a starting color to white or light yellow
    color is the starting color in hex
    end is either "white" or "yellow"

    The function will use bezier smoothing to avoid harsh color transitions.
    Furthermore, it will even out the lightness profile so that it is linear.
	This ensures good color scales.
    '''
    assert 2 <= len(colors) <= 4, 'Error, supply between two and four colors for a sequential scale.' 
    #assert that the colors are valid
    
    #they must also be continually lighter or continually darker
    

    if len(colors) == 2: # linear bezier interpolation
        color1, color2 = colors
        col1_hsl = hex_to_hsl(color1)
        col2_hsl = hex_to_hsl(color2)
        
        assert col1_hsl[2] < col2_hsl[2] or col1_hsl[2] > col2_hsl[2], 'Error, the colors mut get continually lighter or continually darker.'
        
        #figure out how much lightness should change if evenly stepped
        stepsize = (col2_hsl[2]-col1_hsl[2])/(float(step_num)-1.0)
        steps = [col1_hsl[2] + stepsize * s for s in range(step_num)]
        #print('steps', steps)
        
        #find out which bezier t-values corresponds to these lightness steps
        if col1_hsl[2] <= col2_hsl[2]: #darkest color is first
            min_hsl = float(col1_hsl[2])
            max_hsl = float(col2_hsl[2])
            t_values = [devide_and_conquer(0.0, 1.0, data=[min_hsl, max_hsl], target=s, func=calculate_linear_bezier) for s in steps]
            
        elif col1_hsl[2] > col2_hsl[2]: #lightest color is first
            min_hsl = float(col2_hsl[2])
            max_hsl = float(col1_hsl[2])            
            t_values = [devide_and_conquer(0.0, 1.0, data=[min_hsl, max_hsl], target=s, func=calculate_linear_bezier) for s in steps]
            t_values = t_values[::-1]
        

        #now get the colors for these steps        
        h_vals = [calculate_linear_bezier([col1_hsl[0], col2_hsl[0]], t) for t in t_values]
        s_vals = [calculate_linear_bezier([col1_hsl[1], col2_hsl[1]], t) for t in t_values]
        l_vals = [calculate_linear_bezier([col1_hsl[2], col2_hsl[2]], t) for t in t_values]
        
        #combine h, s and l components
        hsl_cols = list(zip(h_vals, s_vals, l_vals))
        
        return [hsl_to_hex(s) for s in hsl_cols]

                
    elif len(colors) == 3: # quadratic bezier interpolation
        color1, color2, color3 = colors
        col1_hsl = hex_to_hsl(color1)
        col2_hsl = hex_to_hsl(color2)
        col3_hsl = hex_to_hsl(color3)

        assert col1_hsl[2] < col2_hsl[2] < col3_hsl[2] or col1_hsl[2] > col2_hsl[2] > col3_hsl[2], 'Error, all colors must get continually lighter or continually darker. You supplied a mix of those. Revise input colors.'
        
        
        #figure out how much lightness should change if evenly stepped
        stepsize = (col3_hsl[2]-col1_hsl[2])/(float(step_num)-1.0)
        steps = [col1_hsl[2] + stepsize * s for s in range(step_num)]
        #print(steps)
        
        #find out which bezier t-values corresponds to these lightness steps
        if col1_hsl[2] <= col2_hsl[2] <= col3_hsl[2]: #darkest color is first
            min_hsl = float(col1_hsl[2])
            med_hsl = float(col2_hsl[2])
            max_hsl = float(col3_hsl[2])
            t_values = [devide_and_conquer(0.0, 1.0, data=[min_hsl, med_hsl, max_hsl], target=s, func=calculate_quadratic_bezier) for s in steps]

        elif col1_hsl[2] >= col2_hsl[2] >= col3_hsl[2]: #lightest color is first
            min_hsl = float(col3_hsl[2])
            med_hsl = float(col2_hsl[2])
            max_hsl = float(col1_hsl[2])
            t_values = [devide_and_conquer(0.0, 1.0, data=[min_hsl, med_hsl, max_hsl], target=s, func=calculate_quadratic_bezier) for s in steps]
            t_values = t_values[::-1]
            
        #now get the colors for these steps        
        h_vals = [calculate_quadratic_bezier([col1_hsl[0], col2_hsl[0], col3_hsl[0]], t) for t in t_values]
        s_vals = [calculate_quadratic_bezier([col1_hsl[1], col2_hsl[1], col3_hsl[1]], t) for t in t_values]
        l_vals = [calculate_quadratic_bezier([col1_hsl[2], col2_hsl[2], col3_hsl[2]], t) for t in t_values]
        
        #combine h, s and l components
        hsl_cols = list(zip(h_vals, s_vals, l_vals))
        
        return [hsl_to_hex(s) for s in hsl_cols]

                
    elif len(colors) == 4: # cubic bezier interpolation
        color1, color2, color3, color4 = colors
        col1_hsl = hex_to_hsl(color1)
        col2_hsl = hex_to_hsl(color2)
        col3_hsl = hex_to_hsl(color3)
        col4_hsl = hex_to_hsl(color4)

        assert col1_hsl[2] < col2_hsl[2] < col3_hsl[2] < col4_hsl[2] or col1_hsl[2] > col2_hsl[2] > col3_hsl[2] > col4_hsl[2], 'Error, all colors must get continually lighter or continually darker. You supplied a mix of those. Revise input colors.'
        
        
        #figure out how much lightness should change if evenly stepped
        stepsize = (col4_hsl[2]-col1_hsl[2])/(float(step_num)-1.0)
        steps = [col1_hsl[2] + stepsize * s for s in range(step_num)]
        #print(steps)
        
        #find out which bezier t-values corresponds to these lightness steps
        if col1_hsl[2] <= col2_hsl[2] <= col3_hsl[2]: #darkest color is first
            min_hsl = float(col1_hsl[2])
            med1_hsl = float(col2_hsl[2])
            med2_hsl = float(col3_hsl[2])
            max_hsl = float(col4_hsl[2])
            t_values = [devide_and_conquer(0.0, 1.0, data=[min_hsl, med1_hsl, med2_hsl, max_hsl], target=s, func=calculate_cubic_bezier) for s in steps]

        elif col1_hsl[2] >= col2_hsl[2] >= col3_hsl[2]: #lightest color is first
            min_hsl = float(col4_hsl[2])
            med1_hsl = float(col3_hsl[2])
            med2_hsl = float(col2_hsl[2])
            max_hsl = float(col1_hsl[2])
            t_values = [devide_and_conquer(0.0, 1.0, data=[min_hsl, med1_hsl, med2_hsl, max_hsl], target=s, func=calculate_cubic_bezier) for s in steps]
            t_values = t_values[::-1]
            
        #now get the colors for these steps        
        h_vals = [calculate_cubic_bezier([col1_hsl[0], col2_hsl[0], col3_hsl[0], col4_hsl[0]], t) for t in t_values]
        s_vals = [calculate_cubic_bezier([col1_hsl[1], col2_hsl[1], col3_hsl[1], col4_hsl[1]], t) for t in t_values]
        l_vals = [calculate_cubic_bezier([col1_hsl[2], col2_hsl[2], col3_hsl[2], col4_hsl[2]], t) for t in t_values]
        
        #combine h, s and l components
        hsl_cols = list(zip(h_vals, s_vals, l_vals))
        
        return [hsl_to_hex(s) for s in hsl_cols]



def diverging(colors, number=10):
    '''
    Generates a color scale that can be used for visualizing data.
    colors should be a list of colors which a are used for creating the scale
    number defines how many colors should get returned
    '''
    #there should be 3 or 5 colors where the center one is the middle color of the scale
    assert len(colors) == 3 or len(colors) == 5, 'Error, please supply three or five colors where the centre one is your midpoint color.'
    
    #make sure the colors are in the right format
    
            
    #if 3 colors, do linear interpolation and lightness correction. Operate on each half by itself and then add together.
    
    #if 5 colors, do quadratic bezier interpolation and lightness correction. Operate on each half by itself and then add together.

    
    #calculate a linear ligntess profile
    
    #move from one color to the other and for each output color make sure the lightness is correct    
        
 

def qualitative(number, scale=1):
    '''
    Return a list of qualitative colors for plotting categorical data.
    number defines how many (12 is max)
    scale defines which one of three pre-defined scales should be used
    '''
    assert 1 <= number <= 12, 'Error, the number of colors must be between 1 and 12'
    assert 1 <= scale <= 2, 'Error, scale must be between 1 and 2'
    
    sc1 = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928']
    sc2 = ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd', '#ccebc5', '#ffed6f']

    if scale == 1:
        return sc1[:number]
        
    elif scale == 2:
        return sc2[:number]
        

#def binary(scale=1):
#	'''
#	Return 
#	'''
#	
#	if scale == 1:
#		return 
	
	
    

def NextRGB(color = (0,0,0)):
	'''
	Function for generating unique RGB colors. 
	The input is a tuple of an RGB color, for example (124,1,34), and the method returns the "next" color.
	When R reaches 255 one is added to G and R is reset.
	When R and G both reach 255 one is added to B and R and G are reset.
	This should generate over 1.6 million colors (255*255*255)
	'''
	assert is_rgb(color), 'Error, the input must be a tuple of three integers between 0 and 255'
	R, G, B = color

	if R == 255 and G == 255 and B == 255:
		raise ValueError('R, G and B all have the value 255, no further colors are available.')
	elif  R == 255 and G == 255:
		R = 0
		G = 0
		B += 1
	elif R == 255:
		R = 0
		G += 1
	else:
		R += 1
	return (R, G, B)
	
	
	
#good scales

#purple to teal
#col1 = '#800080'
#col2 = '#008080'

#orange to blue
#col1 = '#ffc500'
#col2 = '#056efa'

#blue to red
#col1 = '#817cbb'
#col2 = '#c12133'

#another blue to red
#col1 = '#30acdf'
#col2 = '#ef292b'

#orange to green
#col1 = '#ff6600'
#col2 = '#2c9082'

#orange to dark blue
#col1 = '#ff6600'
#col2 = '#18567d'

#grey to orange
#col1 = '#666666'
#col2 = '#ff6600'

#dark yellow to blue
#col1 = '#cba916'
#col2 = '#8eb6d5'

	

	 	
	
