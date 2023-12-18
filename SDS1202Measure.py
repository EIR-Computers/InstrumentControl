import pyvisa
import time
import string
import winsound


# Function to select Horisontal scale by frequency
def SelectHorScale(frequency):
    HORmode = 0
    HorModes = ['2.0ns', '5.0ns', '10.0ns', '20.0ns', '50.0ns', '100ns', '200ns', '500ns', '1.0us', '2.0us', '5.0us',
                '10us',
                '20us', '50us', '100us', '200us', '500us', '1.0ms', '2.0ms', '5.0ms', '10ms', '20ms', '50ms', '100ms',
                '200ms',
                '500ms', '1.0s', '2.0s', '5.0s', '10s', '20s', '50s', '100s', '200s', '500s', '1000s']
    cells = 14  # from edge to edge
    periods = 8
    hscale = [2.0E-6, 5.0E-6, 10.0E-6, 20.0E-6, 50.0E-6, 100E-6, 200E-6, 500E-6, 1.0E-3, 2.0E-3, 5.0E-3, 10E-3, 20E-3,
              50E-3,
              100E-3, 200E-3, 500E-3, 1.0, 2.0, 5.0, 10, 20, 50, 100, 200, 500, 1.0E+3, 2.0E+3, 5.0E+3, 10E+3, 20E+3,
              50E+3, 100E+3,
              200E+3, 500E+3, 1000E+3]
    dur = (((1 / frequency) * periods * 1000) / cells)
    for i in range(len(hscale) - 1):
        if dur >= hscale[i] and dur < hscale[i + 1]:
            HORmode = i + 1
    return HorModes[HORmode]


# Function to covert data from query about freq
def InputToFreq(input):
    S1 = input[4:len(input)]
    index = S1.find('k')
    if index > 0:
        S1 = S1[0:index]
        S1 = S1 + 'E+3'
    if index < 0:
        index2 = S1.find('Hz')
        S1 = S1[0:index2]
    if S1.find('?') != -1:
        S1 = '0'
    return float(S1)


# Function to convert Voltage
def InputToVTG(input):
    S1 = input[5:len(input)]
    indexV = S1.find('V')
    indexMV = S1.find('mV')
    if indexV > 0:
        S1 = S1[0:indexV]
        S1 = S1 + 'E+3'
    if indexMV > 0:
        S1 = S1[0:indexMV]
    if S1.find('?') != -1:
        S1 = '0'
    return float(S1)


# defining number of measures

TIME = int(input("ENTER duration of experiment in seconds: "))
NUM = int(input("ENTER number of measurements: "))

stime = (TIME / NUM) / 2
if stime > 0.1:
    print("Delay time is: " + str(TIME / NUM))
else:
    print("Delay OFF")

time.sleep(1)

# Init resource manager
rm = pyvisa.ResourceManager()

# opening file
file = open('measure2.txt', 'w')

# creating obj DSO
dso = rm.open_resource('USB0::0x5345::0x1234::SERIAL::INSTR') # OWON SDS1202
#dso = rm.open_resource('USB0::0xF4EC::0xEE3A::NEU00003130499::INSTR') # AKIP 4115


print("Query ID number:")
# test conn
print(dso.query('*IDN?'))

time.sleep(1)

# initial setup vert scale
dso.write(':CH1:SCALe 20mV')  # Attenuation is 10x
#dso.write(':CH1:SCALe 200mV') #Attenuation is 10x


frequency = float(input("ENTER START FREQ in HZ: "))

# initial measurement
hormode = SelectHorScale(frequency)

dso.write(':HORIzontal:SCALe ' + hormode)

OUTFREQ = 'freq=['
OUTVTG = 'vtg=['

print("Executing cycle, wait")

tic = time.perf_counter()
for count in range(NUM):
    # GENERATE SOUND (INCOMPATABLE)
    # winsound.Beep(freq[count], 1000)

    # taking freq data
    frequencySTR = dso.query(':MEASUrement:CH1:FREQ?')
    frequency = InputToFreq(frequencySTR)

    # if frequency is correctly measured - correct horisontal resolution of DSO
    if frequency != 0:
        hormode = SelectHorScale(frequency)
        dso.write(':HORIzontal:SCALe ' + hormode)

    # taking voltage data
    VTGSTR = dso.query(':MEASUrement:CH1:VAMP?')
    volts = InputToVTG(VTGSTR)

    OUTFREQ += str(frequency) + ', '
    OUTVTG += str(volts) + ', '

    if count == round(NUM / 4):
        print("25% ELAPSED")

    if count == round(NUM / 2):
        print("50% ELAPSED")

    if count == round((NUM / 4) * 3):
        print("75% ELAPSED")

    # delay for instrument
    if stime > 0.1:
        time.sleep(stime)
    else:
        time.sleep(0.1)

# formatting out str
OUTVTG = OUTVTG[:len(OUTVTG) - 2] + '];'
OUTFREQ = OUTFREQ[:len(OUTFREQ) - 2] + '];'

# Write to file
file.write(OUTVTG)
file.write('\n')
file.write(OUTFREQ)
file.close()
print('WRT-OK')

# count time
toc = time.perf_counter()
print(f" {toc - tic:0.4f} seconds elapsed for " + str(NUM) + ' measurements')
