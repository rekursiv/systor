from IPython.utils.process import system, getoutput
import os.path

device = None
efipart = '1'
syspart = '2'

def assertReady():
  if device is None:
    raise RuntimeError('Destination drive not set.')
  o = getoutput("df")
  if o.find(device)!=-1:
    raise RuntimeError('Destination drive already mounted!')
    
def mount(readOnly):
  if readOnly: arg='-r '
  else: arg=''
  system('mount {} /mnt/efi'.format(arg+device+efipart))
  system('mount {} /mnt/sys'.format(arg+device+syspart))
  
def umount():
  system('umount '+device+efipart)
  system('umount '+device+syspart)

def initDrive():
  print 'Clearing the partition table on device {}...'.format(device)
  system("sgdisk -Z -o -g {}".format(device))

def printPartTable():
  system("sgdisk -p {}".format(device))

def setupEfi():
  print 'Setting up UEFI boot partition as {}...'.format(device+efipart)
  system("sgdisk -n 1::+512M {}".format(device))
  system("sgdisk -t 1:ef00 {}".format(device))
  print '  Formatting...'
  system("mkfs.fat -F32 {}".format(device+efipart))

def setupSys():
  print 'Setting up system partition as {}...'.format(device+syspart)
  system("sgdisk -n 2:: {}".format(device))
  print '  Formatting...'
  system("mkfs.ext4 -F {}".format(device+syspart))
 
def isEfiMounted():
  system('mountpoint /mnt/efi')

def updateUuids():
  efiUuid = getUuid(efipart)
  sysUuid = getUuid(syspart)
  print('new efi UUID={}').format(efiUuid)
  print('new system UUID={}').format(sysUuid)
  oldUuid = updateFstabUuids(efiUuid, sysUuid)
  print('old system UUID={}').format(oldUuid)
  updateGrubCfgUuids(oldUuid, sysUuid, '/mnt/sys/boot/grub/grub.cfg')
  updateGrubCfgUuids(oldUuid, sysUuid, '/mnt/efi/EFI/ubuntu/grub.cfg')  
  
def updateFstabUuids(efiUuid, sysUuid):
  print('Inserting new UUIDs into fstab...')
  with open('/mnt/sys/etc/fstab', 'r+') as fsFile:
    fsText = fsFile.read()
    idBegin = fsText.find("\nUUID=")+6
    fsFile.seek(idBegin)
    fsFile.write(sysUuid)
    oldUuid = fsText[idBegin:(idBegin+len(sysUuid))]
    idBegin = fsText.find("\nUUID=", idBegin)+6
    fsFile.seek(idBegin)
    fsFile.write(efiUuid)
  return oldUuid

def updateGrubCfgUuids(oldUuid, newUuid, filepath):
  print('Inserting new UUIDs into {}...').format(filepath)
  with open(filepath, 'r+') as gcFile:
    gcText = gcFile.read()
    idBegin = 0
    idEnd = 0
    count = 0
    while True:
      idBegin = gcText.find(oldUuid, idEnd)
      idEnd = idBegin+len(oldUuid)
      if idBegin == -1: break
      if count > 100: break
      count=count+1
      gcFile.seek(idBegin)
      gcFile.write(newUuid)
  print('Replaced {} UUIDs'.format(count))

def getUuid(part):
  return getoutput("blkid {} -o value -s UUID".format(device+part)).strip()

