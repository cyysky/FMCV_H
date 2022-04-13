import tensorflow_hub as hub
import tensorflow as tf
import cv2
import os
import numpy as np
import time
import traceback
import json 
import matplotlib.pyplot as plt

model = None

dict_class = None

#np.set_printoptions(suppress=True)

np.set_printoptions(formatter={'float': lambda x: "{0:0.5f}".format(x)})

def init(s):
    global self
    self = s 

def load():
    global MODEL
    global model
    global dict_class
    MODEL = os.path.join("Profile",self.Config.profile,"CNN_MODEL")
    
    print(MODEL)
    
    if model is not None:
        model = None
        tf.keras.backend.clear_session()
    
    if os.path.exists(MODEL):
        model = tf.keras.models.load_model(MODEL)
        model.summary()
        try:
            with open(os.path.join(MODEL,"name.json")) as f:
                dict_class = json.loads(f.read())
        except:
            traceback.print_exc()
        
def get_class_name(n):
    global dict_class    
    if dict_class is None:
        return str(n)
    else:
        try:
            key_list=list(dict_class.keys())
            val_list=list(dict_class.values())
            ind=val_list.index(n)
            return key_list[ind]
        except:
            traceback.print_exc()
            return str(n)

def predict(name,im): #image size (224,224)  
    global model
    if model is not None:        
        start = time.time()
        im = np.expand_dims(im, axis=0)
        score = model.predict(im)
        score = score[0]
        print(f'{name} {np.argmax(score)} , {round(float(np.max(score)),5)},{score} time {round(time.time() - start,5)}')
        return np.argmax(score),round(float(np.max(score)),5)
    return 0,0
        
def write_images(dir,sub,template):
    w,h = template.shape[::-1]
    for file in os.listdir(dir):
        if file.endswith(".jpg"):
            print(file)
            if not os.path.exists(os.path.join("TRAIN",sub,file)):
                temp_im_color = cv2.imread(os.path.join(dir,file))
                temp_im=cv2.cvtColor(temp_im_color, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(temp_im,template,cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                x1,y1 = max_loc            
                cropped_im = temp_im_color[y1:y1+h,x1:x1+w]            
                cv2.imwrite(os.path.join("TRAIN",sub,file),cropped_im)   

def create_model(classes):
    global model

    model = tf.keras.Sequential([
     hub.KerasLayer(os.path.join("FMCV","Ai","MobileNetV3"),
     trainable=False),
     #tf.keras.layers.Dense(1280, activation='sigmoid'),  
     #tf.keras.layers.Dropout(.2),
     #tf.keras.layers.Dense(1280, activation='sigmoid'),
     #tf.keras.layers.Dense(1280, activation='sigmoid'),
     #tf.keras.layers.Dropout(.1),
     tf.keras.layers.Dense(1280, activation='sigmoid'),
     tf.keras.layers.Dense(1280, activation='sigmoid'),
     #tf.keras.layers.Dense(1280, activation='sigmoid'),
     #tf.keras.layers.Dense(1280, activation='sigmoid'),
     #tf.keras.layers.Dense(1280, activation='sigmoid'),
     #tf.keras.layers.Dense(1280, activation='sigmoid'),
     tf.keras.layers.Dense(classes, activation='softmax')
    ])
    model.build([None, 224, 224, 3])
    #model.summary()

    model.compile(
     optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
     loss=tf.keras.losses.CategoricalCrossentropy(),
     metrics=['acc'])
            
def train(epochs = 0): 
    global MODEL 
    MODEL = os.path.join("Profile",self.Config.profile,"CNN_MODEL")
    
    global model
    global dict_class
    
    data_root = os.path.join("Profile",self.Config.profile,"images")
    
    #os.makedirs(os.path.join(data_root,"PASS"), exist_ok=True)
    #os.makedirs(os.path.join(data_root,"FAIL"), exist_ok=True)

    IMAGE_SHAPE = (224,224) 
    TRAINING_DATA_DIR = str(data_root)
    #datagen_kwargs = dict(rescale=1./255)#rescale=1./255, validation_split=.6)
    #dct_method='INTEGER_ACCURATE'
    # valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagen_kwargs)
    # valid_generator = valid_datagen.flow_from_directory(
        # TRAINING_DATA_DIR,
        # subset="validation",
        # shuffle=True,
        # target_size=IMAGE_SHAPE        
        # )

    datagen_kwargs = dict(rescale=1./255)#rescale=1./255)
    
    if self.Config.train_brightness == "Y":
        print("Train with brightness")
        datagen_kwargs.update(brightness_range=(0, 1))
        
    if self.Config.train_rotate == "Y":
        print("Train with rotation")
        datagen_kwargs.update(rotation_range=360)
    
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(**datagen_kwargs)
    train_generator = train_datagen.flow_from_directory(
        TRAINING_DATA_DIR,
        #subset="training",
        shuffle=True,
        target_size=IMAGE_SHAPE
        )

    # for image_batch, label_batch in train_generator:
      # break
    # image_batch.shape, label_batch.shape
    dict_class = train_generator.class_indices
    print (train_generator.class_indices) 
    #https://tfhub.dev/google/imagenet/mobilenet_v3_small_100_224/feature_vector/5
    #https://tfhub.dev/google/imagenet/mobilenet_v3_large_075_224/feature_vector/5
    #https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4
    
    if model is None:
        create_model(train_generator.num_classes)
    
    if epochs == 0:
        epochs = int(input("Epochs? : "))
    
    try:
        steps_per_epoch = np.ceil(train_generator.samples/train_generator.batch_size)
        #val_steps_per_epoch = np.ceil(valid_generator.samples/valid_generator.batch_size)
        hist = model.fit(
         train_generator,
         epochs=epochs,
         verbose=1,
         steps_per_epoch=steps_per_epoch).history
         # ,
         # validation_data=valid_generator,
         # validation_steps=val_steps_per_epoch
    except:
        create_model(train_generator.num_classes)
        steps_per_epoch = np.ceil(train_generator.samples/train_generator.batch_size)
        #val_steps_per_epoch = np.ceil(valid_generator.samples/valid_generator.batch_size)
        hist = model.fit(
         train_generator,
         epochs=epochs,
         verbose=1,
         steps_per_epoch=steps_per_epoch).history
         # validation_data=valid_generator,
         # validation_steps=val_steps_per_epoch
        
    # Save the weights
    try:
        model.save(MODEL)
        
        with open(os.path.join(MODEL,"name.json"), 'w') as f:
            f.write(json.dumps(train_generator.class_indices))
    except:
        traceback.print_exc()