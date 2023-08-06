============
jira-history
============

Makes working with Jira issue changelogs a breeze!

Quickstart
----------

::

    >>> issue = jira.issue('JIRA-2204')
    >>> add_history(issue)
    >>> issue.history
    <Changelog 3 entries>
    >>> issue.history.at(day)
    {'resolution': ...}

Installation
------------

Simply run ::

    pip install jira-history

Contributing
------------

Please do! I would love for this to be developed further by anyone who is interested. Wherever possible, please
provide unit tests for your work (yes, this is very much a 'do as I say, not as I do' kind of moment).
Don't forget to add your name to AUTHORS.

License
-------

Copyright (c) 2016 Sebastian Rahlf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.