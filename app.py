from distutils.log import debug
from flask import Flask, render_template,Response
import cv2
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
app = Flask(__name__)
camera = cv2.VideoCapture(0)
text=""
model = load_model('keras_model.h5')
gg = 'nice'

@app.route('/')
def index():
    return render_template('index.html',value=gg)


@app.route('/treat')
def index_2():
    return render_template('index.html',value=gg)
    
def gen():
    # while True:
    #     success, frame = camera.read()  # read the camera frame
    #     if not success:
    #         break
    #     else:
    #         for frame in camera.get_frame():
    #             yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
    #             yield frame
    #             yield b'\r\n\r\n'
    camera = VideoCamera()
    for frame in camera.get_frame():
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
        yield frame
        yield b'\r\n\r\n'


@app.route('/video')

def video():
    return Response(gen(),mimetype='multipart/x-mixed-replace;boundary=frame')

class VideoCamera():
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def get_frame(self):     
        globals()['gg']='okay'
        print(globals())
        text=""
        while(True):
            # index('okay')
            ret, image = self.video.read()
            #that face is the list, which has all the detected faces in the frame, using dlib library
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            size = (224, 224)
            image = cv2.resize(image,(224,224))
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            prediction = model.predict(data)
            print(prediction)
            #print(prediction)
            for i in prediction:
                if i[0] >0.7:
                    text="Apple Cedar Rust"
                    
                if i[1] >0.7:
                    text = "Apple Rot"
                    
                if i[2] >0.7:
                    text = "Apple Scab"
                    
                if i[3] >0.7:
                    text = "Cherry Powdery Mildrew"
                    
                if i[4] >0.7:
                    text = "Corn Common Leaf Blight"
                    
                if i[5] >0.7:
                    text = "Corn Common Rust"
                    
                if i[6] >0.7:
                    text = "corn maize cercospora leaf spot gray leaf spot"
                    
                if i[7] >0.7:
                    text = "Grape Black Rot"
                    
                if i[8] >0.7:
                    text = "Grape Esca"
                    
                if i[9] >0.7:
                    text = "Grape Leaf Blight"
                    
                if i[10] >0.7:
                    text = "Orange Haunglongbing"
                    
                cv2.putText(image,text,(0,20),cv2.FONT_ITALIC,1,(0,255,0),2)
            ret, jpeg = cv2.imencode('.jpg', image)
            yield jpeg.tobytes()
app.run(debug=True)
