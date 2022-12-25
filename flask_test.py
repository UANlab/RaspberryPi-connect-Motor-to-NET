import csv
import time

from flask import Flask, render_template, jsonify, Response
import os
import cv2

app = Flask(__name__)
file = open('MS.csv', mode='w', newline='')
writer = csv.writer(file)
writer.writerow('7')
file.close()
file = open('required_speed.csv', mode='w', newline='')
writer = csv.writer(file)
writer.writerow('0')
file.close()


def get_data():  # 從各個csv檔案取得想要的參數
    file = open("data_refresh.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    file.close()
    Times = dataList[0][0]
    speed = dataList[0][1]
    V = dataList[0][2]
    I = dataList[0][3]

    file = open("required_speed.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    R_speed = dataList[0][0]
    file.close()

    file = open("Kp.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    Kp = dataList[0][0]
    file.close()

    file = open("Ki.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    Ki = dataList[0][0]
    file.close()

    file = open("Kd.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    Kd = dataList[0][0]
    file.close()

    file = open("RPI_Kp.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    file.close()
    RPI_Kp = dataList[0][0]

    file = open("RPI_Ki.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    file.close()
    RPI_Ki = dataList[0][0]

    file = open("RPI_Kd.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    file.close()
    RPI_Kd = dataList[0][0]

    file = open("PID_switch.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    file.close()
    PID_S = dataList[0][0]
    if PID_S == '1':
        PID_S = 'ON'
    elif PID_S == '0':
        PID_S = 'OFF'
    else:
        PID_S = 'ERROR'

    file = open("MS.csv")
    reader = csv.reader(file)
    dataList = list(reader)
    file.close()
    MS = dataList[0][0]
    if MS == '15':
        MS = 'ON'
    elif MS == '7':
        MS = 'OFF'
    else:
        MS = 'ERROR'
    return str(Times), str(speed), str(R_speed), V, I, Kp, Ki, Kd, MS, RPI_Kp, RPI_Ki, RPI_Kd, PID_S


def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/pid/<PID_switch>")
def PID_state(PID_switch=None):
    try:
        print("PID_S:" + PID_switch)
        file = open('PID_switch.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow([PID_switch])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


@app.route("/w/<MS>")
def Motor_State(MS=None):
    try:
        print("MS:" + MS)
        file = open('MS.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow([MS])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


@app.route("/s/<required>")
def change_speed(required=None):  # 改變速度用的函式，從Web端接收required變數
    try:
        required = int(required)  # 確認輸入的是數字
        required = str(required)
        print("SPEED:" + required)
        file = open('required_speed.csv', mode='w', newline='')  # 把required寫入csv檔
        writer = csv.writer(file)
        writer.writerow([required])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


@app.route("/Rp/<RPI_Kp>")
def change_RPI_Kp(RPI_Kp=None):
    try:
        print("0000")
        RPI_Kp = float(RPI_Kp)  # 確認輸入的是數字
        RPI_Kp = str(RPI_Kp)
        print("RPI_KP:" + RPI_Kp)
        file = open('RPI_Kp.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow([RPI_Kp])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


@app.route("/Ri/<RPI_Ki>")
def change_RPI_Ki(RPI_Ki=None):
    try:
        RPI_Ki = float(RPI_Ki)  # 確認輸入的是數字
        RPI_Ki = str(RPI_Ki)
        print("RPI_KI:" + RPI_Ki)
        file = open('RPI_Ki.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow([RPI_Ki])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


@app.route("/Rd/<RPI_Kd>")
def change_RPI_Kd(RPI_Kd=None):
    try:
        RPI_Kd = float(RPI_Kd)  # 確認輸入的是數字
        RPI_Kd = str(RPI_Kd)
        print("RPI_KD:" + RPI_Kd)
        file = open('RPI_Kd.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow([RPI_Kd])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


@app.route("/p/<r_Kp>")
def change_Kp(r_Kp=None):
    try:
        r_Kp = float(r_Kp)  # 確認輸入的是數字
        r_Kp = str(r_Kp)
        print("KP:" + r_Kp)
        file = open('Kp.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow([r_Kp])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


@app.route("/i/<r_Ki>")
def change_Ki(r_Ki=None):
    try:
        r_Ki = float(r_Ki)  # 確認輸入的是數字
        r_Ki = str(r_Ki)
        print("KI:" + r_Ki)
        file = open('Ki.csv', mode='w', newline='')
        writer = csv.writer(file)
        writer.writerow([r_Ki])
        file.close()
        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
    except:
        print("Invalid Input")
        return "error"


#@app.route("/d/<r_Kd>")
#def change_Kd(r_Kd=None):
#    try:
#       r_Kd = float(r_Kd)  # 確認輸入的是數字
#        r_Kd = str(r_Kd)
#        print("KD:" + r_Kd)
#        file = open('Kd.csv', mode='w', newline='')
#        writer = csv.writer(file)
#        writer.writerow([r_Kd])
#        file.close()
#        return "success"  # 在Web端使用jquery函式庫的get()函示時，必須得回傳字串
#    except:
#        print("Invalid Input")
#        return "error"


@app.route("/update", methods=['GET', 'POST'])  # 資料傳輸
def update_data():
    data = list(get_data())
    # data[0] = time.time()
    data[1] = int(data[1])
    return jsonify(TT=data[0], Sp=data[1], RS=data[2], V=data[3], I=data[4], Kp=data[5], Ki=data[6], Kd=data[7],
                   MS=data[8], RPI_Kp=data[9], RPI_Ki=data[10], RPI_Kd=data[11], PID_S=data[12])
    # 轉Json丟給html


@app.route("/")
def main():
    return render_template('Interface.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
