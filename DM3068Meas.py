import pyvisa
import time
#123
import string

#CHANGE FREQ OF INSTRUMENT

#N-number of measures
N=500

#Init resource manager
rm=pyvisa.ResourceManager()

file = open('measure.txt', 'w')

#INIT instrument
dm3068=rm.open_resource('USB0::0x1AB1::0x0C94::DM3O192900505::INSTR')

#Setting mode to measure AC voltage with range (2V)
dm3068.write(':FUNCtion:VOLTage:AC 1')

#creating array of voltages
vtg=[0]*N
S2=''

#start timer
tic = time.perf_counter()

#taking voltage from instrument
for i in range (N):
    vtg[i]=dm3068.query(':MEASure:VOLTage:AC?')


for i in range(N):
    S1 = vtg[i]
    S1 = S1[:len(S1) - 1]
    # print(S1)
    S2 += S1 + ', '

#Formatting file for octave
S2=S2[:len(S2)-2]
S2=('['+S2+']')
file.write(S2)
file.close()

toc = time.perf_counter()
#print(vtg)
print(f" {toc - tic:0.4f} seconds elapsed for " + str(N) + ' measurements')