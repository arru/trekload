Trekload
========

This conversion script was designed for exporting Google Earth placemarks to the
Garmin Fenix GPS watch.

Still, it's most likely useful for other Garmin GPS
units, and a great starting point for writing the same kind of optimized
icon-aware export to GPS units of different brands. The <sym> tag is
part of the GPX specification rather than Garmin-specific, the icons themselves
are specific, but this utility makes it super easy to define your own icon table.

Features
--------
* Converts Google Earth KML data to GPX optimized for Garmin standalone GPS units
* One-line operation to load waypoints from Google Earth and write to mounted device
* Translates Google Earth standard icons into Garmin/GPX equivalents
* Simple setup for custom icon tables
* Count number of written waypoints to avoid flooding GPS unit's waypoint memory
* Prune KML tracks into single waypoints, or skip them entirely
* Remove HTML in waypoint descriptions, trim description length and convert filenames to ASCII
* All pruning features and hardware GPS targetting yields significantly smaller GPX files than GPSBabel, for example
* Python 2.7, no external dependencies
* Uses default paths that are specific to MacOS X, but should work on any OS as long as arguments are specified manually

Planned
-------
* Create routes from Google Earth folders
* Option to import entire *My Places* from Google Earth
* Option to leave out altitude data altogether

Compatibility
-------------
Designed for and tested with the Garmin Fenix. Should be usable with the other
Garmin GPS units that are mountable as USB mass storage devices, although only
Fenix' symbols have been programmed.

License
-------

Trekload is licensed under the Revised BSD License, se LICENSE file