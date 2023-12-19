import pyvisa
import time

#Init resource manager
rm=pyvisa.ResourceManager()

#INIT instrument
dm3068=rm.open_resource('USB0::0x1AB1::0x0C94::DM3O192900505::INSTR')

dm3068.write(':FUNCtion:VOLTage:AC 1')

print(dm3068.query(':MEASure:VOLTage:AC?'))
print(dm3068.query(':MEASure:FREQuency?'))

# It takes time
