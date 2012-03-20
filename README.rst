############################
ssh config command line tool
############################

``favssh`` is a tool to manipulate the ssh configuration file from the command
line.


************
Installation
************


``pip install favssh`` in a virtualenv or ``sudo pip install favssh``.


*****
Usage
*****

List hosts
==========

``favssh [-c/--config-file=~/.ssh/config] list``


Add host
========

``favssh [-c/--config-file=~/.ssh/config] add <name> <hostname> [-p/--port=22] [-u/--user=$USER]``


Update host
===========

``favssh [-c/--config-file=~/.ssh/config] update <name> <key> <value>``


Remove host
===========

``favssh [-c/--config-file=~/.ssh/config] remove <name>``
