MMLlib - Modern library for handling Music Macro Language
=========================================================

About
-----

MMLlib is a pure Python implementation of functionality related to the
`Music Macro
Language <https://en.wikipedia.org/wiki/Music_Macro_Language>`__ as
implemented by Microsoft® GW-BASIC® and compatibles, which is its most
common form, also implemented by the PC speaker driver in Linux and
`BSD <http://www.mirbsd.org/man4/spkr>`__, with a number of extensions
and changes:

-  ``|`` denotes a bar line, ignored by the Linux/BSD driver
-  support for multiple (parallel) instrument tracks
-  a per-file header with work metadata (optional)
-  lines starting with a ``#`` are comments
-  the alias ``~`` is not supported

The library currently contains functions to:

-  parse an (extended) MML file into metadata and individual tracks
-  a duration estimate and the number of tracks is added to the metadata
-  return a list of tuples (frequency, duration) to play (in a threaded
   interpreter, such as Floppi-Music)
-  bar lines are indicated separately as integer ``1``
-  return an event-oriented list of measures / bars across all tracks;
   each measure has a duration and a list of time-fixed tone on/off
   events; facilitates playing in non-threaded interpreters and,
   possibly, MIDI export
-  export (extended) MML to MusicXML
-  which can be imported by e.g. `MuseScore <https://musescore.org/>`__
   to…

   -  double-check the MML score for mistakes in a visual representation
   -  play, arrange, etc. the music
   -  beautify the score to print it as sheet music
   -  export into other formats or share on their website

-  check tracks for synchronisation error
-  missing tracks, i.e. with 0 bars
-  missing bars (can only be detected at the end, of course)
-  missing notes within a bar, relative to other tracks

Examples
--------

Some example extended MML files are contained within the examples/
directory, in lieu of better documentation for the extended format, in
addition to the `MML format documentation
<http://www.mirbsd.org/man4/spkr>`__.

Projects using MMLlib
---------------------

::Floppi-Music::
    `Floppi-Music <https://github.com/Natureshadow/Floppi-Music>`__ has
    MML as input format for floppy drive music on Raspberry Pi and uses
    MMLlib for processing. Floppi-Music is also the origin of MMLlib.

Description of the (extended) music macro language
==================================================

Based on http://www.antonis.de/qbebooks/gwbasman/play.html and
https://www.mirbsd.org/man4/spkr .

Symbols of MML
--------------

:A-G[#,+,-][length]:
    A-G are notes. # or + following a note produces a sharp; - produces a
    flat.

:L(n):

    Sets the length of each note. L4 is a quarter note, L1 is a whole note,
    and so on. n may be from 1 to 64. Length may also follow the note to
    change the length for that note only. A16 is equivalent to L16A. Default
    is L4.

:ML:
    Music legato. Each note plays the full period set by L.

:MN:
    Music normal. Each note plays seven-eighths of the time determined by L
    (length).

:MS:
    Music staccato. Each note plays three-quarters of the time determined by
    L.

:N(n):
    Play note n. n may range from 0 to 84. In the 7 possible octaves, there
    are 84 notes. n set to 0 (or omitted) indicates a rest.

:O(n):
    Octave 0 sets the current octave. There are 7 octaves (0 through 6).
    Default is 4. Middle C is at the beginning of octave 2.

:P(n):
    Pause. n may range from 1-64; the current L value is used if omitted.

:T(n):
    Tempo. T sets the number of L4s in a minute. n may range from 32-255.
    Default is 120.

:. (period):
    A period after a note increases the playing time of the note by 3/2
    times the period determined by L (length of note) times T (tempo).
    Multiple periods can appear after a note, and the playing time is scaled
    accordingly. For example, A. will cause the note A to play one and half
    times the playing time determined by L (length of the note) times T (the
    tempo); two periods placed after A (A..) will cause the note to be
    played at 9/4 times its ascribed value; an A with three periods (A...)
    at 27/8, etc. Periods may also appear after a P (pause), and increase
    the pause length as described above.

:>:
    A greater-than symbol raises the current octave by one.

:<:
    A less-than symbol lowers the current octave by one.

:\|:
    Optionally used as a synchronisation mark for multi-track music. This is
    a proprietary extension in the Floppi-Music project.

Comments
--------

Lines starting with # are comments. At the beginning of the file,
comments may be used to encode metadata. This is yet to be specified.
The current implementation parses '^:raw-latex:`\s*`#(
[^:]*):(.*):raw-latex:`\s*`$' into :raw-latex:`\1` = key,
:raw-latex:`\2` = value pairs, strips both key and value, lower-cases
the key and adds it to a dictionary.

The MusicXML export currently specifically recognises these keys:

-  Title, Copyright, Encoder (person), Source
-  Composer, Lyrics, Arranger, Translator *xor* Artist (deprecated, only
   one)

Any other key is treated as miscellaneous field.

Voices
------

The voices of a song are interleaved. They are grouped per notation
system, and the notation systems are seperated by empty lines.

Changelog for MMLlib
====================

0.3
---

-  Enable Python 3 compatibility.
-  Add new mmllint script.
-  Include example MML songs.
-  Add first parts of test suite.
-  Some bugfixes.

0.2
---

-  Add mml2musicxml script.

0.1
---

-  Separate from Floppi-Music.


