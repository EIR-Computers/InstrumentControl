import winsound
periods=100
#123

for i in range(2500):
    freq = i + 37
    t = 1 / freq
    duration = round(t * periods * 1000)
    #print(duration, ' ', freq)
    winsound.Beep(freq, duration)