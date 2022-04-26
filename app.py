from distutils.log import debug
from flask import Flask, render_template,Response
import cv2
import numpy as np
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'
camera = cv2.VideoCapture(0)
text=""

model = load_model('keras_model.h5')
gg = 'nice'
disease = ''
from flask_wtf import FlaskForm
from wtforms import FileField
from flask_uploads import configure_uploads, IMAGES, UploadSet
class MyForm(FlaskForm):
    image = FileField('image')


images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class MyForm(FlaskForm):
    image = FileField('image')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if(form.image.data):    
        print(form.image.data)
        disease = predict(form.image.data)
        descriptions = ''
        treatment = ''
        if(disease=='Apple Cedar Rust'):
            descriptions = 'Cedar Apple Rust is a disease caused by a plant pathogen called Gymnosporangium juniperi-virginianae. It can be a destructive or disfiguring disease on both apples and cedars. '
            treatment = 'Apply fungicides labeled for use on apples weekly. Dispose of fallen leaves and other debris from trees. Remove one of the host trees to break the cedar-quince rust disease cycle. Replace the removed tree with a rust-resistant tree variety. Follow good cultural practices to help control cedar-quince rust. Fungal spores can fall from the tree and remain on the ground until spread by rain or wind. Use a rake to keep the area around the infected tree free of debris. Always destroy pruned and collected plant tissue promptly.'
        if(disease=='Apple Rot'):
            descriptions = 'It is a foliar disease that is caused by the fungus Ventura inaequalis.'
            treatment = 'Remove and destroy the fallen leaf litter so that the fungus cannot overwinter. This may reduce the disease pressure in the following spring, but will not likely eliminate the disease. Regular use of fungicides is an effective method for controlling the disease. Prune your apple trees regularly to open up branching and allow air circulation. Clean all the leaf litter from the base of previously-infected trees.'
        if(disease=='Apple Scab'):
            descriptions = 'It is a disease caused by the apple-rotting fungi.'
            treatment = 'Prune out dead or diseased branches. Pick all dried and shriveled fruits remaining on the trees. Remove infected plant material from the area. All infected plant parts should be burned, buried or sent to a municipal composing site. Be sure to remove the stumps of any apple trees you cut down, because it can be a source of spores that can still spread to other plant leaves.'

        if(disease=='Cherry Powdery Mildrew'):
            descriptions = 'Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) cultivars are commonly affected, rendering them unmarketable due to the covering of white fungal growth on the cherry surface.'
            treatment = 'Manage irrigation. In the arid west in a typical dry spring, early irrigation may stimulate early cherry powdery mildew infections. Pruning. Humid conditions favor cherry powdery mildew. A well pruned canopy will promote more air flow and leaf drying, reducing these humid conditions favorable for disease. Pruning will also help to achieve good spray coverage. Root sucker management. Root suckers are a preferred by powdery mildews since they are comprised of highly susceptible leaf tissue. Root suckers are close to the irrigation and high humidity levels favor the onset and spread of infections. Additionally, sprays aimed at the canopy often do not protect root suckers allowing fungal inocula to survive all season. Remove root suckers to eliminate this source for infection of the canopy and fruit. The key to managing powdery mildew on the fruit is to keep the disease off of the leaves. Most synthetic fungicides are preventative, not eradicative, so be pro-active about disease prevention.'
        if(disease=='Corn Common Leaf Blight'):
            descriptions = 'Northern corn leaf blight (NCLB), caused by the fungus Exserohilum turcicum. During wet weather yield losses may be as high as 30-50% if the disease becomes establishes before tasseling. However, if leaf damage is only moderate or is delayed until 6 weeks after silking, yield losses are minimal. Severe damage caused by NCLB also predisposes plants to stalk rot and lodging, which may further reduce yield and grain quality.'
            treatment = 'Planting resistant hybrids is the most effective method for controlling NCLB. A one- to two-year rotation away from corn and destruction of old corn residues by tillage will be helpful for controlling NCLB. Fungicide sprays are recommended for fresh market sweet corn, hybrid seed production, and dent corn fields planted with susceptible hybrids.'
        
        if(disease=='Corn Common Rust'):
            descriptions = 'Common rust of sweet corn is caused by the fungus Puccinia sorghi and can result in serious losses in yield or quality of sweet corn.  Early symptoms of common rust are chlorotic flecks on the leaf surface.'
            treatment = 'The best management practice is to use resistant corn hybrids. To reduce the incidence of corn rust, plant only corn that has resistance to the fungus.Resistance is either in the form of race-specific resistance or partial rust resistance. If the corn begins to show symptoms of infection, immediately spray with a fungicide. The fungicide is most effective when started at the first sign of infection.'
        
        if(disease=='corn maize cercospora leaf spot gray leaf spot'):
            descriptions = 'It is a fungal disease that affects corn. There are two fungal pathogens that cause GLS: Cercospora zeae-maydis and Cercospora zeina.'
            treatment = 'Fungicides, if sprayed early in season before initial damage, can be effective in reducing disease. Avoid overwatering or watering in the late evening to reduce free moisture. Space plants to encourage air movement and reduce high humidity levels. Avoid overhead watering where the water can dislodge and disperse spores to uninfected plants.'
        if(disease=='Grape Black Rot'):
            descriptions = 'Black rot of grapes is a fungal disease that persists in grapevines for many years without treatment. The earliest signs of disease appear as yellow circular lesions on young leaves. As these lesions spread, they brown and sprout black fungal fruiting bodies that look similar to grains of pepper.'
            treatment = 'The best time to treat black rot of grapes is between bud break until about four weeks after bloom; treating outside of this window is likely to end in frustration. Prevention is key when dealing with grape black rot. During your fall clean-up, make sure that all mummies have been removed from the vine and all plant material on the ground below is destroyed. Captan and myclobutanil are the fungicides of choice.'
        
        if(disease=='Grape Esca'):
            descriptions = 'Grape Esca (black measles) "trunk diseases" caused by different wood-infecting fungi. The foliar symptom of Esca is an interveinal "striping". The "stripes", which start out as dark red in red cultivars and yellow in white cultivars, dry and become necrotic.'
            treatment = 'Presently, there are no effective management strategies for measles. Wine grape growers with small vineyards will often have field crews remove infected fruit prior to harvest. Raisins affected by measles will be discarded during harvest or at the packing house, while table grape growers will leave affected fruit on the vine.'
        if(disease=='Grape Leaf Blight'):
            descriptions = 'Grape Leaf blight, also called Isariopsis leaf spot (Pseudocercospora vitis) on Grape (Vitus sp.) Scattered, somewhat angular, purple-brown spots on upper leaf surface. Corresponding, less conspicuous, brown spots on lower leaf surface.'
            treatment = 'vines should be grown in full sun, in a well draining soil and in a location where there is good circulating air to reduce incidence of disease. Low lying areas should be avoided when selecting a planting site as this can lead to water accumulation during periods of wet weather Vines prefer a soil with a slightly acidic to neutral pH between 6.0 and 7.0 and require a trellis system to support the weight of the fruit on the vines.'
        
        if(disease=='Orange Haunglongbing'):
            descriptions = 'the most severe citrus disease, currently devastating the citrus industry worldwide.'
            treatment = 'avoid moving plants and plant materials from areas under regulatory quarantine or where the insect or disease is present. isolation and protection of budwood sources and plant propagation in screened-in, insect-proof locations. development of resistant cultivars. potential chemical control of the Liberibacters using chemical and antibiotic treatments of trees.'

        return render_template('treatment.html',value = {'disease':disease,'treatment':treatment,'descriptions':descriptions})
    if form.validate_on_submit():
        print("OKAYYYYYY")
        filename = images.save(form.image.data)
        print(filename)
        return f'Filename: { filename }'
   
    return render_template('index.html',form=form)

@app.route('/about')
def about():
    return render_template('about.html',value=gg)


@app.route('/tips')
def tips():
    return render_template('growing_tips.html',value=gg)

@app.route('/scanner')
def scanner():
    return render_template('scanner.html',value=gg)


@app.route('/treatment')
def treatment():
    print("OKAYYYY")
    descriptions = ''
    treatment = ''
    print(disease)
    if(disease=='Apple Cedar Rust'):
        descriptions = 'Cedar Apple Rust is a disease caused by a plant pathogen called Gymnosporangium juniperi-virginianae. It can be a destructive or disfiguring disease on both apples and cedars. '
        treatment = 'Apply fungicides labeled for use on apples weekly. Dispose of fallen leaves and other debris from trees. Remove one of the host trees to break the cedar-quince rust disease cycle. Replace the removed tree with a rust-resistant tree variety. Follow good cultural practices to help control cedar-quince rust. Fungal spores can fall from the tree and remain on the ground until spread by rain or wind. Use a rake to keep the area around the infected tree free of debris. Always destroy pruned and collected plant tissue promptly.'
    if(disease=='Apple Rot'):
        descriptions = 'It is a foliar disease that is caused by the fungus Ventura inaequalis.'
        treatment = 'Remove and destroy the fallen leaf litter so that the fungus cannot overwinter. This may reduce the disease pressure in the following spring, but will not likely eliminate the disease. Regular use of fungicides is an effective method for controlling the disease. Prune your apple trees regularly to open up branching and allow air circulation. Clean all the leaf litter from the base of previously-infected trees.'
    if(disease=='Apple Scab'):
        descriptions = 'It is a disease caused by the apple-rotting fungi.'
        treatment = 'Prune out dead or diseased branches. Pick all dried and shriveled fruits remaining on the trees. Remove infected plant material from the area. All infected plant parts should be burned, buried or sent to a municipal composing site. Be sure to remove the stumps of any apple trees you cut down, because it can be a source of spores that can still spread to other plant leaves.'

    if(disease=='Cherry Powdery Mildrew'):
        descriptions = 'Powdery mildew of sweet and sour cherry is caused by Podosphaera clandestina, an obligate biotrophic fungus. Mid- and late-season sweet cherry (Prunus avium) cultivars are commonly affected, rendering them unmarketable due to the covering of white fungal growth on the cherry surface.'
        treatment = 'Manage irrigation. In the arid west in a typical dry spring, early irrigation may stimulate early cherry powdery mildew infections. Pruning. Humid conditions favor cherry powdery mildew. A well pruned canopy will promote more air flow and leaf drying, reducing these humid conditions favorable for disease. Pruning will also help to achieve good spray coverage. Root sucker management. Root suckers are a preferred by powdery mildews since they are comprised of highly susceptible leaf tissue. Root suckers are close to the irrigation and high humidity levels favor the onset and spread of infections. Additionally, sprays aimed at the canopy often do not protect root suckers allowing fungal inocula to survive all season. Remove root suckers to eliminate this source for infection of the canopy and fruit. The key to managing powdery mildew on the fruit is to keep the disease off of the leaves. Most synthetic fungicides are preventative, not eradicative, so be pro-active about disease prevention.'
    if(disease=='Corn Common Leaf Blight'):
        descriptions = 'Northern corn leaf blight (NCLB), caused by the fungus Exserohilum turcicum. During wet weather yield losses may be as high as 30-50% if the disease becomes establishes before tasseling. However, if leaf damage is only moderate or is delayed until 6 weeks after silking, yield losses are minimal. Severe damage caused by NCLB also predisposes plants to stalk rot and lodging, which may further reduce yield and grain quality.'
        treatment = 'Planting resistant hybrids is the most effective method for controlling NCLB. A one- to two-year rotation away from corn and destruction of old corn residues by tillage will be helpful for controlling NCLB. Fungicide sprays are recommended for fresh market sweet corn, hybrid seed production, and dent corn fields planted with susceptible hybrids.'
    
    if(disease=='Corn Common Rust'):
        descriptions = 'Common rust of sweet corn is caused by the fungus Puccinia sorghi and can result in serious losses in yield or quality of sweet corn.  Early symptoms of common rust are chlorotic flecks on the leaf surface.'
        treatment = 'The best management practice is to use resistant corn hybrids. To reduce the incidence of corn rust, plant only corn that has resistance to the fungus.Resistance is either in the form of race-specific resistance or partial rust resistance. If the corn begins to show symptoms of infection, immediately spray with a fungicide. The fungicide is most effective when started at the first sign of infection.'
    
    if(disease=='corn maize cercospora leaf spot gray leaf spot'):
        descriptions = 'It is a fungal disease that affects corn. There are two fungal pathogens that cause GLS: Cercospora zeae-maydis and Cercospora zeina.'
        treatment = 'Fungicides, if sprayed early in season before initial damage, can be effective in reducing disease. Avoid overwatering or watering in the late evening to reduce free moisture. Space plants to encourage air movement and reduce high humidity levels. Avoid overhead watering where the water can dislodge and disperse spores to uninfected plants.'
    if(disease=='Grape Black Rot'):
        descriptions = 'Black rot of grapes is a fungal disease that persists in grapevines for many years without treatment. The earliest signs of disease appear as yellow circular lesions on young leaves. As these lesions spread, they brown and sprout black fungal fruiting bodies that look similar to grains of pepper.'
        treatment = 'The best time to treat black rot of grapes is between bud break until about four weeks after bloom; treating outside of this window is likely to end in frustration. Prevention is key when dealing with grape black rot. During your fall clean-up, make sure that all mummies have been removed from the vine and all plant material on the ground below is destroyed. Captan and myclobutanil are the fungicides of choice.'
    
    if(disease=='Grape Esca'):
        descriptions = 'Grape Esca (black measles) "trunk diseases" caused by different wood-infecting fungi. The foliar symptom of Esca is an interveinal "striping". The "stripes", which start out as dark red in red cultivars and yellow in white cultivars, dry and become necrotic.'
        treatment = 'Presently, there are no effective management strategies for measles. Wine grape growers with small vineyards will often have field crews remove infected fruit prior to harvest. Raisins affected by measles will be discarded during harvest or at the packing house, while table grape growers will leave affected fruit on the vine.'
    if(disease=='Grape Leaf Blight'):
        descriptions = 'Grape Leaf blight, also called Isariopsis leaf spot (Pseudocercospora vitis) on Grape (Vitus sp.) Scattered, somewhat angular, purple-brown spots on upper leaf surface. Corresponding, less conspicuous, brown spots on lower leaf surface.'
        treatment = 'vines should be grown in full sun, in a well draining soil and in a location where there is good circulating air to reduce incidence of disease. Low lying areas should be avoided when selecting a planting site as this can lead to water accumulation during periods of wet weather Vines prefer a soil with a slightly acidic to neutral pH between 6.0 and 7.0 and require a trellis system to support the weight of the fruit on the vines.'
    
    if(disease=='Orange Haunglongbing'):
        descriptions = 'the most severe citrus disease, currently devastating the citrus industry worldwide.'
        treatment = 'avoid moving plants and plant materials from areas under regulatory quarantine or where the insect or disease is present. isolation and protection of budwood sources and plant propagation in screened-in, insect-proof locations. development of resistant cultivars. potential chemical control of the Liberibacters using chemical and antibiotic treatments of trees.'

    return render_template('treatment.html',value = {'disease':disease,'treatment':treatment,'descriptions':descriptions})

@app.route('/treat')
def index_2():
    return render_template('index.html',value=gg)


@app.route('/upload')
def index_3():
    print("okay")
    return ""


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
            # print(prediction)
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
                if i[11] >0.7:
                    text = "Apple Healthy"
                if i[12] >0.7:
                    text = "Corn Healthy"
                if i[13] >0.7:
                    text = "Grape Healthy"
                if i[14] >0.7:
                    text = "Peach Healthy"
                if i[15] >0.7:
                    text = "Pepper Bell Healthy"
                if i[16] >0.7:
                    text = "Potato Healthy"
                if i[17] >0.7:
                    text = "Strawberry Healthy"
                if i[18] >0.7:
                    text = "Tomato Healthy"
                
                cv2.putText(image,text,(0,20),cv2.FONT_ITALIC,1,(0,255,0),2)
            globals()['disease']=text
            print(globals()['disease'])
            ret, jpeg = cv2.imencode('.jpg', image)
            yield jpeg.tobytes()


def predict(img):
    file = img
    npimg = np.fromfile(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    text=''
    np.set_printoptions(suppress=False)
    model = load_model('keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # img = cv2.imread('ampalaya.jpg')
    img = cv2.resize(img,(224,224))
    image_array = np.asarray(img)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)

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
        if i[11] >0.7:
            text = "Apple Healthy"
        if i[12] >0.7:
            text = "Corn Healthy"
        if i[13] >0.7:
            text = "Grape Healthy"
        if i[14] >0.7:
            text = "Peach Healthy"
        if i[15] >0.7:
            text = "Pepper Bell Healthy"
        if i[16] >0.7:
            text = "Potato Healthy"
        if i[17] >0.7:
            text = "Strawberry Healthy"
        if i[18] >0.7:
            text = "Tomato Healthy"
    print(prediction)
    print(text)
    return text
app.run(debug=True)
