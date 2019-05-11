import time
import paho.mqtt.client as paho
import hashlib
import base64
import picamera
from time import sleep
import atexit


broker="192.168.15.250"
#filename="DSCI0027.jpg"
filename="image.png" #file to send
topic="anne/nightvision"
qos=1
data_block_size=268435455
# for outfile as I'm rnning sender and receiver together
def process_message(msg):
   """ This is the main receiver code
   """
   if len(msg)==200: #is header or end
      msg_in=msg.decode("utf-8")
      msg_in=msg_in.split(",,")
      if msg_in[0]=="end": #is it really last packet?
         in_hash_final=in_hash_md5.hexdigest()
         if in_hash_final==msg_in[2]:
            print("File copied OK -valid hash  ",in_hash_final)
         else:
            print("Bad file receive   ",in_hash_final)
         return False
      else:
         if msg_in[0]!="header":
            in_hash_md5.update(msg)
            return True
         else:
            return False
   else:
      in_hash_md5.update(msg)
      return True
#define callback
def on_message(client, userdata, message):
   #print("received message =",str(message.payload.decode("utf-8")))
   process_message(message.payload)

def on_publish(client, userdata, mid):
    #logging.debug("pub ack "+ str(mid))
    client.mid_value=mid
    client.puback_flag=True  


def wait_for(client,msgType,period=0.25,wait_time=40,running_loop=False):
    client.running_loop=running_loop #if using external loop
    wcount=0  
    while True:
        #print("waiting"+ msgType)
        if msgType=="PUBACK":
            if client.on_publish:        
                if client.puback_flag:
                    return True
     
        if not client.running_loop:
            client.loop(.01)  #check for messages manually
        time.sleep(period)
        #print("loop flag ",client.running_loop)
        wcount+=1
        if wcount>wait_time:
            print("return from wait loop taken too long")
            return False
    return True 

def send_header(filename):
   header="header"+",,"+filename+",,"
   header=bytearray(header,"utf-8")
   header.extend(b','*(200-len(header)))
   print(header)
   c_publish(client,topic,header,qos)

def send_end(filename):
   end="end"+",,"+filename+",,"+out_hash_md5.hexdigest()
   end=bytearray(end,"utf-8")
   end.extend(b','*(200-len(end)))
   print(end)
   c_publish(client,topic,end,qos)

def c_publish(client,topic,out_message,qos):
   res,mid=client.publish(topic,out_message,qos)#publish
   if res==0: #published ok
      if wait_for(client,"PUBACK",running_loop=True):
         if mid==client.mid_value:
            print("match mid ",str(mid))
            client.puback_flag=False #reset flag
         else:
            raise SystemExit("not got correct puback mid so quitting")
         
      else:
         raise SystemExit("not got puback so quitting")

@atexit.register
def goodbye():   
   try: 
      camera.stop_preview()
      camera.close()
      client.disconnect() 
      fo.close()
      pass
   finally:
      print("terminate")

while True:
   print("take a picture")
   camera = picamera.PiCamera()   
   try: 
      camera.start_preview()
      camera.capture('image.png', resize=(1280,720))
      camera.stop_preview()
      pass
   finally:
      camera.close()
      fo=open(filename,"rb")


   client= paho.Client(client_id="client-001", clean_session=True, userdata=None, transport="tcp")
   ######
   #client.on_message=on_message
   client.on_publish=on_publish
   client.puback_flag=False #use flag in publish ack
   client.mid_value=None
   #####
   print("connecting to broker ",broker)
   client.connect(broker)#connect
   client.loop_start() #start loop to process received messages
   print("subscribing ")
   client.subscribe(topic)#subscribe
   start=time.time()
   print("publishing ")
   send_header(filename)
   Run_flag=True
   count=0
   out_hash_md5 = hashlib.md5()
   in_hash_md5 = hashlib.md5()
   bytes_out=0

   while Run_flag:
      chunk=fo.read(data_block_size)
      if chunk:
         out_hash_md5.update(chunk)
         out_message=chunk
         #print(" length =",type(out_message))
         c_publish(client,topic,out_message,qos)
            
      else:
         #send hash
         out_message=out_hash_md5.hexdigest()
         send_end(filename)
         #print("out Message ",out_message)
         res,mid=client.publish("anne/nightvision",out_message,qos=1)#publish
         Run_flag=False
   time_taken=time.time()-start
   print("took ",time_taken)
   client.disconnect() #disconnect
   fo.close()