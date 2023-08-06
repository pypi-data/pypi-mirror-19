tastic
======

*A python package for working with taskpaper documents*.

<img src="http://i.imgur.com/NOAEm0A.png" alt="image" width="400" />

Here's a summary of what's included in the python package:

Command-Line Usage
==================

    Documentation for tastic can be found here: http://tastic-for-taskpaper.readthedocs.io/en/stable/


    Usage:
        tastic init
        tastic sort <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
        tastic archive <pathToFileOrWorkspace> [-s <pathToSettingsFile>]
        tastic sync <pathToWorkspace> <workspaceName> <pathToSyncFolder> [<editorialRootPath>] [-s <pathToSettingsFile>]
        tastic reminders import <listName> <pathToTaskpaperDoc> 

    Options:
        init                     setup the tastic settings file for the first time
        sort                     sort a taskpaper file or directory containing taskpaper files via workflow tags in settings file
        archive                  move done tasks in the 'Archive' projects within taskpaper documents into markdown tasklog files
        reminders                commands to work with macOS reminders
        import                   import tasks into a given taskpaper document


        pathToFileOrWorkspace    give a path to an individual taskpaper file or the root of a workspace containing taskpaper files
        pathToTaskpaperDoc       a path to a taskpaper document
        pathToWorkspace          root path of a workspace containing taskpaper files
        workspaceName            the name you give to the workspace
        pathToSyncFolder         path to the folder you wish to sync the index task files into
        listName                 name of a reminders.app list (macOS only)
        editorialRootPath        the root path of editorial's dropbox sync folder (add to generate an editorial URL for each task)
        -h, --help               show this help message
        -v, --version            show version
        -s, --settings           the settings file

Documentation
=============

Documentation for tastic is hosted by [Read the
Docs](http://tastic-for-taskpaper.readthedocs.io/en/stable/) (last
[stable version](http://tastic-for-taskpaper.readthedocs.io/en/stable/)
and [latest
version](http://tastic-for-taskpaper.readthedocs.io/en/latest/)).

Installation
============

The easiest way to install tastic us to use `pip`:

    pip install tastic

Or you can clone the [github
repo](https://github.com/thespacedoctor/tastic) and install from a local
version of the code:

    git clone git@github.com:thespacedoctor/tastic.git
    cd tastic
    python setup.py install

To upgrade to the latest version of tastic use the command:

    pip install tastic --upgrade

Development
-----------

If you want to tinker with the code, then install in development mode.
This means you can modify the code from your cloned repo:

    git clone git@github.com:thespacedoctor/tastic.git
    cd tastic
    python setup.py develop

[Pull requests](https://github.com/thespacedoctor/tastic/pulls) are
welcomed!

### Sublime Snippets

If you use [Sublime Text](https://www.sublimetext.com/) as your code
editor, and you're planning to develop your own python code with tastic,
you might find [my Sublime
Snippets](https://github.com/thespacedoctor/tastic-Sublime-Snippets)
useful.

Issues
------

Please report any issues
[here](https://github.com/thespacedoctor/tastic/issues).

License
=======

Copyright (c) 2016 David Young

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
