# -*- coding: UTF-8 -*-

#TODO:
# 1. kontroll av monterad Fenix
# 2. skriv banor som banor eller medianpunkt
#3. strippa bort all HTML från description och lägg i desc eller cmt

import unicodedata
import argparse
import os.path

from random import random

from lxml import etree
import lxml.html.clean

symbol_default = 'White Dot'

mollet = '/Users/arru/Library/Application Support/Google Earth/mollet/'

# http://home.online.no/~sigurdhu/MapSource-text.htm
# http://home.online.no/~sigurdhu/12MAP_symbols.htm


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

ggpx_industrial = 'Ghost Town'

#Test icon IDs
test_items = ()

#Arvids
kml_to_ggpx_overrides = {
	'http://maps.google.com/mapfiles/kml/shapes/police.png':'Private Field',
	'http://www.klavrestromsvhem.g.se/bilder/stfmini.gif':'Lodging',
	'http://industrisemester.nu/sites/default/files/images/erskine-ballong-128.png':'Parachute Area',
	'/Users/arru/Library/Application Support/Google Earth/neon.png':'Bank',
	'/Users/arru/Pictures/Symboler/Vägmärken/Sevärdhet.png':'Scenic Area',
	'/Users/arru/Library/Application Support/Google Earth/Turistväg.png':'Scenic Area',
	mollet + 'woodshed.png':ggpx_industrial,
	mollet + 'factory.png':ggpx_industrial,
	mollet + 'cablecar.png':'Heliport',
	mollet + 'oilpumpjack.png':'Gas Station',
	mollet + 'fillingstation.png':'Gas Station',
	mollet + 'car.png':'Car',
	mollet + 'highway.png':'Car',
	mollet + 'steamtrain.png':ggpx_industrial,
	mollet + 'windturbine.png':ggpx_industrial,
	mollet + 'dam.png':'Levee',
	mollet + 'watertower.png':ggpx_industrial,
	mollet + 'bridge_modern.png':'Picnic Area',
	mollet + 'bunker.png':'Military',
	mollet + 'harbor.png':'Anchor',
	mollet + 'lighthouse.png':'Anchor',
	mollet + 'shipwreck.png':'Shipwreck',
	mollet + 'mine.png':'Golf Course',
	mollet + 'targ.png':'Amusement Park',
	mollet + 'apartment-3.png':'Building',
	mollet + 'publicart.png':'Scenic Area',
	mollet + 'phantom.png':'Residence',
	mollet + 'observatory.png':'Building',
	}

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

gpx_version = "1.0"

kml_ns = {'kml':'http://www.opengis.net/kml/2.2'}

class Waypoint(object):
	def __init__(self, lat_init, lon_init, name='Untitled', alt_init=None, icon=None, description=None):
		self.lat = lat_init
		self.lon = lon_init
		self.alt = alt_init
		self.name = name.encode('utf8')
		self.icons = {}
		self.description = description

		if icon:
			self._setIcon (icon[0], icon[1])
		#print self.icons

	def _setIcon(self, format, id):
		self.icons[format] = id

		if(format == 'kml'):
			if(id in kml_to_ggpx_symbols):
				self.icons['ggpx'] = kml_to_ggpx_symbols[self.icons['kml']]
			else:
				self.icons['ggpx'] = None

	def __str__(self):
		return "%s: %f,%f (%f m) - %s" % (
			self.name,
			self.lat,
           	self.lon,
			self.alt,
			self.icons)

class KMLDocument(object):
	def __init__(self, path):
		self.path = path
		self.data = None
		self.stylemap = {}
		self.waypoints = []

	def read(self):
		"""Read KML data from file at self.path"""
		kml = etree.parse(self.path)
		style_definitions = {}

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
			#print "%s -> %s" % (style_mapping.attrib['id'], style_definitions[style_url])

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
				icon = self.stylemap[style[1:]]

			if (len(points) == 1):
				point = points[0]
				coords = point.findtext('kml:coordinates', namespaces=kml_ns).split(',')

				lat = float(coords[1])
				lon = float(coords[0])
				alt = None
				if (len(coords) >= 3):
					alt = float(coords[2])

				read_waypoint = Waypoint(lat, lon, name, alt, ('kml', icon), description=desc)
				self.waypoints.append(read_waypoint)
			else:
				#if there is no point, either the KML is malformed or there might be a LineString
				print "Skipping %s" % placemark


class GarminGPXDocument(object):
	def __init__(self, name='output'):
		udata = name.decode("utf-8")
		self.name = udata.encode('ascii', 'ignore')
		self.waypoints = []

		self.data = etree.Element('gpx',
								version=gpx_version,
								creator='fenixload',
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

	def close(self):
		# Save to XML file
		file = open('%s.gpx' % self.name, 'wb')

		for wp in self.waypoints:
			if(wp.lat is not None and wp.lon is not None):
				wpt = etree.SubElement(self.data, 'wpt', lat=str(wp.lat), lon=str(wp.lon))
				name = etree.SubElement(wpt, 'name')

				#name.text = etree.CDATA(wp.name.decode('utf-8'))
				name.text = wp.name.decode('utf-8')

				if (wp.alt and wp.alt != 0.0):
					ele = etree.SubElement(wpt, 'ele')
					ele.text = str(wp.alt)

				sym = etree.SubElement(wpt, 'sym')
				if('ggpx' in wp.icons):
					sym.text = wp.icons['ggpx']
				else:
					sym.text = symbol_default

				if wp.description:
					desc = etree.SubElement(wpt, 'desc')
					#desc.text = etree.CDATA(wp.description)

					if len(wp.description) > 50:
						desc.text = wp.description[0:49] + u"…"
					else:
						desc.text = wp.description

		self.xml.write(file, xml_declaration=True, encoding='utf-8')

#Main program flow

parser = argparse.ArgumentParser(description='Process KML data and write to Garmin Fenix as .gpx')
parser.add_argument('--test', action="store_true",
                   help='Output test gpx with symbols 0-test max')
parser.add_argument('--dest', metavar='d', default=None,
                   help="Specify a destination for output file. Default: Fenix' GPX folder")
parser.add_argument('input', default=None,
                   help='Input KML file (ignored in test mode)')

args = parser.parse_args()

dest = args.dest
if args.dest is None:
	dest = "/Volumes/GARMIN/Garmin/GPX/%s" % os.path.basename(args.input)

output_doc = GarminGPXDocument(dest)

if (args.test):
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
		test_wp = Waypoint(point[0], point[1], name=d, icon=('ggpx', str(d)))

		output_doc.addPoint(test_wp)
else:
	#regular run (not test mode)
	assert(args.input is not None)

	input = KMLDocument(args.input)
	input.read()
	output_doc.addPoints(input.waypoints)

output_doc.close()
