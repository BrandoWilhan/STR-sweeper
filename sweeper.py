from platform import java_ver
import time
import math
from timeMed import TimeMed
import pyRTOS

REQUEST_DATA = 128
SENT_DATA = 129




try:
    import sim

except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

print ('Program started')





sim.simxFinish(-1) # just in case, close all opened connections
clientID = sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
robotName = "dr12"


f_a_motor = open("medicoes_motor", "w+")
f_para_motor = open("medicoes_para_motor", "w+")
f_gira_direita = open("medicoes_gira_direita", "w+")
f_gira_esquerda = open("medicoes_gira_esquerda", "w+")
f_le_front = open("medicoes_le_front", "w+")
f_le_right = open("medicoes_le_right", "w+")
f_le_left = open("medicoes_le_left", "w+")

if clientID != -1:
    print ('Connected to remote API server')

    #getting scene objects

    [error, leftJointHandle] = sim.simxGetObjectHandle(clientID,"/dr12/leftJoint_", sim.simx_opmode_oneshot_wait)
    [error, rightJointHandle] = sim.simxGetObjectHandle(clientID, "/dr12/rightJoint_", sim.simx_opmode_oneshot_wait)
    [error, frontSensor] = sim.simxGetObjectHandle(clientID, "/dr12/Proximity_sensor[0]", sim.simx_opmode_oneshot_wait)
    [error, leftSensor] = sim.simxGetObjectHandle(clientID, "/dr12/Proximity_sensor[1]", sim.simx_opmode_oneshot_wait)
    [error, rightSensor] = sim.simxGetObjectHandle(clientID, "/dr12/Proximity_sensor[2]", sim.simx_opmode_oneshot_wait)

    #mutex declaration

    motorMutex = pyRTOS.Mutex()

    #tasks definitions

    def ativarMotores(self):
        
        j = 0
        i = 0
        yield 
        
        while True:
            t1 = time.time()    
            #critical session
            motorMutex.lock(self)
            sim.simxSetJointTargetVelocity(clientID, leftJointHandle, 300*math.pi/180, sim.simx_opmode_oneshot)
            sim.simxSetJointTargetVelocity(clientID, rightJointHandle, 300*math.pi/180, sim.simx_opmode_oneshot)
            motorMutex.unlock()

            print("ativou loop")
            i += 1
            if(i > 1):
                self.send(pyRTOS.Message(SENT_DATA, self, "para_motores"))
                i = 0

            t2 = time.time()
            td = (t2 - t1)*10**3            #time in miliseconds
            time_medition = TimeMed(td, self.name, j)
            f_a_motor.write(f"{str(time_medition.time).replace('.', ',')} \n")
            j += 1
            yield [pyRTOS.timeout(1)]
        
    def pararMotores(self):
        
        j = 0
        i = 0
        yield

        while True:
            t1 = time.time()  
            if(i == 0):
                pass
            else:
                print("parou")
                msg = self.recv()
                print(msg[0].source.name,"-------")
                #critial session
                motorMutex.lock(self)
                sim.simxSetJointTargetVelocity(clientID, leftJointHandle, 0, sim.simx_opmode_oneshot)
                sim.simxSetJointTargetVelocity(clientID, rightJointHandle, 0, sim.simx_opmode_oneshot)
                motorMutex.unlock()

            i += 1

            t2 = time.time()
            td = (t2 - t1)*10**3            #time in miliseconds
            time_medition = TimeMed(td, self.name, j)
            f_para_motor.write(f"{str(time_medition.time).replace('.', ',')} \n")
            j += 1
            yield [pyRTOS.wait_for_message(self)]

            yield [pyRTOS.delay(0.5)]

    def girarDireita(self):
        
        j = 0
        i = 0
        yield

        while True:
            t1 = time.time()  
            if(i == 0):
                pass
            else:
                print("girouDireita loop")
                self.recv()
                #critical session
                motorMutex.lock(self)
                sim.simxSetJointTargetVelocity(clientID, leftJointHandle, 90*math.pi/180, sim.simx_opmode_oneshot)
                sim.simxSetJointTargetVelocity(clientID, rightJointHandle, -90*math.pi/180, sim.simx_opmode_oneshot)
                motorMutex.unlock()

            i += 1
            if(i > 10):
                i = 0
                self.send(pyRTOS.Message(SENT_DATA, self, "gira_esquerda"))

            t2 = time.time()
            td = (t2 - t1)*10**3            #time in miliseconds
            time_medition = TimeMed(td, self.name, j)
            f_gira_direita.write(f"{str(time_medition.time).replace('.', ',')} \n")
            j += 1

            yield[pyRTOS.wait_for_message(self)]
        
        

    def girarEsquerda(self):
        
        j = 0
        i = 0
        yield

        while True:
            t1 = time.time()  
            if(i == 0):
                pass
            else:
                print("girouEsquerda loop")
                self.recv()
                #critical session
                motorMutex.lock(self)
                sim.simxSetJointTargetVelocity(clientID, leftJointHandle, -90*math.pi/180, sim.simx_opmode_oneshot)
                sim.simxSetJointTargetVelocity(clientID, rightJointHandle, 90*math.pi/180, sim.simx_opmode_oneshot)
                motorMutex.unlock()
            i += 1

            t2 = time.time()
            td = (t2 - t1)*10**3            #time in miliseconds
            time_medition = TimeMed(td, self.name, j)
            f_gira_esquerda.write(f"{str(time_medition.time).replace('.', ',')} \n")
            j += 1

            yield[pyRTOS.wait_for_message(self)]
            
            
    
    
    def readSensorRight(self):
        
        j = 0
        sim.simxReadProximitySensor(clientID, rightSensor, sim.simx_opmode_streaming)

        yield
        
        while True:
            t1 = time.time()  
            sensorRight = sim.simxReadProximitySensor(clientID, rightSensor, sim.simx_opmode_buffer)
            print(sensorRight)
            
            if(sensorRight[1]):
                print("entrou_sensor_rigght")
                self.send(pyRTOS.Message(SENT_DATA, self, "front"))

            t2 = time.time()
            td = (t2 - t1)*10**3            #time in miliseconds
            time_medition = TimeMed(td, self.name, j)
            f_le_right.write(f"{str(time_medition.time).replace('.', ',')} \n")
            j += 1

            yield [pyRTOS.timeout(0.1)]
    
    def readSensorLeft(self):
        
        j = 0
        sim.simxReadProximitySensor(clientID, leftSensor, sim.simx_opmode_streaming)

        yield
        
        while True:
            t1 = time.time()  
            sensorLeft = sim.simxReadProximitySensor(clientID, leftSensor, sim.simx_opmode_buffer)
           # print(sensorLeft)
            if(sensorLeft[1]):
                print("entrou_sensor_left")
                self.send(pyRTOS.Message(SENT_DATA, self, "front"))

            t2 = time.time()
            td = (t2 - t1)*10**3            #time in miliseconds
            time_medition = TimeMed(td, self.name, j)
            f_le_left.write(f"{str(time_medition.time).replace('.', ',')} \n")
            j += 1

            yield [pyRTOS.timeout(0.1)]
    
    def readSensorFront(self):
        
        j = 0
        sim.simxReadProximitySensor(clientID, frontSensor, sim.simx_opmode_streaming)

        yield

        while True:
            t1 = time.time()  

            msg_front = self.recv()
            sensorFront = sim.simxReadProximitySensor(clientID, frontSensor, sim.simx_opmode_buffer)
           # print("sensor loop")
            if(sensorFront[1] and not msg_front):
                self.send(pyRTOS.Message(SENT_DATA, self, "gira_direita"))

            else:
                for msg in msg_front:
                    if(msg.source.name == "left" and sensorFront[1]):
                        self.send(pyRTOS.Message(SENT_DATA, self, "gira_direita"))
                    if(msg.source.name == "right" and sensorFront[1]):
                        self.send(pyRTOS.Message(SENT_DATA, self, "gira_esquerda"))
           # print(sensorFront)
            
            t2 = time.time()
            td = (t2 - t1)*10**3            #time in miliseconds
            time_medition = TimeMed(td, self.name, j)
            f_le_front.write(f"{str(time_medition.time).replace('.', ',')} \n")
            j += 1

            yield [pyRTOS.timeout(0.1)]

        
    


    pyRTOS.add_task(pyRTOS.Task(ativarMotores, 3, name="motores", mailbox=True))
    pyRTOS.add_task(pyRTOS.Task(pararMotores, 3, name="para_motores", mailbox=True))
    pyRTOS.add_task(pyRTOS.Task(readSensorFront, 2, name="front", mailbox=True))
    pyRTOS.add_task(pyRTOS.Task(readSensorLeft, 2, name="left", mailbox=True))
    pyRTOS.add_task(pyRTOS.Task(readSensorRight, 2, name="right", mailbox=True))
    pyRTOS.add_task(pyRTOS.Task(girarDireita, 1, name="gira_direita", mailbox=True))
    pyRTOS.add_task(pyRTOS.Task(girarEsquerda, 1, name="gira_esquerda", mailbox=True))
    


    pyRTOS.start()

    
    
else:
    print ('Failed connecting to remote API server')