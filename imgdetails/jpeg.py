#!/usr/bin/env python
# Requires the Python Imaging Library (PIL)
# Available at http://www.pythonware.com/products/pil/

""" jpeg.py - JPEG handler class for imgdetails.py
	Author - Benjamin Kelley
	Date - May 2, 2013
	Release Version - 1.0
"""

import webbrowser
import sys

from PIL import Image
from PIL.ExifTags import TAGS

class jpeg():

	############################
	# __init__()
	# Class initialization method
	# Parameters: 
	#		Self
	#		Image im - Main image object
	# Returns: N/a
	############################
	def __init__(self, im):
		self.image = im						# Local image object
		self.decoded = self.get_exif_data() # Loads a dictionary with decoded EXIF data
		if self.decoded is None:			# Dies if there is no EXIF data to analyze
			print "Image does not contain any extractable exif data!"
			sys.exit(1)
	
	#############################
	# get_exif_data()
	# Extracts exif data from the JPEG image
	# Parameters: 
	#		Self
	# Returns:
	#		decoded - A dictionary of decoded exif data
	##############################
	def get_exif_data(self):
		pic_exif = self.image._getexif()	# Gets raw exif data
		decoded = {}
		if pic_exif is not None:
			for a, b in pic_exif.items():	# Iterates through the dictionary
				val = TAGS.get(a,b)			# Calls the TAGS method to decode exif data
				decoded[val] = b			# Loads the new dictionary to be returned
			return decoded					# Returns the decoded exif data dictionary
		else:
			return None						# Returns None if there's no exif data

	###############################
	# decoded_data()
	# Dumps all of the decoded dictionary data to the console
	# Parameters:
	#		Self
	# Returns: N/a
	###############################
	def decoded_dump(self):
		""" Dumps the metadata in a decoded format, so it is easily human readable
		"""
		print "\nDecoded Metadata:"
		for title, value in self.decoded.items():
			print "%s: %s" % (title, value)

	################################
	# basic_info()
	# Dumps only basic exif data to the screen, like make and model of the camera
	# Parameters:
	#		Self
	# Returns: N/a
	################################
	def basic_info(self):
		# Extracts decoded exif data from the dictionary 
		format = self.image.format
		size = str(self.image.size)
		mode = self.image.mode
		make = self.decoded['Make']
		model = self.decoded['Model']
		date_time = self.decoded['DateTime']
			
		# Prints info to the screen
		print "Image Format: %s" % format
		print "Image Size: %s" % size
		print "Image Mode: %s" % mode
		print "Camera Make: %s" % make
		print "Camera Model: %s" % model
		print "Date and Timestamp: %s" % date_time

	################################
	# get_lat_long()
	# Gets GPS information from the image file and converts it to a useable format
	# Parameters:
	#		Self
	# Returns: N/a
	#################################
	def get_lat_long(self):
		gpsinfo = self.decoded['GPSInfo']
		if gpsinfo:	
			# Source for lat/long calculation from:
			# http://stackoverflow.com/questions/6460381/translate-exif-dms-to-dd-geolocation-with-python
	
			lat = [float(x)/float(y) for x,y in gpsinfo[2]]
			latref = gpsinfo[1]
			long = [float(x)/float(y) for x,y in gpsinfo[4]]
			longref = gpsinfo[3]
	
			lat = lat[0] + lat[1]/60 + lat[2]/3600
			long = long[0] + long[1]/60 + long[2]/3600
			if latref == 'S':
				lat = -lat
			if longref == 'W':
				long = -long
		
			# Calls the map_it method to pin the location on Google maps
			self.map_it(lat, long)
		else:
			print "No location data could be found!"
	
	####################################
	# map_it()
	# Maps the GPS coordinates of the image on Google maps
	# Parameters:
	#		Self
	#		lat - Float of the latitude value
	#		long - Float of the longitude value
	# Returns: N/a
	####################################
	def map_it(self, lat, long):
		# Prints latitude and longitude values
		print "Lat: %s" % lat
		print "Long: %s" % long
		# Creates the URL for the map using the latitude and longitude values
		maps_url = "https://maps.google.com/maps?q=%s,+%s" % (lat, long)
		# Prompts the user to launch a web browser with the map
		openWeb = raw_input("Open GPS location in web broser? (Y/N) ")
		if openWeb.upper() == 'Y':
			# Opens the maps link in a web brower
			webbrowser.open(maps_url, new=2)
