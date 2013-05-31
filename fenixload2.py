# -*- coding: UTF-8 -*-

#TODO:
# 2. filnamnsargument
# 3. testa nummer för symboler som saknas (tex. 'Mine')
# 3. kontroll av monterad Fenix

import unicodedata

from lxml import etree

symbol_default = 'Flag, Blue'

#http://home.online.no/~sigurdhu/MapSource-text.htm
#http://home.online.no/~sigurdhu/12MAP_symbols.htm
kml_to_ggpx_symbols = {
					#'':'Boat Ramp',
					'/Users/arru/Library/Application Support/Google Earth/mollet/apartment-3.png':'Building',
					#'':'Geocache Found',
					#'':'Geocache',
					#'':'Hunting Area',
					#'':'Parachute Area'

					#'':'Beach',
					#'':'City (Capitol)',
					#'':'Crossing',
					#'':'Fast Food',
					#'':'Crossing',
					'http://www.klavrestromsvhem.g.se/bilder/stfmini.gif':'Lodging',
					'http://maps.google.com/mapfiles/kml/shapes/lodging.png':'Lodging',
					'http://maps.google.com/mapfiles/kml/shapes/caution.png':'Skull and Crossbones',
					'http://maps.google.com/mapfiles/kml/shapes/caution.png':'Danger Area',
					'http://maps.google.com/mapfiles/kml/shapes/bars.png':'Bar',
					'/Users/arru/Library/Application Support/Google Earth/mollet/dam.png':'Dam',
					'/Users/arru/Library/Application Support/Google Earth/mollet/dam.png':'Levee',
					'http://mw1.google.com/mw-earth-vectordb/smartmaps_icons/museum-15.png':'Museum',
					#'/Users/arru/Library/Application Support/Google Earth/mollet/oilpumpjack.png':'Oil Field',
					'http://maps.google.com/mapfiles/kml/shapes/parking_lot.png':'Parking Area',
					#'':'Private Field',
					#'':'Restricted Area',
					#'':'Bell'
					#'':'Summit',
					#'':'Truck Stop',
					#'':'Forest',
					#'':'Cemetery',
					'http://maps.google.com/mapfiles/kml/shapes/ranger_station.png':'School',
					'http://maps.google.com/mapfiles/kml/shapes/grocery.png':'Shopping Center',
					'/Users/arru/Library/Application Support/Google Earth/mollet/powerlinepole.png':'Tall Tower',
					'http://maps.google.com/mapfiles/kml/shapes/subway.png':'Tunnel',
					'http://maps.google.com/mapfiles/kml/shapes/poi.png':'Waypoint',
					'http://mw1.google.com/mw-earth-vectordb/smartmaps_icons/zoo-15.png':'Zoo',
					'/Users/arru/Library/Application Support/Google Earth/mollet/targ.png':'Amusement Park',
					'/Users/arru/Library/Application Support/Google Earth/mollet/bridge_modern.png':'Bridge',
					#'':'Contact, Biker',
					'http://maps.google.com/mapfiles/kml/shapes/police.png':'Contact, Ranger',

					'/Users/arru/Library/Application Support/Google Earth/mollet/bunker.png':'Military',
					'/Users/arru/Library/Application Support/Google Earth/mollet/phantom.png':'Ghost Town',
					'/Users/arru/Library/Application Support/Google Earth/mollet/harbor.png':'Anchor',
					'/Users/arru/Library/Application Support/Google Earth/mollet/shipwreck.png':'Shipwreck',
					'http://maps.google.com/mapfiles/kml/shapes/airports.png':'Airport',
					'http://maps.google.com/mapfiles/kml/shapes/cabs.png':'Car',
					'http://maps.google.com/mapfiles/kml/shapes/camera.png':'Scenic Area',
					'http://maps.google.com/mapfiles/kml/shapes/campground.png':'Campground',
					'http://maps.google.com/mapfiles/kml/shapes/dining.png':'Restaurant',
					'http://maps.google.com/mapfiles/kml/shapes/dollar.png':'Bank',
					'http://maps.google.com/mapfiles/kml/shapes/fishing.png':'Fishing Area',
					'http://maps.google.com/mapfiles/kml/shapes/flag.png':'Flag, Blue',
					'http://maps.google.com/mapfiles/kml/shapes/gas_stations.png':'Gas Station',
					'http://maps.google.com/mapfiles/kml/shapes/golf.png':'Golf Course',
					'http://maps.google.com/mapfiles/kml/shapes/hiker.png':'Trail Head',
					'http://maps.google.com/mapfiles/kml/shapes/homegardenbusiness.png':'Residence',
					'http://maps.google.com/mapfiles/kml/shapes/hospitals.png':'Medical Facility',
					'http://maps.google.com/mapfiles/kml/shapes/info_circle.png':'City (small)',
					'http://maps.google.com/mapfiles/kml/shapes/info_circle.png':'Information',
					'http://maps.google.com/mapfiles/kml/shapes/marina.png':'Anchor',
					'http://maps.google.com/mapfiles/kml/shapes/open-diamond.png':'Dot, White',
					'http://maps.google.com/mapfiles/kml/shapes/parks.png':'Park',
					'http://maps.google.com/mapfiles/kml/shapes/phone.png':'Telephone',
					'http://maps.google.com/mapfiles/kml/shapes/picnic.png':'Picnic Area',
					'http://maps.google.com/mapfiles/kml/shapes/ski.png':'Skiing Area',
					'http://maps.google.com/mapfiles/kml/shapes/swimming.png':'Swimming Area',
					'http://maps.google.com/mapfiles/kml/shapes/toilets.png':'Restroom',
					#'/Users/arru/Library/Application Support/Google Earth/mollet/mine.png':'Mine',
					'':symbol_default
				}

gpx_version = "1.0"

kml_ns = {'kml':'http://www.opengis.net/kml/2.2'}

class Waypoint(object):
	def __init__(self, lat_init, lon_init, name_init='Untitled', alt_init=None, kml_icon=None):
		self.lat = lat_init
		self.lon = lon_init
		self.alt = alt_init
		self.name = name_init
		self.icons = {}

		if kml_icon:
			self._setIcon ('kml', kml_icon)

	def _setIcon(self, format, id):
		self.icons[format] = id

		if(format != 'ggpx' and 'kml' in self.icons):
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
		kml = etree.parse(self.path) #.getroot()
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

				print icon
				read_waypoint = Waypoint(lat, lon, name, alt, icon)
				print "Read waypoint %s" % read_waypoint
				self.waypoints.append(read_waypoint)
			else:
				#if there is no point, either the KML is malformed or there might be a LineString
				print "Skipping %s" % placemark


class GarminGPXDocument(object):
	def __init__(self, name='output'):
		self.name = name
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
		#def close_spider (self, spider):
		# Save to XML file
		file = open('%s.gpx' % self.name, 'wb')

		for wp in self.waypoints:
			if(wp.lat is not None and wp.lon is not None):
				wpt = etree.SubElement(self.data, 'wpt', lat=str(wp.lat), lon=str(wp.lon))
				name = etree.SubElement(wpt, 'name')
				name.text = wp.name
				if (wp.alt is not None):
					ele = etree.SubElement(wpt, 'ele')
					ele.text = str(wp.alt)

				#strippa bort all HTML från description och lägg i desc eller cmt

					sym = etree.SubElement(wpt, 'sym')
					if('ggpx' in wp.icons):
						sym.text = wp.icons['ggpx']
					else:
						sym.text = symbol_default
			print "Writing waypoint %s" % wp.name

		self.xml.write(file, xml_declaration=True, encoding='utf-8')

input = KMLDocument('Marint.kml')
input.read()

output_doc = GarminGPXDocument('mar')
#output_doc = GarminGPXDocument('/Volumes/GARMIN/Garmin/GPX/marint')
output_doc.addPoints(input.waypoints)
output_doc.close()
