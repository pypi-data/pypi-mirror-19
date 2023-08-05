=================================================
Music22: Modal Music Analysis
=================================================

Overview
========

Music22 is a Python2 package for musicological analysis, especially modal music and melodies. The analysis is done from audio files.

For now, it's main features are :

* Fondamental frequencies extraction (using *PredominentMelody()* from **Essentia**);
* Getting the main frequencies as peaks of the probability density function from frequencies;
* Comparing PDFs using a correlation coefficient;
* Getting a similarity matrix between melodies.

Installation
============

To use Music22, you need to manually install `Essentia`_. `In futur versions, it will be also possible to use` `TimeSide`_.

Then, install Music22 with the following :

.. code:: python
	
	pip install music22

Or, if you have a GitLab account, using ``git``:

.. code:: python

	git clone https://gitlab.com/AnasGhrab/music22
	python setup.py install


.. _Essentia: http://essentia.upf.edu/
.. _TimeSide: https://github.com/Parisson/TimeSide

Basic Usage
===========

To use Music22 :

.. code:: python

	from music22 import modalis,scale
	path = "path/to/a/folder/with/audios/wav/files/"
	Kchants = modalis.melodies(path,transpose='Yes',freqref=300)
	
Then you can

.. code:: python

	Kchants.pdf_show()
	Kchants.matrix()
	Kchants.melodies[0].scale
		
For more details, please read to the tutorial (in french) :

http://nbviewer.ipython.org/github/AnasGhrab/music22/blob/master/docs/source/examples/barraq.ipynb

Contact
=======

Homepage: http://anas.ghrab.tn

Email:

 * Anas Ghrab <anas.ghrab@gmail.com>

License
=======

GNU General Public License

https://www.gnu.org/licenses/gpl-3.0.en.html

https://gitlab.com/AnasGhrab/music22/blob/master/LICENSE

Copyright (c) 2015-2017 Anas Ghrab
