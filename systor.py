#  version 2.1

import argparse
import util
import guide

parser = argparse.ArgumentParser(description='Copies entire system from [source] to [destination].  Run with no args to get current drive status.  One arg should be a folder name and the other should be a device path.  Example:  python systor.py ubuntu /dev/sda')
parser.add_argument("source", nargs="?")
parser.add_argument("destination", nargs="?")
parser.parse_args()
args = parser.parse_args()

if args.source is None and args.destination is None:
  util.info()
elif args.source is not None and args.source.startswith('/dev/'):
  guide.setDevice(args.source)
  guide.setFolderName(args.destination)
  guide.deviceToFiles()
elif args.destination is not None and args.destination.startswith('/dev/'):
  guide.setFolderName(args.source)
  guide.setDevice(args.destination)
  guide.filesToDevice()
else:
  parser.print_help()

