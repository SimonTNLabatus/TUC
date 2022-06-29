from __future__ import print_function
import can
import time

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)

class send_can_proxy:
    def send_pdo(self):
        while True: 
            msg = can.Message(arbitration_id=0x60E, data=[0x40]) #Remove this let students write this code 
            try:
                bus.send(msg)
                print("Message sent on {}".format(bus.channel_info))
            except can.CanError:
                print("Message NOT sent")
            time.sleep(4)


def main():
    pdo_handler = send_can_proxy()
    pdo_handler.send_pdo()

if __name__ == '__main__':
    main()
