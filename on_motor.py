import time
import can
import canopen
import struct
import os
from datetime import datetime, timezone
import csv

file = open("required_speed.csv", mode='r', encoding="utf-8")  # 讀要求的速度
reader = csv.reader(file)
dataList = list(reader)
required_speed = dataList[0][0]
Last_required_speed = required_speed
input_speed = float(required_speed)
file.close()

file1 = open("Kp.csv", mode='r', encoding="utf-8")
file2 = open("Ki.csv", mode='r', encoding="utf-8")
file3 = open("Kd.csv", mode='r', encoding="utf-8")
reader1 = csv.reader(file1)
reader2 = csv.reader(file2)
reader3 = csv.reader(file3)
dataList1 = list(reader1)
dataList2 = list(reader2)
dataList3 = list(reader3)
Kp = float(dataList1[0][0])
Ki = float(dataList2[0][0])
Kd = float(dataList3[0][0])
# print(Kp + Ki + Kd)
file1.close()
file2.close()
file3.close()
MS = '7'
Last_Kp = Kp
Last_Ki = Ki
Last_MS = MS
error_sum = 0


# print('\n\rCAN Rx test')
# print('Bring up CAN0....')
# os.system("sudo ip link set can0 up type can bitrate 500000 loopback on")
# time.sleep(0.1)

# try:
#    bus = can.interface.Bus(channel='can0', bustype='socketcan')
# except OSError:
#    print('Cannot find PiCAN board.')
#    exit()

# print('Ready')

def convert_1to4(value):
    x4 = int((value / 16777216))
    x3 = int((value % 16777216 / 65536))
    x2 = int((value % 16777216 % 65536 / 256))
    x1 = int((value % 16777216 % 65536 % 256 / 1))
    converted = [x1, x2, x3, x4]
    return converted


def convert_4to1(word):
    x1 = int(word[8:10], 16)
    x2 = int(word[10:12], 16)
    x3 = int(word[12:14], 16)
    x4 = int(word[14:16], 16)
    if x4 >= 240:
        x5 = ((255 - x1) + (256 * (255 - x2)) + (65536 * (255 - x3)) + (16777216 * (255 - x4)))
    else:
        x5 = x1 + (256 * x2) + (65536 * x3) + (16777216 * x4)
    # print(x5)
    return x5


can_interface = 'can0'
bus = can.interface.Bus(channel=can_interface, bustype='socketcan', bitrate=500000)
i = 0
f = open("data.csv", "w")
f.close()
while True:
    # if (i+1)%100 == 0:
    # os.system('sudo ip link set can0 down')
    # time.sleep(1)
    # os.system('sudo ip link set can0 up type can bitrate 500000')
    # time.sleep(1)
    try:
        msg1 = can.Message(
            arbitration_id=0x601, data=[0x20, 0x40, 0x60, 0x00, 0x07, 0x00, 0x00, 0x00], is_extended_id=False,
            check=True)
        msg2 = can.Message(
            arbitration_id=0x601, data=[0x20, 0x42, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False,
            check=True)
        msg4 = can.Message(
            arbitration_id=0x601, data=[0x40, 0x44, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False,
            check=True)
        msgV = can.Message(
            arbitration_id=0x601, data=[0x40, 0x10, 0x2C, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False,
            check=True)
        msgI = can.Message(
            arbitration_id=0x601, data=[0x40, 0x0A, 0x2C, 0x00, 0x00, 0x00, 0x00, 0x00], is_extended_id=False,
            check=True)
        try:
            if i == 0:
                bus.flush_tx_buffer()
                bus.send(msg1)
                message = bus.recv(0.01)
                print(message)
                bus.send(msg2)
                message = bus.recv(0.01)
                # print(message)
                # print(f"Message sent on {bus.channel_info}")
                # message = bus.recv()

            # print(msg2)
            # print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")
        # try:
        i = i + 1
        # print(sys_time.second, sys_time.microsecond)
        # print(message.data)
        # print("receive from can byte to hex: ")
        # print(int(message.data.hex()[8:]))
        # print()

        # x1 = int(message.data.hex()[8:10],16)
        # x2 = int(message.data.hex()[10:12],16)
        # x3 = int(message.data.hex()[12:14],16)
        # x4 = int(message.data.hex()[14:16],16)
        # print(x1,x2,x3,x4)
        try:
            file = open("required_speed.csv", mode='r', encoding="utf-8")  # 讀要求的速度
            reader = csv.reader(file)
            dataList = list(reader)
            required_speed = int(dataList[0][0])
            file.close()

            file1 = open("Kp.csv", mode='r', encoding="utf-8")
            file2 = open("Ki.csv", mode='r', encoding="utf-8")
            file3 = open("Kd.csv", mode='r', encoding="utf-8")
            reader1 = csv.reader(file1)
            reader2 = csv.reader(file2)
            reader3 = csv.reader(file3)
            dataList1 = list(reader1)
            dataList2 = list(reader2)
            dataList3 = list(reader3)
            Kp = float(dataList1[0][0])
            Ki = float(dataList2[0][0])
            Kd = float(dataList3[0][0])
            # print(Kp + Ki + Kd)
            file1.close()
            file2.close()
            file3.close()

            file = open("MS.csv", mode='r', encoding="utf-8")
            reader = csv.reader(file)
            dataList = list(reader)
            file.close()
            MS = dataList[0][0]


            # print("Times:" + str(times) + " Speed:" + str(speed))

            if required_speed != Last_required_speed:
                # required speed 轉換
                speed_data_package = [0x20, 0x42, 0x60, 0x00] + convert_1to4(required_speed)
                # print(speed_data_package)
                speed_msg = can.Message(
                    arbitration_id=0x601, data=speed_data_package, is_extended_id=False,
                    check=True
                )
                bus.send(speed_msg)
                message = bus.recv(0.01)
                error_sum = 0

            if Kp != Last_Kp or Ki != Last_Ki:
                # print(Kp)
                # print(Last_Kp)
                cs01 = int((float(Kp) * 100 / 7.5) * 10000)
                Kp_data_package = [0x20, 0x01, 0x27, 0x00] + convert_1to4(cs01)
                cs05 = int(cs01 / 10000 * 7.5 / (100 * float(Ki)) * 1000)
                Ki_data_package = [0x20, 0x05, 0x27, 0x00] + convert_1to4(cs05)
                # print(Kp_data_package)
                # print(Ki_data_package)
                cs01_msg = can.Message(
                    arbitration_id=0x601, data=Kp_data_package, is_extended_id=False,
                    check=True
                )
                bus.send(cs01_msg)
                message = bus.recv(0.01)
                cs05_msg = can.Message(
                    arbitration_id=0x601, data=Ki_data_package, is_extended_id=False,
                    check=True
                )
                bus.send(cs05_msg)
                message = bus.recv(0.01)
            if MS != Last_MS:
                print(MS)
                MS = int(MS)
                MS_data_package = [0x20, 0x40, 0x60, 0x00, MS, 0x00, 0x00, 0x00]
                msgms = can.Message(
                    arbitration_id=0x601, data=MS_data_package, is_extended_id=False,
                    check=True
                )
                bus.send(msgms)
                message = bus.recv(0.01)
                MS = str(MS)
                error_sum = 0;

            Last_required_speed = required_speed
            Last_Kp = Kp
            Last_Ki = Ki
            Last_MS = MS
        except:
            print('Load Error')
        try:
            bus.send(msg4)
            message = bus.recv(0.01)
            sys_time = datetime.fromtimestamp(message.timestamp)
            time_converted = str(sys_time.minute) + "." + str(sys_time.second) + "." + str(sys_time.microsecond)
            if i == 1:
                start_time_minute = sys_time.minute
                start_time_second = sys_time.second
                start_time_microsecond = sys_time.microsecond
                Last_time_pass = -0.01;
                Last_error = 0;
            time_pass = str((sys_time.minute - start_time_minute) * 60 + (sys_time.second - start_time_second)
                            + (sys_time.microsecond - start_time_microsecond) / 1000000)
            print(time_converted + " , " + time_pass)
            speed = convert_4to1(message.data.hex())
            bus.send(msgV)
            messageV = bus.recv(0.01)
            Voltage = convert_4to1(messageV.data.hex()) / 10
            bus.send(msgI)
            messageI = bus.recv(0.01)
            Current = convert_4to1(messageI.data.hex()) / 100
            #Voltage = 0
            #Current = 0
            print("converted value: ")
            print(speed, Voltage, Current)

            f = open("data.csv", "a")
            f.write(time_converted + ",")
            f.write(time_pass + ",")
            f.write(str(speed) + ",")
            f.write(str(required_speed) + ",")
            f.write(str(input_speed) + ",")
            f.write(str(Voltage) + ",")
            f.write(str(Current) + "\n")
            f.close()

            f = open("data_refresh.csv", "w")
            f.write(time_converted + ",")
            f.write(str(speed) + ",")
            f.write(str(Voltage) + ",")
            f.write(str(Current) + "\n")
            f.close()
        except:
            print("Data Message Lost Error")
        
        #if i%10 == 9:
        #    try:
        #        for j in range(1,10):
        #            bus.recv(0.01)
        #            j = j + 1
        #    except:
        #        print("clean buffer problem")

        # PID
        try:
            file1 = open("RPI_Kp.csv", mode='r', encoding="utf-8")
            file2 = open("RPI_Ki.csv", mode='r', encoding="utf-8")
            file3 = open("RPI_Kd.csv", mode='r', encoding="utf-8")
            reader1 = csv.reader(file1)
            reader2 = csv.reader(file2)
            reader3 = csv.reader(file3)
            dataList1 = list(reader1)
            dataList2 = list(reader2)
            dataList3 = list(reader3)
            file1.close()
            file2.close()
            file3.close()
            RPI_Kp = float(dataList1[0][0])
            RPI_Ki = float(dataList2[0][0])
            RPI_Kd = float(dataList3[0][0])
            # print(Kp + Ki + Kd)
            file = open("PID_switch.csv", mode='r', encoding="utf-8")
            reader = csv.reader(file)
            dataList = list(reader)
            file.close()
            PID_switch = dataList[0][0]
        except:
            print("PID Parameter Load Error")
        
        try:
            if MS == '15':
                if PID_switch == '1':
                    dt = float(time_pass) - Last_time_pass
                    error = float(required_speed) - speed
                    error_sum += (error * dt)
                    dError = (error - Last_error) / dt                
                    input_speed =int(RPI_Kp * error + RPI_Ki * error_sum + RPI_Kd * dError)
                    print('PID:')
                    print(input_speed)
                    print(error_sum)
                    input_speed_data_package = [0x20, 0x42, 0x60, 0x00] + convert_1to4(input_speed)
                    # print(input_speed_data_package)
                    input_speed_msg = can.Message(
                        arbitration_id=0x601, data=input_speed_data_package, is_extended_id=False,
                        check=True
                    )
                    bus.send(input_speed_msg)
                    message = bus.recv(0.01)
                    Last_error = error
                elif input_speed != required_speed:
                    Last_required_speed = 'A'
        except:
            print('PID Error')
        Last_time_pass = float(time_pass)
            


    except KeyboardInterrupt:
        msg3 = can.Message(
            arbitration_id=0x601, data=[0x20, 0x40, 0x60, 0x00, 0x07, 0x00, 0x00, 0x00], is_extended_id=False,
            check=True)
        bus.send(msg3)
        break
