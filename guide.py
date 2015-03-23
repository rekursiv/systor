import drive, archive, util, uuid


class UserAbort(Exception):
  pass

unattendedMode = False

def init():
  global unattendedMode
  unattendedMode = False

def setDevice(device):
  drive.device = device
  if device[-1].isdigit():
    drive.efipart = 'p1'
    drive.syspart = 'p2'
  else:
    drive.efipart = '1'
    drive.syspart = '2'

def setFolderName(folderName):
  archive.folderName = folderName
  
def ok(prompt):
  global unattendedMode
  while True:
    print(prompt)
    if unattendedMode:
      return True
    ui = raw_input("(D)o this / (S)kip this / (A)bort all | (F)inish all unattended >>   ").lower()
    if ui=='d':
      return True
    elif ui=='s':
      return False
    elif ui=='a':
      raise UserAbort()
    elif ui=='f':
      unattendedMode = True
      return True

def warnUser():
  print('\nThis utility is for setting up a new machine or resetting a broken machine back to its default state.')
  print('If you are using this utility to fix a broken machine, make sure any important data has been recovered BEFORE continuing.')
  print('The following steps WILL DELETE ALL DATA on the following device: {}'.format(drive.device))
  print('If this is NOT what you want to do, enter "A" for "ABORT" at the prompt.')
  while True:
    ui = raw_input("(C)ontinue / (A)bort >>   ").lower()
    if ui=='c':
      return
    elif ui=='a':
      raise UserAbort()
  
def finish():
  while True:
    ui = raw_input("(R)eboot / (P)ower off / (S)hell / (U)nmount >>   ").lower()
    if ui=='r':
      drive.umount()
      util.reboot()
    elif ui=='p':
      drive.umount()
      util.poweroff()
    elif ui=='s':
      return
    elif ui=='u':
      drive.umount()
      return
  
def deviceToFiles():
  init()
  try:
    archive.assertNotExists()
    drive.mount(True)
    if ok('Ready to archive entire system on device {} into folder "{}"'.format(drive.device, archive.folderName)):
      archive.pack()
    print 'All done!'
  except UserAbort:
    print('Process aborted by user.')
  except Exception, err:
    print('Error: {}'.format(err))
  finally:
    finish()

def filesToDevice():
  init()
  try:
    archive.assertReady()
    drive.assertReady()
    warnUser()
    if ok('\nReady to initialize the hard drive.  All data will be erased.  LAST CHANCE to abort.'):
      drive.initDrive()
      drive.setupEfi()
      drive.setupSys()
      drive.mount(False)
    if ok('\nReady to unpack the system onto the new partition.'):
      archive.unpack()
    if ok('\nReady to update UUIDs.'):
      drive.updateUuids()
    print 'All done!'
  except UserAbort:
    print('Process aborted by user.')
  except Exception, err:
    print('Error: {}'.format(err))
  finally:
    finish()

