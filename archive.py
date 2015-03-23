from IPython.utils.process import system
import os.path

folderName = None

def pack():
  print 'Archiving system into {}...'.format(folderName)
  system('mksquashfs /mnt/efi {}/efi.sfs'.format(folderName))
  system('mksquashfs /mnt/sys {}/sys.sfs'.format(folderName))
  
def unpack():
  print 'Unpacking system from folder {}...'.format(folderName)
  system('unsquashfs -f -d /mnt/efi {}/efi.sfs'.format(folderName))
  system('unsquashfs -f -d /mnt/sys {}/sys.sfs'.format(folderName))
  
def assertNotExists():
  if os.path.exists(folderName+'/efi.sfs'):
    raise RuntimeError('UEFI archive file already exists.')
  if os.path.exists(folderName+'/sys.sfs'):
    raise RuntimeError('System archive file already exists.')
  
def assertReady():
  checkEfi()
  checkSys()

def checkEfi():
  system('mount -r {} /mnt/efi'.format(folderName+'/efi.sfs'))
  if not os.path.exists('/mnt/efi/EFI'):
    raise RuntimeError('Invalid archive file "{}"'.format(folderName+'/efi.sfs'))
  system('umount /mnt/efi')

def checkSys():
  system('mount -r {} /mnt/sys'.format(folderName+'/sys.sfs'))
  if not os.path.exists('/mnt/sys/etc'):
    raise RuntimeError('Invalid archive file "{}"'.format(folderName+'/sys.sfs'))
  system('umount /mnt/sys')

  
def debug():
  print('path={}'.format(fileName))
  

