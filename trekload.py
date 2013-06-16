#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#	Trekload is licensed under the Revised BSD License:
#	
#	Copyright (c) 2013, Arvid Rudling
#	All rights reserved.
#	
#	Redistribution and use in source and binary forms, with or without
#	modification, are permitted provided that the following conditions are met:
#	    * Redistributions of source code must retain the above copyright
#	      notice, this list of conditions and the following disclaimer.
#	    * Redistributions in binary form must reproduce the above copyright
#	      notice, this list of conditions and the following disclaimer in the
#	      documentation and/or other materials provided with the distribution.
#	    * The name(s) of its contributor(s) may not be used to endorse or promote products
#	      derived from this software without specific prior written permission.
#	
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#	DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
#	DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#	SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#TODO (bugs):
# handle style mappings embedded in waypoints

#Test icon IDs
from trekload_conf import kml_to_ggpx_overrides, test_items

import unicodedata
import argparse
import os.path
import logging

import re
from random import random

from lxml import etree
import lxml.html.clean

#Garmin symbol code references are available here:
# http://home.online.no/~sigurdhu/MapSource-text.htm
# http://home.online.no/~sigurdhu/12MAP_symbols.htm


### Fenix specific constants

waypoint_mem_reserve = 25
fenix_max_waypoints = 1000

fenix_sym_missing = (
	'Ball Park',
	'Bar',
	'Beach',
	'Bell',
	'Bike Trail',
	'Blue Pin',
	'Bridge',
	'Cemetery',
	'Circle with X',
	'City (Capitol)',
	'City (small)',
	'Civil',
	'Civil',
	'Contact, Biker',
	'Contact, Ranger',
	'Controlled Area',
	'Convenience Store',
	'Crossing',
	'Dam',
	'Danger Area',
	'Diver Down Flag 1',
	'Diver Down Flag 2',
	'Drinking Water',
	'Exit',
	'Fast Food',
	'Forest',
	'Green Diamond',
	'Green Square',
	'Horn',
	'Hunting Area',
	'Ice Skating Area',
	'Large City', 	'Light',
	'Medium City',
	'Movie Theater',
	'Museum',
	'Navaid, Amber',
	'Navaid, White',
	'Oil Field',
	'Parking Area',
	'Parking',
	'Pharmacy',
	'Pizza',
	'Police Station',
	'Post Office',
	'Radio Beacon',
	'Red Square',
	'Restricted Area',
	'RV Park',
	'Scales',
	'School',
	'Shopping Center',
	'Shopping',
	'Short Tower',
	'Small City',
	'Summit',
	'Tall Tower',
	'Theater',
	'Toll Booth',
	'Truck Stop',
	'Tunnel',
	'Water Hydrant',
	'White Buoy',
	'Zoo',
)

fenix_sym_set = (
	'Airport',
	'Amusement Park',
	'Anchor',
	'Bank',
	'Boat Ramp',
	'Building',
	'Campground',
	'Car',
	'Dot, White',
	'Fishing Area',
	'Flag, Blue',
	'Gas Station',
	'Geocache Found',
	'Geocache',
	'Ghost Town',
	'Golf Course',
	'Heliport',
	'Information',
	'Levee',
	'Lodging',
	'Medical Facility',
	'Military'
	'Parachute Area',
	'Park',
	'Picnic Area',
	'Private Field', #rendered like 'Restricted Area'
	'Residence',
	'Restaurant',
	'Restroom',
	'Scenic Area',
	'Skiing Area',
	'Skull and Crossbones',
	'Soft Field',
	'Swimming Area',
	'Telephone',
	'Trail Head',
	'Waypoint',
)

### Generic symbol constants

symbol_default = 'White Dot'

#Standard KML icon equivalents
kml_to_ggpx_symbols = {
					#'http://maps.google.com/mapfiles/kml/shapes/grocery.png':'Shopping Center',
					#'http://mw1.google.com/mw-earth-vectordb/smartmaps_icons/museum-15.png':'Museum',					'http://maps.google.com/mapfiles/kml/pal4/icon61.png':'Flag, Blue',
					'http://maps.google.com/mapfiles/kml/shapes/cabs.png':'Car',
					'http://maps.google.com/mapfiles/kml/shapes/camera.png':'Scenic Area',
					'http://maps.google.com/mapfiles/kml/shapes/campground.png':'Campground',
					'http://maps.google.com/mapfiles/kml/shapes/caution.png':'Skull and Crossbones',
					'http://maps.google.com/mapfiles/kml/shapes/dining.png':'Restaurant',
					'http://maps.google.com/mapfiles/kml/shapes/dollar.png':'Bank',
					'http://maps.google.com/mapfiles/kml/shapes/fishing.png':'Fishing Area',
					'http://maps.google.com/mapfiles/kml/shapes/flag.png':'Flag, Blue',
					'http://maps.google.com/mapfiles/kml/shapes/gas_stations.png':'Gas Station',
					'http://maps.google.com/mapfiles/kml/shapes/golf.png':'Golf Course',
					'http://maps.google.com/mapfiles/kml/shapes/hiker.png':'Trail Head',
					'http://maps.google.com/mapfiles/kml/shapes/homegardenbusiness.png':'Residence',
					'http://maps.google.com/mapfiles/kml/shapes/hospitals.png':'Medical Facility',
					'http://maps.google.com/mapfiles/kml/shapes/info_circle.png':'Information',
					'http://maps.google.com/mapfiles/kml/shapes/lodging.png':'Lodging',
					'http://maps.google.com/mapfiles/kml/shapes/marina.png':'Anchor',
					'http://maps.google.com/mapfiles/kml/shapes/open-diamond.png':'Dot, White',
					'http://maps.google.com/mapfiles/kml/shapes/parking_lot.png':'Car',
					'http://maps.google.com/mapfiles/kml/shapes/parks.png':'Park',
					'http://maps.google.com/mapfiles/kml/shapes/phone.png':'Telephone',
					'http://maps.google.com/mapfiles/kml/shapes/picnic.png':'Picnic Area',
					'http://maps.google.com/mapfiles/kml/shapes/poi.png':'Waypoint',
					'http://maps.google.com/mapfiles/kml/shapes/ski.png':'Skiing Area',
					'http://maps.google.com/mapfiles/kml/shapes/swimming.png':'Swimming Area',
					'http://maps.google.com/mapfiles/kml/shapes/toilets.png':'Restroom',
					'http://maps.google.com/mapfiles/kml/shapes/airports.png':'Airport',
					'':symbol_default
				}

kml_to_ggpx_symbols.update (kml_to_ggpx_overrides)

### KML & GPX format constants

gpx_version = "1.0"

kml_ns = {'kml':'http://www.opengis.net/kml/2.2'}

# String that gets appended to the wp name when tracks are collapsed to their
# median points ('--tracks point' option)
median_point_suffix = '(mitten)'

class Track(object):
	'''Represents a GIS track (multi-segment path between two locations)'''
	def __init__(self, coords, name='Untitled', icon=None, description=None):
		self.coords = []
		self.coords.extend(coords)
		self.name = name.encode('utf8')
		self.icons = {}
		self.description = description

		if icon:
			self._setIcon (icon[0], icon[1])

	def _setIcon(self, format, id):
		self.icons[format] = id

		if(format == 'kml'):
			if(id in kml_to_ggpx_symbols):
				self.icons['ggpx'] = kml_to_ggpx_symbols[self.icons['kml']]
			else:
				self.icons['ggpx'] = None

	def _makePoint(self, parent, coord, type_code):
		wpt = etree.SubElement(parent, type_code, lat=str(coord[0]), lon=str(coord[1]))
		if (len(coord) == 3 and coord[2] != 0.0):
			ele = etree.SubElement(wpt, 'ele')
			ele.text = str(coord[2])

		return wpt

	def _makeMetadata(self, parent, option=''):
		name = etree.SubElement(parent, 'name')

		#name.text = etree.CDATA(self.name.decode('utf-8'))
		if option == 'point':
			name.text = "%s %s" % (self.name.decode('utf-8'), median_point_suffix)
		else:
			name.text = self.name.decode('utf-8')

		sym = etree.SubElement(parent, 'sym')
		if('ggpx' in self.icons):
			sym.text = self.icons['ggpx']
		else:
			sym.text = symbol_default

		if self.description:
			desc = etree.SubElement(parent, 'desc')
			#desc.text = etree.CDATA(self.description)

			if len(self.description) > 50:
				desc.text = self.description[0:49] + u"…"
			else:
				desc.text = self.description

	def outputGPX(self, parent, option):
		elem = None
		if option == 'full':
			elem = etree.SubElement(parent, 'trk')
			seg = etree.SubElement(elem, 'trkseg')

			assert (len(self.coords) > 0)
			for c in self.coords:
				self._makePoint(seg, c, type_code='trkpt')
		elif option == 'point':
			pt = self.coords[len(self.coords) / 2]
			elem = self._makePoint(parent, pt, type_code='wpt')

		if elem is None:
			assert (option == 'skip')
		else:
			self._makeMetadata(elem, option)

	def __str__(self):
		return "%s: %s, - %s" % (
			self.name,
			self.coords,
			self.icons)

class Waypoint(Track):
	'''Representation of GIS waypoint'''
	def __init__(self, coord3D, name='Untitled', icon=None, description=None):
		Track.__init__(self, [coord3D], name, icon, description)

	def outputGPX(self, parent, option=''):
		if len(self.coords) == 1:
			wpt = self._makePoint(parent, self.coords[0], type_code='wpt')
			self._makeMetadata(wpt)
		else:
			assert (len(self.coords) == 0)


class KMLDocument(object):
	'''KML document loader/parser class'''
	def __init__(self, path):
		self.path = path
		self.data = None
		self.stylemap = {}
		self.waypoints = []

	def read(self):
		"""Read KML data from file at self.path"""
		kml = etree.parse(self.path)
		style_definitions = {}

		line_string_pattern = re.compile("\s*(?:([-]?[\d]*[\.]?[\d]+),)(?:([-]?[\d]*[\.]?[\d]+),)?([-]?[\d]*[\.]?[\d]+)\s+")

		#read style definitions
		for style in kml.xpath('//kml:Document/kml:Style', namespaces=kml_ns):
			id = style.attrib['id']
			assert(id)
			icon_list = style.xpath('kml:IconStyle/kml:Icon/kml:href', namespaces=kml_ns)
			if (len(icon_list) > 0):
				icon_href = icon_list[0].text
			else:
				icon_href = ''
			style_definitions[id] = icon_href


		#generate self.stylemap from style_definitions and StyleMap pairs
		for style_mapping in kml.xpath('//kml:Document/kml:StyleMap', namespaces=kml_ns):

			url = None
			for pair in style_mapping.xpath('kml:Pair', namespaces=kml_ns):
				if pair.findtext('kml:key', namespaces=kml_ns) == 'normal':
					style_url = pair.findtext('kml:styleUrl', namespaces=kml_ns)[1:]

			assert(style_url)
			self.stylemap[style_mapping.attrib['id']] = style_definitions[style_url]
			#logging.debug( "%s -> %s" % (style_mapping.attrib['id'], style_definitions[style_urself.		for placemark in kml.xpath('//kml:Placemark', namespaces=kml_ns):)

		for placemark in kml.xpath('//kml:Placemark', namespaces=kml_ns):
			points = placemark.xpath('kml:Point', namespaces=kml_ns)
			name = placemark.findtext('kml:name', namespaces=kml_ns)
			style = placemark.findtext('kml:styleUrl', namespaces=kml_ns)
			desc_str = placemark.findtext('kml:description', namespaces=kml_ns)

			desc = None
			if desc_str:
				desc_html = lxml.html.fromstring(desc_str)
				cleaner = lxml.html.clean.Cleaner(allow_tags=[], remove_unknown_tags=True)
				stripped_html = cleaner.clean_html(desc_html)

				desc = stripped_html.text_content()

			if (style is not None):
				if style[1:] in self.stylemap:
					icon = self.stylemap[style[1:]]
				else:
					icon = None
					logging.warning("Could not find style mapping %s on %s, skipping icon" % (style[1:], name))
			else:
				icon = None
				#TODO: support inline style mappings
				logging.warning("No style URL for %s, skipping icon" % name)

			coords = []
			if (len(points) == 1):
				point = points[0]
				raw_coords = point.findtext('kml:coordinates', namespaces=kml_ns).split(',')

				if (len(raw_coords) >= 3):
					point = (float(raw_coords[1]), float(raw_coords[0]), float(raw_coords[2]))
				else:
					point = (float(raw_coords[1]), float(raw_coords[0]))

				read_waypoint = Waypoint(point, name, ('kml', icon), description=desc)
				self.waypoints.append(read_waypoint)
			else:
				line_coords_chunk = placemark.findtext('kml:LineString/kml:coordinates', namespaces=kml_ns)
				if line_coords_chunk is not None:
					line_tokens = line_string_pattern.findall(line_coords_chunk)
					try:
						for c in line_tokens:
							if len(c) == 2:
								coords.append((float(c[1]), float(c[0]), float(c[2])))
							else:
								coords.append((float(c[1]), float(c[0])))
					except ValueError:
						logging.error("Could not parse %s (%s) to float coordinates" % (c, name))
						raise

					read_track = Track(coords, name, ('kml', icon), description=desc)
					self.waypoints.append(read_track)
				else:
					logging.warning ("Skipping %s b/c unrecognized placemark type" % placemark)

class GarminGPXDocument(object):
	'''GPX file writer'''
	def __init__(self, name='output'):
		udata = name.decode("utf-8")
		self.name = udata.encode('ascii', 'ignore')
		self.path = '%s.gpx' % self.name
		self.waypoints = []

		self.data = etree.Element('gpx',
								version=gpx_version,
								creator='trekload',
								#attrib={'{xsi}schemaLocation':'http://www.topografix.com/GPX/1/0/gpx.xsd'},
								nsmap={
									#'wptx1' : 'http://www.garmin.com/xmlschemas/WaypointExtension/v1',
									#'gpxx':'http://www.garmin.com/xmlschemas/GpxExtensions/v3',
									#'gpxtpx':'http://www.garmin.com/xmlschemas/TrackPointExtension/v1',
									'xsi':'http://www.w3.org/2001/XMLSchema-instance',
									None:'http://www.topografix.com/GPX/1/0'}
								)

		self.xml = etree.ElementTree(self.data)


	def addPoints(self, wpoint_list):
		for wpoint in wpoint_list:
			self.addPoint(wpoint)

	def addPoint(self, wpoint):
		self.waypoints.append(wpoint)

	def close(self, option):
		# Save to XML file
		file = open(self.path, 'wb')

		for wp in self.waypoints:
			wp.outputGPX(self.data, option=option)

		self.xml.write(file, xml_declaration=True, encoding='utf-8')

### Main program flow

parser = argparse.ArgumentParser(description='Process KML data and write to Garmin Fenix as .gpx')
parser.add_argument('--test', action="store_true",
                   help='Output test gpx with symbols 0-test max')
parser.add_argument('--tracks', default='point',
                   help='KML tracks: full, point or skip. Default: point')
parser.add_argument('--dest', metavar='d', default=None,
                   help="Specify a destination for output file. Must be a directory. Default: Fenix' GPX folder")
parser.add_argument('--input', default=os.path.expanduser('~/Desktop/'),
                   help='Input KML file (ignored in test mode)')
parser.add_argument('--log', default='debug',
                   help='Logging level')

args = parser.parse_args()

#Logging
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}
level = LEVELS.get(args.log, logging.NOTSET)
logging.basicConfig(level=logging.DEBUG)

#Destination
if args.dest is None:
	dest_dir = "/Volumes/GARMIN/Garmin/GPX/"
	if not os.path.isdir(dest_dir):
		raise IOError(u"Fenix is not mounted. Check your connections or specify a different destination argument")
else:
	dest_dir = os.path.abspath(args.dest)
assert (os.path.isdir(dest_dir))

waypoint_counter = 0

if (args.test):
	#Test mode
	test_center = (59.6, 16.53)
	test_radius = 0.1

	test_step = test_radius / (len(test_items) + 1)
	r = test_step
	#for d in range(0, args.test):
	for d in test_items:
		direction = [random()*2.0 - 1.0, random()*2.0 - 1.0]
		r = r + test_step
		offset = [v * r for v in direction]
		point = [test_center[i] + offset[i] for i in range(0, 2)]
		test_wp = Waypoint(point, name=d, icon=('ggpx', str(d)))

		output_doc.addPoint(test_wp)
else:
	#regular conversion (non-test) mode

	#input file/dir
	input = os.path.abspath(args.input)
	input_files = []

	if (os.path.isdir(input)):
		for fileName in os.listdir(input):
			splitName = os.path.splitext(fileName)
			if len(splitName) > 1:
				fileType = splitName[1]
				if fileType.lower() == '.kml':
					input_files.append(os.path.join(input, fileName))
	else:
		assert(os.path.exists(input))
		input_files.append(input)

	#Iterate through input files
	for file in input_files:
		dest_filename = os.path.splitext(os.path.basename(file))[0]
		output_doc = GarminGPXDocument(os.path.join(dest_dir, dest_filename))

		input = KMLDocument(file)
		input.read()
		output_doc.addPoints(input.waypoints)

		output_doc.close(option=args.tracks)

		num_waypoints = len(output_doc.waypoints)
		logging.info("Wrote %s\t(%d waypoints)" % (dest_filename, num_waypoints))
		waypoint_counter += num_waypoints

#Report number of waypoints written

#FIXME: actually counts number of waypoints AND tracks
#(each complete track counts as one point)
if waypoint_counter >= fenix_max_waypoints:
	logging.warning("Waypoint memory exhausted (%s) by this loading session" % waypoint_counter)
elif waypoint_counter > fenix_max_waypoints - waypoint_mem_reserve:
	logging.warning("Waypoint memory almost exhausted (%s) by this loading session" % waypoint_counter)
else:
	logging.info("Wrote %d tracks or waypoints" % waypoint_counter)
