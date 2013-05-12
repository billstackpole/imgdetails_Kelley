#!/usr/bin/env python

""" imgdetails.py - Exif data parser for JIF and TIFF image files
	Author - Ben Kelley
	Date - May 2, 2013
	Release Version - 1.0
"""
# Requires the Python Imaging Library (PIL)
# Available at http://www.pythonware.com/products/pil/

import argparse

from PIL import Image, TiffImagePlugin
from imghdr import what
from PIL.ExifTags import TAGS
#from PIL import PngImagePlugin

from jpeg import * # class for handling .jpg images
from tiff import * # class for handling .tif images

################################
# main()
# The main code block for the program
# Parameters: N/a
# Returns: N/a
################################
def main():
	
	if type is 'jpeg':
		image = jpeg(im)
		if args.gps:
			image.get_lat_long()
		if args.basic:
			image.basic_info()
		if args.dump:
			image.decoded_dump()
	elif type is 'tiff':
		image = tiff(im)
		if args.gps:
			print "Not available for TIFF images!"
		if args.basic:
			print "Not yet implemented!"
		if args.dump:
			image.decoded_dump()
			

if __name__ == "__main__":
	# Sets up and handles command-line options	
	parser = argparse.ArgumentParser(description="Image EXIF Analyzer - Analyzes JPG and TIFF images")
	parser.add_argument('imgpath', metavar='IMGPATH', nargs=1,
		help="Path to the image file that will be analyzed")
	parser.add_argument('-d', '--dump', help="Dumps the decoded exif data", action="store_true")
	parser.add_argument('-g', '--gps', help="Attempt to determine the Lat/Long of picture's origin", action="store_true")
	parser.add_argument('-b', '--basic', help="Prints basic image data", action="store_true")
	
	args = parser.parse_args()

	# Attempts to open the image using the Python Imaging Library's image object
	# If it opens successfully, the file type is identified and the main is called
	try:
		im = Image.open(args.imgpath[0])
		type = what(args.imgpath[0])
		main()
	except IOError:
		print "%s cannot be found, or is not an image file!" % args.imgpath[0]

