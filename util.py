from IPython.utils.process import system

def info():
	print('\nSystem volume info:')
	system('lshw -class volume,disk -short')
	print('\nMount points:')
	system('mount | grep /dev/[sm]')
	print('\n')

def reboot():
  system('reboot')

def poweroff():
  system('poweroff')
