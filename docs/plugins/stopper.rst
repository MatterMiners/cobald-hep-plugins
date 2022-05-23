#################
Start/Stop Plugin
#################

.. py:module:: cobald_hep_plugins.stopper
    :synopsis: Stops the booting of new drones if there are no pending jobs

This plugin sets the demand to 0 and keeps it at 0 as long as there are no pending jobs on the monitored partition. If there are pending jobs on the partition, the demand is not modified by the plugin.

The plugin is configured via the COBalD configuration file. The available parameters are ``script`` and ``interval``.

``script`` is a mandatory parameter and defines the location of the script that checks for pending jobs on the monitored partition. The script should contain the command of the respective batch system that returns the number of pending jobs. An example for the Slurm batch system is: ``squeue -p name_of_partition -t pending -h | wc -l``.

``interval`` defines the time in seconds between executions of the script. The default value is ``300``.

An example configuration of the plugin in a COBalD configuration file using the YAML interface is:

.. code:: yaml
	  
    - !Stopper
    script: '/path/to/script.sh'
    interval: 60
