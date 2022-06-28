# COBalD/TARDIS Plugins for High Energy Physics

[![Documentation Status](https://readthedocs.org/projects/cobald-hep-plugins/badge)](https://cobald-hep-plugins.readthedocs.io)

This package collects official and third-party plugins
for the [COBalD](https://github.com/MatterMiners/cobald) /
[TARDIS](https://github.com/MatterMiners/tardis) resource manager.

## How do I use these plugins?

The plugins work like the basic COBalD/TARDIS components:
install the package and the plugins are automatically available
in configuration and code.

The package is directly available via `pip` and must be installed
to the same `python3` environment as COBalD/TARDIS.
```bash
$ python3 -m pip install cobald-hep-plugins
```

Consult [the documentation](https://cobald-hep-plugins.readthedocs.io)
on how to use individual plugins.

## Do I have to publish plugins here?

You are free to publish and maintain plugins yourself.
All COBalD/TARDIS plugins are just regular Python packages
which set some specific metadata.

Plugins in this repository are reviewed by the COBalD/TARDIS team
and maintained with similar standards as the core frameworks.

## How do I publish a plugin here?

Before proposing a plugin, please reach out to us for advise.
This could be for example via email, chats, or just opening a ticket.

To add a new plugin,
[head to our GitHub repository](https://github.com/MatterMiners/cobald-hep-plugins)
and open a pull request that adds your plugin.
Plugins are modules or sub-packages in the `cobald_hep_plugins` folder
that can also come with additional meta-data.
See the `cobald_hep_plugins/example` as a template.

In addition to the plugin itself, you should provide
- *unittests* in a `tests` subfolder, and
- *documentation* in a `docs/plugins` file or subfolder.
