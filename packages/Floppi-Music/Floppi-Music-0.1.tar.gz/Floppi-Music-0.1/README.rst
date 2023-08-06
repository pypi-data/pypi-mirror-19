Floppi-Music - Crazily advanced floppy music player for Raspberry Pi
====================================================================

The Floppi-Music project aims at creating a "crazily advanced" floppy
music library for the Raspberry Pi, written in pure Python.

Motivation
----------

Everyone is doing floppy music these days, and it really gets old and
boring. However, Eike badly wanted to try floppy music himself, and of
course I wanted to meet his desire. Our plan was to create the floppy
music code in pure Python, and we wanted to use the Raspberry Pi to have
a lot of high-level interfaces available.

The final goal is to build a "floppy music jukebox" for presentation at
events and conferences.

Implementation / design goals
-----------------------------

Our intention was to break loose from the low-level approach to floppy
music controller programming and use modern paradigms in a modern
language instead.

The floppy music engine is entirely multi-threaded, with a playback
engine scheduling playback of notes for the various floppy drive
threads.

The framework is designed so it can be easily extended or used as a
library. For example, all recognized input formats are parsed by
seperate functions and converted to an internal format suitable for
playback by the engine. It is easy to create such parsers for any other
(sensible) file format.

Wiring scheme
-------------

The wiring scheme for the Raspberry and floppy interfaces can be found
in WIRING.txt.

What works
----------

-  Parsing of MML (Music Macro Language) files, via
   `MMLlib <https://github.com/Natureshadow/mmllib>`__
-  Playback of 4 (or 8) simultaneous tracks
-  floppi-play command to play recognized, single files through the
   engine

What is planned (Roadmap)
-------------------------

-  Parsing of MIDI files
-  A webserver to select tracks and manage a playlist
-  An mpd-compatible network interface
-  Control through an LCD display and buttons on a controller
-  Self-tuning of floppy drives

Credits
-------

Credits go to:

-  Felix "theftf" Falk (felix@b9d.de), for the wiring and hardware
   advice
-  Thorsten "mirabilos" Glaser (tg@mirbsd.de), for his floppy drive
   donation and magically always being right

Awards
------

The Floppi-Music project has won the following (more or less serious
;-)) awards:

-  "Coolest problem of the friggin' month"-award in #python for "Floppy
   disk drives being out of tune"
