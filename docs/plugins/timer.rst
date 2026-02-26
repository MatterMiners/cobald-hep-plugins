#############
Timer Plugin
#############

.. py:module:: cobald_hep_plugins.timer
    :synopsis: Time-of-day demand controller

The :class:`~cobald_hep_plugins.timer.Timer` plugin enforces a recurring,
time-of-day schedule for the demand of a target pool.

At its core the Timer plugin stores an ordered mapping of timestamps to demand
values. Each day it steps through the mapping in sorted order: if the timestamp
is in the past it immediately updates the target pool's demand, otherwise it sleeps
until the timestamp is reached and then updates the demand accordingly. After
reaching the last timestamp in the mapping it starts over at the beginning for the
next day. As a reference time the plugin uses the system's local time on which the
COBalD instance is running.

Configuration
=============

The class accepts two arguments:

``target``
    The pool whose demand should follow the schedule. This is the same target
    you would normally use in a COBalD pipeline.

``schedule``
    A mapping where the key is ``HH:MM`` and the
    value is a floating-point demand. The schedule must contain at least one
    entry, and demand values must be non-negative.


Example configuration
=====================

An example snippet for the YAML interface in a COBalD configuration file:

.. code:: yaml

    - !Timer
      target: SomePool
      schedule:
        '06:00': 20
        '09:00': 80
        '17:30': 10

With this configuration the target pool ``SomePool`` will have its demand set
to ``20`` from 6 AM, to ``80`` from 9 AM, and to ``10`` from 5:30 PM until 
6 AM on the following day and so on.
