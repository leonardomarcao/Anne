import time
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import hashlib
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import random as random
import atexit
from colorama import Fore, Back, Style 

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
broker=input("Who is broker? ")
i=1 #initialize random integer
filename=".jpg" #format for save file
topic="anne/nightvision" #topic
qos=1 #QoS
data_block_size=268435455 #data block size of payload

#process_message
def process_message(msg):
   """ This is the main receiver code
   """
   print("received ")
   global bytes_in
   if len(msg)==200: #is header or end
      print("found header")
      msg_in=msg.decode("utf-8")
      msg_in=msg_in.split(",,")
      if msg_in[0]=="end": #is it really last packet?
         in_hash_final=in_hash_md5.hexdigest()
         if in_hash_final==msg_in[2]:           
            print("File copied OK -valid hash  ",in_hash_final)
            return -1
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
      bytes_in=bytes_in+len(msg)
      in_hash_md5.update(msg)
      print("found data bytes= ",bytes_in)
      return True
   
#define callback
def on_message(client, userdata, message):
   #time.sleep(1)
   global run_flag
   #print("received message =",str(message.payload.decode("utf-8")))
   ret=process_message(message.payload)
   if ret:
      fout.write(message.payload)
   if ret== -1:
      run_flag=False #exit receive loop
      print("complete file received")

#predict
def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):
    """
    Recognizes faces in given image using a trained KNN classifier
    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

#show_prediction_labels_on_image
def show_prediction_labels_on_image(img_path, predictions):
    """
    Shows the face recognition results visually.
    :param img_path: path to image to be recognized
    :param predictions: results of the predict function
    :return:
    """    
    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # There's a bug in Pillow where it blows up with non-UTF-8 text
        # when using the default bitmap font
        name = name.encode("UTF-8")

        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs
    del draw
    
    # Display the resulting image
    pil_image.save(img_path)
   
#goodbye program python
@atexit.register
def goodbye():
    try:            
        client.loop_stop()  #manual loop
        client.disconnect() #disconnect         
        fout.close()
        pass
    finally:
        print("terminate")

while True:   
    i=random.randrange(0, 101, 2)
    file_out="copy"+str(i)+filename
    fout=open(file_out,"wb")    
    bytes_in=0
    client= paho.Client(client_id="client-receive-001", clean_session=True, userdata=None, transport="tcp") 
    ######
    client.on_message=on_message
    client.mid_value=None
    #####
    print("connecting to broker ",broker)
    client.connect(broker)#connect
    #client.loop_start() #start loop to process received messages
    print("subscribing ")  
    client.subscribe(topic)#subscribe
    start=time.time()
    time_taken=time.time()-start
    in_hash_md5 = hashlib.md5()
    run_flag=True
    while run_flag:
      client.loop()  #manual loop
    pass
    client.disconnect() #disconnect
    #client.loop_stop() #stop loop
        
    if __name__ == "__main__":
        # STEP 2: Using the trained classifier, make predictions for unknown images
        image_file = file_out
        full_file_path = os.path.join(file_out)

        print("Looking for faces in {}".format(image_file))
        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        predictions = predict(full_file_path, model_path="trained_knn_model.clf")

        # Print results on the console 
        for name, (top, right, bottom, left) in predictions:
            print(Fore.RED + "- Found {} at ({}, {})".format(name, left, top))
            print(Style.RESET_ALL) 
            if name is not None:       
                if name != "unknown":                            
                    publish.single("anne/padlock", payload=name[:1], qos=0, retain=False, hostname=broker, client_id="", keepalive=60, will=None, transport="tcp")
                else:
                    publish.single("anne/padlock", payload="-1", qos=0, retain=False, hostname=broker, client_id="", keepalive=60, will=None, transport="tcp")

        # Display results overlaid on an image
        show_prediction_labels_on_image(os.path.join(image_file), predictions)

        fout.close()

    
    

