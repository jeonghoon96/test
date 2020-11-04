#!/usr/bin/ python3
import serial
import threading
import firebase_admin
import time

from firebase_admin import credentials, db
from picamera import PiCamera
from time import sleep
from pyfcm import FCMNotification
from flask import Flask, render_template
from time import localtime, strftime, sleep

#from flask import Flask, render_template
#import serial
#from picamera import PiCamera
#from time import sleep
#import webbrowser
#from pyfcm import FCMNotification
#import firebase_admin
#from firebase_admin import credentials, db
#import threading
#import webbrowser

#Firebase(FCM) Authentication
push_service = FCMNotification(api_key="AAAA6oFTOZk:APA91bGV8mG3Qm5sVNHc93ek8veiUEU80GcgzXEPYKbH1u0rOIvGAguj5yEDJaaPhKRMmH92bAyssEeE42hxLNrPhopM4rfLd-XRR6jDdSuUmKL1o3uoeuUCKGEzV5VzenOmNLlo3syo")
cred = credentials.Certificate('/home/pi/Desktop/project/web/FCM_key.json')

#FCM Database URL
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://fcmtest-2ed81.firebaseio.com/'
})

#Flask module
app = Flask(__name__)

#Global variable initialization
id = ""
mToken = ""
g_temp = 0
g_humi = 0
g_gas = 0
g_move = ""
num = 0

temp_time = 0
humi_time = 0
gas1_time = 0
gas2_time = 0
move_time = 0

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600
)



#Thread function
#Reading sensors' data from aduino every 1 sec
def th_read():
    
    #Print Sensor Data
    thread=threading.Thread(target=read_data)
    thread.daemon = True
    thread.start()
    

def th_sendMSG():

    thread=threading.Thread(target=sendMessage)
    thread.daemon = True
    thread.start()

def th_snap():
    thread=threading.Thread(target=snapshot)
    thread.daemon = True
    thread.start()
    


#Get app token of user
#Realtime push service for alert
#Client get alert in background only  
def sendMessage():
    
    global temp_time
    global humi_time
    global gas1_time
    global gas2_time
    global move_time

    while(True):
        registration_id = mToken #App token
    
        #Print app token
        #print("appToken: "+registration_id)
    
        send_time = int(time.time())
    
        if(g_temp > 30 and (send_time - temp_time) > 30):  
            message_title = "Danger!!"
            message_body = "Temperature High"+"("+str(g_temp)+")"
            result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
            print(result) #Push result(Success/Failure)
            temp_time = int(time.time())
    
        elif(g_humi > 50 and (send_time - humi_time) > 30):
            message_title = "Danger!!"
            message_body = "Humidity High"+"("+str(g_humi)+")"
            result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
            print(result) #Push result(Success/Failure)
            humi_time = int(time.time())
        elif(g_gas >= 200 and g_gas < 250 and (send_time - gas1_time) > 60):
            message_title = "Danger!!"
            message_body = "valve check"+"("+str(g_gas)+")"
            result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
            print(result) #Push result(Success/Failure)
            gas1_time = int(time.time())
        elif(g_gas >= 250 and (send_time - gas2_time) > 30):
            message_title = "Danger!!"
            message_body = "Gas leakage"+"("+str(g_gas)+")"
            result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
            print(result) #Push result(Success/Failure)
            gas2_time = int(time.time())
        
        elif(g_move == "Movement detected!" and (send_time - move_time) > 30):
            message_title = "Danger"
            message_body = "Somebody invaded!"
            result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
            move_time = int(time.time()) 
        sleep(0.5)

     

#Getting data from aduino with serial connection
def read_data() :
    
    

    global g_temp
    global g_humi
    global g_gas
    global g_move
    global num
    global ser
    
    while True:   
        if ser.readable():
            res = ser.readline()                         
            if res.decode()[:len(res)-1] == "start\r" :
                res1 = ser.readline()

                #Print serial data
                '''
                print(res1)
                print(res1.decode()[0:5])    #Temperature
                print(res1.decode()[6:11])   #Humidity
                print(res1.decode()[12:15])  #Gas
                print(res1.decode()[16])     #PIR sensor
                '''
                
                g_temp = float(res1.decode()[0:5])
                g_humi = float(res1.decode()[6:11])
                g_gas = int(res1.decode()[12:16])
                g_gas -= 1000

                if res1.decode()[17] == '1':
                    g_move = "Movement detected!"
                else:
                    g_move = "No movement"
                    if(num >= 4):
                        num = 0
                
                print("temperature:"+str(g_temp))
                print("humi:"+str(g_humi))
                print("gas:"+str(g_gas))
                print(g_move)
                print(strftime("%H:%M:%S", localtime()))
                print("\n")                
                sleep(1)
                #return
               
'''              
def open_browser():
    url = 'http://0.0.0.0:5000'
    webbrowser.open_new(url)
    return
'''

def snapshot():

    while True:
        global num 
        shot_time = time.strftime("%y%m%d_%H%M%S", time.localtime())
        if g_move == "Movement detected!" and num < 4:
            camera = PiCamera()
            file_dir = '/home/pi/Desktop/project/web/static/test' + str(num) + '.jpg'
            camera.capture(file_dir)
            num = num + 1
            camera.annotate_text = shot_time
            camera.annotate_text_size = 20
            print(file_dir) #Picture's directory
            camera.close()
            sleep(1)
    
        
@app.route('/')
def index():
      
    return render_template('index.html', temperature = g_temp, humidity = g_humi, gas= g_gas , somebody = g_move) 
    


'''
@app.route('/push')
def push():
    
    ref = 'users/'  
    new_ref = ref+id
    dir = db.reference(new_ref)
    
    temp = dir.get()
    for key in temp.keys():
        if(key == 'token'):
            mToken = temp[key]
    
    

    #sendMessage()
    return render_template('index.html', temper=10, gas=100)
'''

@app.route('/id/<_id>')
def hello(_id):
    
    global id
    global mToken
    id = _id
    print(id)
    ref = 'users/'  
    new_ref = ref+id
    dir = db.reference(new_ref)
    
    temp = dir.get()
    for key in temp.keys():
        if(key == 'token'):
            mToken = temp[key]

    
    return "Your ID: "+str(id)+"\n"+"Your token: "+str(mToken) 
    #return render_template('index.html',temper = 10, gas = 100)




if __name__ == '__main__':
    th_read()
    th_snap()
    th_sendMSG()
    #open_browser()
    app.run(debug=False, host='0.0.0.0')
