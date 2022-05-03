# COBalD/TARDIS Plugins for High Energy Physics

This repository collects official and third-party plugins.

## Do I have to publish plugins here?

You are free to publish and maintain plugins yourself.
All COBalD/TARDIS plugins are just regular Python packages
which set some specific metadata.

Plugins in this repository are reviewed by the COBalD/TARDIS team
and maintained with similar standards as the core frameworks.

## How do I publish a plugin here?

Plugins are modules or sub-packages in the `cobald_hep_plugins` folder.
To add a new plugin, simply open a pull request that adds your plugin.

In addition to the plugin itself, you should provide
- *unittests* in a `tests` subfolder named after your plugin, and
- *documentation*
