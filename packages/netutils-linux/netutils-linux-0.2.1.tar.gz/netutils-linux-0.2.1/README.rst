netutils-linux
======
It's just a bunch of utils to simplify linux network troubleshooting and performance tuning.

Project state
======
Alpha, raw alpha. Six script were gathered together, shortly documented and packet into python package.

Some were cleaned up, some - not. Most of them was being written in bash, not python, maybe they'll be ported later.

Installation
======
.. code :: shell

  pip install netutils-linux

Utils
======

irqtop
------
- Show you a rate of interrupts
- based on /proc/interrupts file
- Hides interrupts with small rate to show a better picture.

softirq-net-rx-top
------
- Show you a rate of receiving packets
- Based on /proc/softirqs
- Sometimes shows much more CPUs than really exists

missed-pkts-monitor
------
- Detects when were packets missed (maybe it will give some idea of correlation with something)
- Easy to use in tactical, not strategic debug, without deployment of graphite/influxdb
- Based on ip -s -s link output

link-rx-rate
------
- Shows how many packets/bytes network interface receives
- Based on /proc/net/dev

rss-ladder
------
Automatically set smp_affinity_list for IRQ of NIC rx/tx queues for ixgbe/igb/vmxnet3 drivers (they usually work on CPU0 out of box).

Based on lscpu's output.

Later, there will be a support for double/quad ladder in case of multiprocessor systems.


autorps
------
Enables RPS of NIC on all available CPUs. It may be good for small servers with cheap network cards or bunch of VLAN.

Later, there will be a support for enable RPS only for subgroup of CPUs based on L3 caches.
