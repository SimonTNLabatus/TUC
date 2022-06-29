from __future__ import print_function
from threading import Thread
import can
import time
import enum
class ObjectDictionary(enum.Enum):
    PINCODE = 1
    MACHINETYPE = 2
    AUTOMATICDRIVE = 3
    LIFTSENSOR = 4
    ID = 5

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)


class recive_msg:
    def __init__(self):
        self.run = 1
    def read_input(self):
        self.reset_timer = 1
        while(self.run):
            msg = bus.recv()
            if msg.arbitration_id == 0x60E and msg.data[0] == 0x40:
                self.reset_timer = 1
            elif msg.arbitration_id == 0x40E:
                test_value = [0] * 8
                test_value[0] = 0x80
                test_value[1] = 0x01
                test_value[2] = 0x00
                test_value[3] = 0x00                
                test_value[4] = 0xFF
                test_value[5] = 0xFF
                test_value[6] = 0xFF
                test_value[7] = 0xFF
                if msg.data[1] == ObjectDictionary.PINCODE.value:

                    test_value[0] = 0x4B
                    test_value[2] = ObjectDictionary.PINCODE.value
                    test_value[4] = 83
                    test_value[5] = 59
                elif msg.data[1] == ObjectDictionary.MACHINETYPE.value:

                    test_value[0] = 0x4F
                    test_value[2] = ObjectDictionary.MACHINETYPE.value
                    test_value[4] = 10
                elif msg.data[1] == ObjectDictionary.AUTOMATICDRIVE.value:

                    test_value[0] = 0x4F
                    test_value[2] = ObjectDictionary.AUTOMATICDRIVE.value
                    test_value[4] = 1
                elif msg.data[1] == ObjectDictionary.LIFTSENSOR.value:

                    test_value[0] = 0x4F
                    test_value[2] = ObjectDictionary.LIFTSENSOR.value
                    test_value[4] = 0
                elif msg.data[1] == ObjectDictionary.ID.value:

                    test_value[0] = 0x43
                    test_value[2] = ObjectDictionary.ID.value
                    test_value[4] = 0x52
                    test_value[5] = 0xfa
                    test_value[6] = 0x00
                    test_value[7] = 0x99                     
                msg = can.Message(arbitration_id=0x4E,
                data=test_value)
                bus.send(msg)


    def kill_timer(self):
        self.reset_timer
        i = 0
        while(i < 5):
            time.sleep(1)
            i = i + 1
            if self.reset_timer == 1:
                i = 0
                self.reset_timer = 0
        self.run = 0
        print("Shutting down, missing PDO")

if __name__ == '__main__':
    cp = recive_msg()
    T1 = Thread(target=cp.read_input, args=())
    T2 = Thread(target=cp.kill_timer, args=())
    T1.start()
    T2.start()
    T2.join()
    T1.join()
    