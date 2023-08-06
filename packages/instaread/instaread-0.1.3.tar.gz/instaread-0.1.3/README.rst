===============================
instaread
===============================

.. image:: https://badge.fury.io/py/instaread.png
    :target: http://badge.fury.io/py/instaread

.. image:: https://travis-ci.org/anhdat/instaread.png?branch=master
        :target: https://travis-ci.org/anhdat/instaread


Fast and minimal CLI application to read Instapaper from terminal

Usage
--------

Main flow

`instaread`

Read the last unread item. Use with '--archive' as 'instaread --archive' to show your commitment.

In the case you was overconfident, unarchive last archived item with:
    instaread putback

More commands:
.. code-block::
    Usage:
      instaread [--archive][--force]
      instaread putback
      instaread folders
      instaread unreads
      instaread archiveds
      instaread -h | --help
      instaread --version
    
    Options:
      -h --help     Show this screen.
		    Open last unread
      --archive     Open last unread and archive it
      --force       Force refresh token and secret
      --version     Show version.
  

Installation
------------

`pip3 install instaread`


Requirements
------------

- Python >= 3.3

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/anhdat/instaread/blob/master/LICENSE>`_ file for more details.
