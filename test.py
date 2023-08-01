import datetime

timer_on = datetime.time(10,0)
timer_off = datetime.time(22, 0)

def timer_check(on, off):
    now = datetime.datetime.now().time()
    print(on, off, now)
    if on <= now < off:
        print("Light is on") #Turn the light on
    else:
        print('light is off') #Turn the light off

timer_check(timer_on, timer_off)