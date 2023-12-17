import pyvisa
import time
import string
import winsound

HorModes=['2.0ns', '5.0ns', '10.0ns', '20.0ns', '50.0ns', '100ns', '200ns', '500ns', '1.0us', '2.0us', '5.0us', '10us',
          '20us', '50us', '100us', '200us', '500us', '1.0ms', '2.0ms', '5.0ms', '10ms', '20ms', '50ms', '100ms', '200ms',
          '500ms', '1.0s', '2.0s', '5.0s', '10s', '20s', '50s', '100s', '200s', '500s', '1000s']

hscale=[2.0E-6, 5.0E-6, 10.0E-6, 20.0E-6, 50.0E-6, 100E-6, 200E-6, 500E-6, 1.0E-3, 2.0E-3, 5.0E-3, 10E-3, 20E-3, 50E-3,
        100E-3, 200E-3, 500E-3, 1.0, 2.0, 5.0, 10, 20, 50, 100, 200, 500, 1.0E+3, 2.0E+3, 5.0E+3, 10E+3, 20E+3, 50E+3, 100E+3,
        200E+3, 500E+3, 1000E+3]

freq=[100, 200, 300, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 710, 720, 730, 740, 750, 760, 770, 780,
      790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000, 1100, 1200,
      1300, 1400, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200,
      3300, 3400, 3500, 3600, 3700, 3800, 3900, 4000, 4100, 4200, 4300, 4400, 4500, 4600, 4700, 4800, 4900, 5000];

N=10
periods = 5
cells = 14 #from edge to edge
#Init resource manager
rm=pyvisa.ResourceManager()

file = open('measure2.txt', 'w')

dso=rm.open_resource('USB0::0x5345::0x1234::SERIAL::INSTR')

print(dso.query('*IDN?'))

dso.write(':CH1:SCALe 20mV') #Attenuation is 10x
S2=''
HORmode = 19
dso.write(':HORIzontal:SCALe ' + HorModes[HORmode])




tic = time.perf_counter()
for count in range (1000):
    #calculate duration
    dur=((1/freq[count])*5*1000/cells)
    #print(str(dur))

    for i in range(len(hscale)-1):
        if dur >= hscale[i] and dur < hscale[i+1]:
            HORmode=i+1
    dso.write(':HORIzontal:SCALe ' + HorModes[HORmode])

    #GENERATE SOUND
    #winsound.Beep(freq[count], 1000)

    INP=dso.query(':MEASUrement:CH1:VAMP?')
    S1=INP[5:len(INP)]
    indexV=S1.find('V')
    indexMV=S1.find('mV')
    if indexV > 0:
        S1 = S1[0:indexV]
        S1=S1+'E+3'
    if indexMV > 0:
        S1 = S1[0:indexMV]
    #print(S1)
    S2 += S1 + ', '
    #print(dso.query(':MEASUrement:CH1:FREQ?'))
    time.sleep(0.1)
S2=S2[:len(S2)-2]
S2=('['+S2+']')
file.write(S2)
file.close()
toc = time.perf_counter()
print('WRT-OK')
print(f" {toc - tic:0.4f} seconds elapsed for " + str(len(freq)) + ' measurements')
