"""
 ========================================================================
 Project Name: GROOT
 Description: The role of the Groot is to frequently moniter the 
     plant, identify if there is sufficient amount of water, sunlight
     and temperature, it can also detect if there is any harm caused
     to the plants and takes a picture of it to mail it to his boss
 Date created: 14-03-2020    
 =========================================================================
"""

#Importing all the required libraries
import RPi.GPIO as GPIO
from picamera import PiCamera
from gpiozero import MotionSensor
import Adafruit_MCP3008 as mcp
import Adafruit_DHT
from time import sleep
import time
from datetime import date
from csv import writer
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)  # Setup the red LED 
GPIO.setup(18, GPIO.OUT)  # Setup the blue LED

pir=MotionSensor(17)  # Setting up the PIR Motion Sensor

camera=PiCamera()  # Setting up the Pi Camera Module
camera.rotation = 180  # Rotating the camera orientation if it is not angled properly

mcpval = mcp.MCP3008(clk=11, cs=8, miso=9, mosi=10)

dht = Adafruit_DHT.DHT11  # Importing DHT11 library from Addafruit Library

# Setting the mail client
fromaddr = "frommailaddress@exapmle.com"
toaddr = "toaddress@example.com"
msg = MIMEMultipart()   # instance of MIMEMultipart 
msg['From'] = fromaddr   # storing the senders email address 
msg['To'] = toaddr   # storing the receivers email address 

starttime = time.time()
humidity=0; moistval = 0; lightval = 0

def temperature(row_list):
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    print("[VAL] Temperature: {} C, Humidity: {} %" .format(temperature,humidity))
    if temperature <= 34 and temperature >= 20 and humidity <= 75 and humidity >= 35:
        print("[MSG] The weather is alright")
    else:
        print("[MSG] The temperature and Humidity are not suitable")
    temperature = int(temperature); humidity = int(humidity)
    makearow(temperature, row_list)
    makearow(humidity, row_list)
    return row_list

def moisture(row_list):
    moistval = mcpval.read_adc(0)
    print("[VAL] Moisture reading: {}" .format(moistval))
    if moistval >= 930:
        print("[INFO] No Water, Can you please Water me")
        blink(5, "blue")
    elif moistval <= 930 and moistval >= 500:
        print("[MSG] Need some water")
    elif moistval <= 500 and moistval >= 325:
        print("[MSG] I'm doing good now")
    elif moistval <= 325:
        print("[MSG] Can you stop over pouring me please, I'm filled totally")
    moistval= int(moistval)
    makearow(moistval, row_list)
    return row_list

def light(row_list):
    lightval = mcpval.read_adc(1)
    print("[VAL] Light readings: {}" .format(lightval))
    if lightval == 0:
        print("[MSG] Light is insufficient")
    else:
        print("[MSG] The light is alright")
    makearow(lightval, row_list)
    return row_list

def motion():
    if pir.motion_detected:
        timestamp = time.ctime().replace(" ","-").replace(":","")
        image_name = "image-{}.png" .format(timestamp)
        camera.capture('/home/pi/Pictures/Stranger/{}' .format(image_name))
        blink(3,"red")
        file_name1 = image_name
        print("[INFO] Motion Detected")
        print("[INFO] Image Saved" .format(image_name))
        subject = "[MSG] Motion Detected {}" .format(image_name)
        path_name = "/home/pi/Pictures/Stranger/{}" .format(image_name)
        body_message = "\n Check the attachment below for the Image \n Image Source: {} at /home/pi/Pictures/Stranger/" .format(image_name)
        sendmail(subject, file_name1, path_name, body_message)
        sleep(0.5) 
    else:
        return
    sleep(0.5)
    return

def blink(n, color):
    GPIO.output(12,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)
    if color == "blue":
        pin = 18
    elif color == "red":
        pin = 12
    for b in range(n):
        GPIO.output(pin,GPIO.HIGH)
        sleep(0.2)
        GPIO.output(pin,GPIO.LOW)
        sleep(0.2)

def append_csv(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)
    print("[INFO] Row Updated \n[MSG] File name: {}" .format(file_name))
    
def makearow(item_val, row_list):
    row_list.append(item_val)
    return row_list

def sendmail(subject, file_name1, path_name, body_message):
    msg['Subject'] = subject    # storing the subject 
    body = body_message
    msg.attach(MIMEText(body, 'plain')) 
    filename = file_name1
    attachment = open( path_name, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read())  # To change the payload into encoded form 
    encoders.encode_base64(p)     # encode into base64 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p)     # attach the instance 'p' to instance 'msg'
    s = smtplib.SMTP('smtp.gmail.com', 587)     # creates SMTP session 
    s.starttls()     # start TLS for security 
    s.login(fromaddr, "password")   # Authentication 
    text = msg.as_string()  # Converts the Multipart msg into a string
    s.sendmail(fromaddr, toaddr, text)   # sending the mail 
    print("[INFO] Mail Sent\n[MSG] Mailed to {}\n[MSG]Subject: {}" .format(toaddr,subject))
    s.quit()
        
def sendreport():
    file_name1 = "database-groot.csv"
    subject = "Updated Report {}" .format(file_name1)
    path_name = "/home/pi/groot/mspy/{}" .format(file_name1)
    body_message = " Check the attachment below for detailed logs \n File Name: Report {}" .format(file_name1)
    sendmail(subject, file_name1, path_name, body_message)

def main():
    blink(1, "red")
    print("[INFO] Program Run Time {} seconds" .format(round(time.time() - starttime)))
    while True:
        row_list = []
        if round(time.time() - starttime) % 30 <= 1.5:
            print("\n[INFO] Reading Values...")
            print("[INFO] Check Run Time {} seconds" .format(round(time.time() - starttime)))  # Set the time delay for the check
            timestamp1=time.ctime().replace(" ","_").replace(":","-")
            makearow(timestamp1, row_list)
            temperature(row_list)
            light(row_list)
            moisture(row_list)
            csv_file = "database-groot.csv"
            append_csv(csv_file, row_list)
            print("\n")
            #sendreport()
        
        else:
            print("[INFO] Motion Detection Running...")
            motion()
        
        sleep(2.5)

if __name__ == "__main__":
    try:
        main()
        
    except KeyboardInterrupt:
        sendreport()
        pass
    
