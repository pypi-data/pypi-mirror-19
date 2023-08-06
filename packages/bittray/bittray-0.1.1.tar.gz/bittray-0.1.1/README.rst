========================================
Bittray - a systray app for bitcoin info
========================================

.. figure:: bittray.png
   :alt: Bittray running inside tint2

   Bittray running inside tint2.

Bittray is an application to display the current price in your systray.

Requirements
============

It's probably the best to install wx and pillow through your operating
system, on Debian use::

    apt-get install python-wxgtk3.0 python-pil

If you use python3::

    apt-get install python3-pil

Wx is not packaged yet for py3, please refer to it's documentation for
install instructions. Please report any bugs as I haven't tested on py3
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

Planned features
================

- Notifications for price changes, will require a price history
- Possibly support more wallets
- Dynamic price color, probably hooked into the notification logic
