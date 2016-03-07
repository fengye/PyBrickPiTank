import SocketServer
from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import threading

left_motor_power = 0
right_motor_power = 0
motor2 = PORT_B
motor1 = PORT_C

class MyUDPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        # print data
        mydata = bytearray(data)
        # print(mydata)
        if len(mydata) == 2:
            left_motor_power = (mydata[0] - 128) * 2
            right_motor_power = (mydata[1] - 128) * 2
            if abs(left_motor_power) < 32:
                left_motor_power = 0
            if abs(right_motor_power) < 32:
                right_motor_power = 0
            print( "Power: %d, %d" % (left_motor_power, right_motor_power))

            BrickPi.MotorSpeed[motor1] = -left_motor_power
            BrickPi.MotorSpeed[motor2] = -right_motor_power
            BrickPiUpdateValues()
        else:
            print "Abnormal data len %d" % len(mydata)

        socket = self.request[1]


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Ready"
        while 1:
            BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            time.sleep(.2)              # sleep for 200 ms

if __name__ == "__main__":

    BrickPiSetup()                          # setup the serial port for communication
    BrickPi.MotorEnable[motor1] = 1         #Enable the Motor A
    BrickPi.MotorEnable[motor2] = 1         #Enable the Motor D
    BrickPiSetupSensors()                   #Send the properties of sensors to BrickPi

    thread1 = myThread(1, "Thread-1", 1)
    thread1.setDaemon(True)
    thread1.start()  

    HOST, PORT = "", 9999
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    print 'Start'
    server.serve_forever()

