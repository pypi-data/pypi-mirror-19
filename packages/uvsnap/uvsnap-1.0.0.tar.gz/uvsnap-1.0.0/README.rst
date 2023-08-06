uvsnap - UniFi Video Command Line Client
****************************************

Usage
=====

List All Cameras::

    $ uvsnap -V -n https://172.17.0.1:7443 -a ABC1234 list
    577d92a5e4b05e057437584c  ||  online  || Reception
    57bddeb5e4b05f0574f678d0  ||  online  || Design
    5746397d5g030d9ca9caf631  ||  online  || MPOE / Telephone Room
    574775aee4b05e0574341e88  ||  online  || Rear Office Windows
    577e9a5fe4b05a0574376016  || OFFLINE  || Front Door - Stairwell

Get a Snapshot of a specific Camera::

    $ uvsnap -V -n https://172.17.0.1:7443 -a ABC1234 577d92a5e4b05e057437584c
    Wrote Snapshot: /tmp/577d92a5e4b05e057437584c.jpg

Get a Snapshot of a all Cameras::

    $ uvsnap -V -n https://172.17.0.1:7443 -a ABC1234 all
    Wrote Snapshot: /tmp/577d92a5e4b05e057437584c.jpg
    Wrote Snapshot: /tmp/57bddeb5e4b05f0574f678d0.jpg
    ...

Install
=======

    pip install uvsnap

Source
======
Github: https://github.com/ampledata/uvsnap

Author
======
Greg Albrecht oss@undef.net

http://ampledata.org/

Copyright
=========
Copyright 2017 Greg Albrecht

License
=======
Apache License, Version 2.0. See LICENSE for details.
