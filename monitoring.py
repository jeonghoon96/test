import serial
import threading


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
cred = credentials.Certificate('./FCM_key.json')

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

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600
)

'''
ret_tem = ""
ret_hum = ""
ret_gas = ""
ret_some = ""
ret_tem_n = 0
ret_hum_n = 0
ret_gas_n = 0
'''

first = 0


#Thread function
#Reading sensors' data from aduino every 1 sec
def th_read():
    
    #Print Sensor Data
    '''
    print("temperature: "+str(ret_tem_n))
    print("humidity: "+str(ret_hum_n))
    print("gas: "+str(ret_gas_n))
    print("Invader: "+str(ret_some))
    '''
    thread=threading.Thread(target=read_data)
    thread.daemon = True
    thread.start()
    
    #read_data()   
    #threading.Timer(1, th_read).start() #Thread operation every 1 sec

def th_sendMSG():

    thread=threading.Thread(target=sendMessage)
    thread.daemon = True
    thread.start()

def th_snap():
    thread=threading.Thread(target=snapshot)
    thread.daemon = True
    thread.start()
    
    #threading.Timer(1, th_read).start()


#Get app token of user
#Realtime push service for alert
#Client get alert in background only  
def sendMessage():
    while(True):
        registration_id = mToken #App token
    
        #Print app token
        print("appToken: "+registration_id)
    
        send_time = int(time.time())
    
        if(g_temp > 30 and (send_time - temp_time) > 30):  
            message_title = "Danger!!"
            message_body = "Temperature High"+"("str(g_temp)+")"
            result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
            print(result) #Push result(Success/Failure)
            temp_time = int(time.time())
    
        else if(g_humi > 50 and (send_time - humi_time) > 30):
            message_title = "Danger!!"
            message_body = "Humidity High"+"("str(g_humi)+")"
            result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
            print(result) #Push result(Success/Failure)
            humi_time = int(time.time())

        sleep(0.5)

'''
def temperature_anal(res):
    ret_tem = res
    global ret_tem_n
    ret_tem_n = float(ret_tem) 
    
    
def humidity_anal(res):
    ret_hum = res
    global ret_hum_n
    ret_hum_n = float(ret_hum)              
    
    
def gas_anal(res):          
    ret_gas = res          #erase \b\r    <- becasuse gas num is not 3 num place .. if gas num 2 place then it is error so i make code this way
    global ret_gas_n
    ret_gas_n = float(ret_gas)
    
        
def pir_anal(res):
    if res == '1' :            # string compare
        global ret_some
        ret_some = 'Movement detected!\r\n'
        
    else :
        ret_some = 'No movement\r\n'
        global num
        num = 0
'''       

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
                print(res1.decode()[0:5])    #Temperature
                print(res1.decode()[6:11])   #Humidity
                print(res1.decode()[12:15])  #Gas
                print(res1.decode()[16])     #PIR sensor
                '''

                g_temp = float(res1.decode()[0:4])
                g_humi = float(res1.decode()[6:10])
                g_gas = float(res1.decode()[12:14])
                
                if res1.decode()[16] == '1':
                    g_move = "Movement detected!\r\n"
                else:
                    g_move = "No movement\r\n"
                    if(num >= 4):
                        num = 0
                
                print(g_temp)
                print(g_humi)
                print(g_gas)
                print(g_move)
                print(time.time())
                '''
                temperature_anal(res1.decode()[0:4])
                humidity_anal(res1.decode()[6:10])
                gas_anal(res1.decode()[12:14])
                pir_anal(res1.decode()[16])
                '''
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
        if g_move == "Movement detected!\r\n" and num < 4:
            camera = Picamera()
            file_dir = '/home/pi/Desktop/web/static/test' + str(num) + '.jpg'
            camera.capture(file_dir)
            num = num + 1
            camera.annotate_text = shot_time
            camera.annotate_text_size = 20
            print(file_dir) #Picture's directory
            camera.close()
            sleep(1)
    
    '''
    global num
    if ret_some == 'Movement detected!\r\n' and num < 3:
        camera = PiCamera()
        file_dir = '/home/pi/Desktop/web/static/test' + str(num) + '.jpg'
        num = num + 1
        camera.capture(file_dir)
        print(file_dir)
        camera.close()
    return
    '''
    
@app.route('/')
def index():
    '''
    global first
    if first == 0:
        print("kk")
        open_browser()
        first = 1
    
    
    global num
    if ret_some == 'Movement detected!\r\n' and num < 3:
        global camera
        
        camera = PiCamera()
        #camera.start_preview()
        #sleep(10)
        file_dir = '/home/pi/Desktop/web/static/test' + str(num) + '.jpg'
        num = num + 1
        camera.capture(file_dir)
        print(file_dir)
        #camera.stop_preview()
        camera.close()
    '''   
    return render_template('index.html', temperature = ret_tem_n, humidity = ret_hum_n, gas=ret_gas_n , somebody = ret_some) 
    

'''
@app.route('/time')
def time():
    a = strftime("%H%M%S", localtime())
    return a


@app.route('/push')
def push():
    
    ref = 'users/'  
    new_ref = ref+id
    dir = db.reference(new_ref)
    
    temp = dir.get()
    for key in temp.keys():
        if(key == 'token'):
            mToken = temp[key]
    
    

    sendMessage()
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

    
    
    return render_template('index.html',temper = 10, gas = 100)




if __name__ == '__main__':
    th_read()
    th_snap()
    th_sendMSG()
    #open_browser()
    app.run(debug=False, host='0.0.0.0')
