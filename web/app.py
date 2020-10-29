from time import localtime, strftime
from flask import Flask, render_template
import serial

gas_p = 200
temperature_p = 300
humidity_p = 400
somebody_p = 500


app = Flask(__name__)
def temperature_anal(res):
    ret = res[0:5]                        #erase \r
    if float(ret) > 45 :                  # temperature num -> type casting (string to float) and if temperature is upper 45
        print("danger!")
    else :
        print(float(ret))                 # then now temperature is 
    
def humidity_anal(res):
    ret = res[0:5]                        #erase \r
    if float(ret) < 30 :                  # type casting (string to float) and if humidity is lower 30
        print("turn on humidifier")       # this way is using AI   not our skill 
    
def gas_anal(res):          
    ret = res[0:len(res) - 2]             #erase \b\r    <- becasuse gas num is not 3 num place .. if gas num 2 place then it is error so i make code this way
    if int(ret) > 380 :                   # type casting (string to int) and if gas is upper 380
        print("watch out your house!")    
    
def pir_anal(res):
    if res == 'Welcome!\r\n' :            # string compare
        print("intruder!!")
    else :
        print("no way~!")

def read_data() :
    ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600
)
    while True:
        if ser.readable():
            res = ser.readline()             #temperature string
            if res.decode()[:len(res)-1] == "temperature\r" :
                res1 = ser.readline()        #temperature num
                res2 = ser.readline()        #humidity string
                res3 = ser.readline()        #humidity num
                res4 = ser.readline()        #gas string      
                res5 = ser.readline()        #gas num
                res6 = ser.readline()        # pir sensor
                '''print(res.decode()[:len(res)-1])
                print(len(res))
                print(res)
                print(res1)
                print(res2)
                print(res3)
                print(res4)
                print(res5)
                print(res6)'''
                temperature_anal(res1)
                humidity_anal(res3)
                gas_anal(res5)
                pir_anal(res6)
                if res.decode()[:len(res)-1] == "400\r":
                    print("kk")
                    return 30
                else:
                    print("ll")
                    return 50
                
            else:
                print("no temerature!!")


            
@app.route('/')
def index():
    return render_template('index.html', temper=read_data(), gas=gas_p , temperature = temperature_p, humidity = humidity_p, somebody = somebody_p)



@app.route('/time')
def time():
    a = strftime("%H%M%S", localtime())
    return a

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
