from asyncio import wait_for
import pyRTOS


motorMutex = pyRTOS.Mutex()

def andar(self):
    
    
    yield

    while True:
        print("andando loop")

        yield [pyRTOS.timeout(1.5)]

def ler_sensor1(self):
    
    yield

    while True:
        motorMutex.lock(self)

        print("lendo_sensor1 loop")
        
        motorMutex.unlock()
        yield [pyRTOS.timeout(1)]

def ler_sensor2(self):
    i = 0

    yield

    while True:
        
        if(i == 0):
            pass
        else:    
            
            print(i, "de2")
            print("lendo_sensor2 loop")
            
            print("isso foi executado")
        i += 1
        yield [pyRTOS.timeout(1)]

ler_sensor = pyRTOS.Task(ler_sensor1, 1, mailbox=True)

pyRTOS.add_task(pyRTOS.Task(andar, 3, name="andar", mailbox=True))
pyRTOS.add_task(ler_sensor)
pyRTOS.add_task(pyRTOS.Task(ler_sensor2, 1, name="ler2", mailbox=True))

ler_sensor.deliver(motorMutex)


pyRTOS.start()



