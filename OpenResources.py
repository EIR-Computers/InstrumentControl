import pyvisa
#Init resource manager
rm=pyvisa.ResourceManager()
#print devices
print(rm.list_resources())