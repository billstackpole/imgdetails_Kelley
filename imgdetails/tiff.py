#!/usr/bin/env python
# Requires the Python Imaging Library (PIL)
# Available at http://www.pythonware.com/products/pil/

""" tiff.py - TIFF handler class for imgdetails.py
	Author - Benjamin Kelley
	Date - May 2, 2013
	Release Version - 1.0
"""
import sys

from PIL import Image, TiffImagePlugin
from PIL.ExifTags import TAGS

class tiff():
	############################
	# __init__()
	# Class initialization method
	# Parameters: 
	#		Self
	#		Image im - Main image object
	# Returns: N/a
	############################
	def __init__(self, im):
		self.image = im
		self.decoded = self.get_tiff_tags()
		if self.decoded is None:
			print "Image does not contain any extractable exif data!"
			sys.exit(1)
	
	#############################
	# get_tiff_tags()
	# Extracts tiff tags from the image file
	# Parameters: 
	#		Self
	# Returns:
	#		decoded - A dictionary of decoded exif data
	##############################
	def get_tiff_tags(self):
		tifftags = self.image.tag.tags
		decoded = {}
		for a, b in tifftags.items():
			val = TAGS.get(a,b)
			decoded[val] = b
		return decoded
	
	###############################
	# decoded_data()
	# Dumps all of the decoded dictionary data to the console
	# Parameters:
	#		Self
	# Returns: N/a
	###############################
	def decoded_dump(self):
		print "\nDecoded Metadata:"
		for title, value in self.decoded.items():
			print "%s: %s" % (title, value)