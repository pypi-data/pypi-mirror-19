========================================
Bittray - a systray app for bitcoin info
========================================

.. figure:: bittray.png
   :alt: Bittray running inside tint2

   Bittray running inside tint2.

Bittray is an application to display the current bitcoin price in your
systray. If you enable electrum support it provides a handy launch menu
for your wallets.

Requirements
============

It's probably the best to install wx and pillow through your operating
system, on Debian use::

    apt-get install python-wxgtk3.0 python-pil

Python3 is not supported at this moment, wx is not packaged for it in Debian,
and some of the code would need porting as well. Nothing big, but I can't do it
yet.

Installation
============

To install bittray and some dependencies run::

    python setup.py install

After this you can use the `bittray` command, assuming the script is
somewhere on your `PATH`.

Configuration
=============

A default configuration file will be create in `~/.config/bittray/bittray.cfg`,
please see there for available settings.

You should not delete settings from the configuration file, the application
doesn't have internal default values. On upgrades new settings should be added
automatically, if not please report a bug.

If you update the configuration while `bittray` is running you can make it
reload the configuration with `pkill -SIGUSR1 bittray`.

Planned features
================

- Notifications for price changes, will require a price history
- Possibly support more wallets
- Dynamic price color, probably hooked into the notification logic
