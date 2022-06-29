from __future__ import print_function
from threading import Thread
import can
import time

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)

class send_can_proxy:
    def __init__(self):
        self.run_test_sequence = 1
        # Create a varibale to save all the test data from Eq. an array
    def request_sdo(self, requested_data):
            # This function will request data over CAN to DUT, this function is completed, no changes should be necessary
            self.requested_data = requested_data
            self.waiting_for_msg = 1
            sdo_timeout = 0
            msg = can.Message(arbitration_id=0x40E,
                  data=[0x40, requested_data])
            try:
                bus.send(msg)
                print("Message sent on {}".format(bus.channel_info))
            except can.CanError:
                print("Message NOT sent")

            while self.waiting_for_msg and sdo_timeout < 5:
                time.sleep(1)    
                sdo_timeout = sdo_timeout + 1

    def read_sdo(self): 
        # This function should save all the test data that is sent over CAN
        # This function is not completed, complete the function
        while self.run_test_sequence:
            msg = bus.recv()
            if msg.arbitration_id == 0x4E:
                if msg.data[0] == 0x43:
                    print("Data read successfuly 1")
                elif msg.data[0] == 0x47:
                    print("Data read successfuly 2")
                elif msg.data[0] == 0x4B:
                      print("Data read successfuly 3")
                elif msg.data[0] == 0x4F:   
                      print("Data read successfuly 4")

    def test_sequence_done(self):
        #Print the collected test data and test result here
        # Test 1 | Data : [...] | Result Pass/Fail  
        # Test 2 | Data : [...] | Result Pass/Fail  
        self.run_test_sequence = 0            


def start_and_wait_for_thread(can_proxy, requested_data):
    # Will call request_sdo and request data requested_data
    # All tests data will be requested from this function
    T2 = Thread(target=can_proxy.request_sdo, args=(requested_data,))
    T2.start()
    T2.join()


def main():
    can_proxy = send_can_proxy()
    T1 = Thread(target=can_proxy.read_sdo, args=())
    T1.start()
    start_and_wait_for_thread(can_proxy, 1)
    # Add the rest of the data requests 
    can_proxy.test_sequence_done()
    T1.join()
    

if __name__ == '__main__':
    main()
