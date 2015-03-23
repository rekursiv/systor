# systor
Utility for archiving Linux OS partitions.

Copies entire system from [source] to [destination].  Run with no args to get current drive status.  One arg should be a folder name and the other should be a device path.  Example:  python systor.py ubuntu /dev/sda

Install dependencies:
* aptitude install ipython
* aptitude install squashfs-tools
* aptitude install gdisk
