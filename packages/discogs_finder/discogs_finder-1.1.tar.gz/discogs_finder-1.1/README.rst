discogs\_finder
===============

**FIND** **E**\ very **R**\ elease in your collection

.. image:: https://travis-ci.org/tim6her/discogs_finder.svg?branch=master
   :alt: build
.. image:: https://coveralls.io/repos/github/tim6her/discogs_finder/badge.svg?branch=master
   :target: https://coveralls.io/github/tim6her/discogs_finder?branch=master
.. image:: https://readthedocs.org/projects/discogs-finder/badge/?version=latest
   :target: http://discogs-finder.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status



This is a small commandline tool that fetches your discogs collection
and performs a deep key value search.

::

    $ discogs-finder --u tim6her name=Chick
    Searching for {'name': 'Chick'}
    1)  Herbie Hancock & Chick Corea: An Evening With Herbie Hancock & Chick Corea In Concert 1978 (530041)
        basic_information.artists.1.name = Chick Corea
    2)  Chick Corea & Friedrich Gulda: The Meeting (2210545)
        basic_information.artists.0.name = Chick Corea
    3)  Wolfgang Amadeus Mozart, Chick Corea, Friedrich Gulda, Concertgebouworkest, Nikolaus Harnoncourt: Double Concerto / Compositions (4764105)
        basic_information.artists.1.name = Chick Corea

It can also return the whole json entry for the matched releases using
the ``--v`` option.

::

    $ discogs-finder --u tim6her --v name=Pob
    Searching for {'name': 'Pob'}
    {
      "instance_id": 207732124, 
      "date_added": "2017-01-14T05:32:34-08:00", 
      "basic_information": {
        "formats": [
          {
            "qty": "1", 
            "descriptions": [
              "LP", 
              "Album", ...

For help on usage run ``discogs-finder --help`` or consult the `Docs. <http://discogs-finder.readthedocs.io/en/latest/>`_
