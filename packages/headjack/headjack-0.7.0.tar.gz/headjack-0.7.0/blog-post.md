headjack
========

[![Documentation Status](https://readthedocs.org/projects/headjack/badge/)](http://headjack.readthedocs.io/en/latest/?badge)

[![Coverage Status](https://cdn.rawgit.com/thespacedoctor/headjack/master/coverage.svg)](https://cdn.rawgit.com/thespacedoctor/headjack/master/htmlcov/index.html)

*A python package and command-line tools to download, organize, share, archive and reference various kinds of media. Books, podcasts, articles, videos …*.

Here’s a summary of what’s included in the python package:

Command-Line Usage
==================

``` sourceCode
Documentation for headjack can be found here: http://headjack.readthedocs.org/en/stable

Usage:
    headjack read sendToKindle [-s <pathToSettingsFile>]
    headjack read convert kindleAnnotations [-s <pathToSettingsFile>]
    headjack web2epub [-s <pathToSettingsFile>]
    headjack media (stage|archive) [-s <pathToSettingsFile>]
    headjack import marvin <pathToMarvinBackup> [-s <pathToSettingsFile>]
    headjack dt <pathToImportFolder> <pathToDevonthinkDB> [-s <pathToSettingsFile>]

    import                import into the headjack database
    marvin                convert and import the database exported from the Marvin iOS app
    web2epub              convert web-articles queued in the headjack database into epub books
    dt                    import a media package into devonthink

    pathToImportFolder    path to the root directory containing the package to import into a devonthink database
    pathToDevonthinkDB    path to the devonthink database to import the contain into

    -h, --help            show this help message
    -s, --settings        the settings file
```

Installation
============

The easiest way to install headjack is to use `pip`:

``` sourceCode
pip install headjack
```

Or you can clone the [github repo](https://github.com/thespacedoctor/headjack) and install from a local version of the code:

``` sourceCode
git clone git@github.com:thespacedoctor/headjack.git
cd headjack
python setup.py install
```

To upgrade to the latest version of headjack use the command:

``` sourceCode
pip install headjack --upgrade
```

Documentation
=============

Documentation for headjack is hosted by [Read the Docs](http://headjack.readthedocs.org/en/stable/) (last [stable version](http://headjack.readthedocs.org/en/stable/) and [latest version](http://headjack.readthedocs.org/en/latest/)).

Command-Line Tutorial
=====================

To convert a directory of kindle annotation notebook exports:

``` sourceCode
headjack read convert kindleAnnotations
```

Importing Media into Devonthink
-------------------------------

The headjack dt command can be used to import media content into a devonthink database. The content is organised by media-kind and it’s possible to populate all of the media’s associated metadata fields (tags, ratings etc) at the point of import.

The media content to be imported into devonthink must be organised in the import folder in a specific manner. Take the ‘Volkswagen - Wikipedia’ article for example ([grab the test data here](https://github.com/thespacedoctor/headjack/blob/master/headjack/archiver/tests/input/st-devonthink.zip?raw=true)):

<img src="https://i.imgur.com/x7VCSFv.png" alt="image" width="800" />

The content is added to a folder whose name indicates the kind of media-content contained (e.g. ‘web-articles’, ‘podcasts’ etc). The content itself is a folder named with the media-title (e.g. a web-article called ‘Volkswagen - Wikipedia’). The folder contains files related to the content (e.g. the web-article in webarchive, epub and PDF format and a markdown file of notes). Finally there is a yaml file containing a rating, tags etc.

``` sourceCode
title: Volkswagen - Wikipedia
rating: 3
tags:
  - car
  - volkswagen
  - germany
url: https://en.wikipedia.org/wiki/Volkswagen
kind: web-article
```

Note without this yaml file the content will be passed over and not imported into devonthink.

To import this media into my *home reference* devonthink database I run the command:

``` sourceCode
headjack dt "/Users/Me/process/st-devonthink" "/Users/Me/devonthink/home reference.dtBase2
```

This imports the media into a ‘web-articles’ group in the devonthink database given:

<img src="https://i.imgur.com/FlWsqwQ.png" alt="image" width="800" />

The metadata fields are populated including tags, rating (as a devonthink label) and the URL field if given in the yaml metadata. Note for tagging to work you will have to install [jdberry’s ‘tag’](https://github.com/jdberry/tag) (a command line tool to manipulate tags on Mac OS X files, and to query for files with those tags.)

To setup regular automated imports just add the command into your crontab (or use another service like Hazel or Keyboard Maestro).

Importing the Marvin iOS Ebook Reader’s Database into Headjack’s MySQL Database
-------------------------------------------------------------------------------

Once you have read a few ebooks in the Marvin iOS app, marked them up with highlights, notes and tags, rated them and marked them as read, it is now time to export the contents of the app to somewhere on your Dropbox path.

In the Marvin app go to ‘*Settings &gt; General Settings*’ and scroll to the bottom of the menu. Here you should see ‘*Backup and restore*’, select this and then ‘*Backup now*’.

<img src="https://i.imgur.com/3Ck9dL5.png" alt="backup and restore in Marvin" width="400" />

Once the backup has completed choose to ‘*Send it*’ and select ‘*import with Dropbox*’ as the share action. I usually just back the zip file up to the root of my Dropbox account.

<img src="https://i.imgur.com/FkxTScp.png" alt="image" width="400" />

Once the backup has synced to the machine you have headjack installed on, run the command:

``` sourceCode
headjack import marvin ~/Dropbox/marvin.zip 
```

This will unzip the backup and sync Marvin’s sqlite database into your headjack database so now you have a local copy of the annotations, tags and notes from all you books.
