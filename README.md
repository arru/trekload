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

Trekload is licensed under the Revised BSD License:

Copyright (c) 2013, Arvid Rudling
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The name(s) of its contributor(s) may not be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
