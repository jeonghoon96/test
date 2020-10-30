from time import localtime, strftime
from flask import Flask, render_template
import serial
from picamera import PiCamera
from time import sleep
import webbrowser
from pyfcm import FCMNotification
import firebase_admin
from firebase_admin import credentials, db
import threading

push_service = FCMNotification(api_key="AAAA6oFTOZk:APA91bGV8mG3Qm5sVNHc93ek8veiUEU80GcgzXEPYKbH1u0rOIvGAguj5yEDJaaPhKRMmH92bAyssEeE42hxLNrPhopM4rfLd-XRR6jDdSuUmKL1o3uoeuUCKGEzV5VzenOmNLlo3syo")


n = 0

cred = credentials.Certificate('./FCM_key.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://fcmtest-2ed81.firebaseio.com/'
})
th = 0
ser = serial.Serial(
port='/dev/ttyACM0',
baudrate = 9600
)
def th_read():
    global th
    th = th+1
    #print(str(th)+"thread starts!")
    #print("temperature: "+str(ret_tem_n))
    #print("humidity: "+str(ret_hum_n))
    #print("gas: "+str(ret_gas_n))
    #print("Invader: "+str(ret_some))
    thread=threading.Thread(target=read_data)
    thread.daemon=True
    thread.start()
    #read_data()
    #snapshot()
    #threading.Timer(1, th_read).start()


def sendMessage(mToken):
    global n
    n += 1
    registration_id = mToken
    print("appToken: "+registration_id)

    data_message = {
        "body" : str(n) + "test"
    }

    message_title = "Push test"
    message_body = "Hi chiho"
    result = push_service.notify_single_device(registration_id = registration_id, message_title = message_title, message_body = message_body)
    print(result)


id = ""




ret_tem = ""
ret_hum = ""
ret_gas = ""
ret_some = ""
ret_tem_n = 0
ret_hum_n = 0
ret_gas_n = 0
num = 0
first = 0
app = Flask(__name__)
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
       

def read_data() :
    '''
    ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600
)
    '''
    global ser
    while True:
        
        if ser.readable():
            #try:
        
            res = ser.readline()             #temperature string
            
            #print(res.decode()[:len(res)-1])
            if res.decode()[:len(res)-1] == "start\r" :
                res1 = ser.readline()
                print(res1.decode()[0:5])
                print(res1.decode()[6:11])
                print(res1.decode()[12:15])
                print(res1.decode()[16])
             
               
                    
                temperature_anal(res1.decode()[0:4])
                humidity_anal(res1.decode()[6:10])
                gas_anal(res1.decode()[12:14])
                pir_anal(res1.decode()[16])
                     
                
                sleep(1)
                #return 0
               
              
def open_browser():
    url = 'http://0.0.0.0:5000'
    webbrowser.open_new(url)
    return

def snapshot():
    global num
    if ret_some == 'Movement detected!\r\n' and num < 3:
        camera = PiCamera()
        file_dir = '/home/pi/Desktop/web/static/test' + str(num) + '.jpg'
        num = num + 1
        camera.capture(file_dir)
        print(file_dir)
        camera.close()
    return

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
    
    

    sendMessage(mToken)
    return render_template('index.html', temper=10, gas=100)

@app.route('/id/<_id>')
def hello(_id):
    global id
    id = _id
    print(id)
    return render_template('index.html',temper = 10, gas = 100)




if __name__ == '__main__':
    th_read()
    #open_browser()
    app.run(debug=False, host='0.0.0.0')
