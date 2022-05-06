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
        if(disease=='Apple Healthy'):
            descriptions = 'An apple is an edible fruit produced by an apple tree (Malus domestica). Apple trees are cultivatedworldwide and are the most widely grown species in the genus Malus. The tree originated in Central Asia, where its wild ancestor, Malus sieversii, is still found today. Apples have been grown for thousands of years in Asia and Europe and were. brought to North America by European colonists. Apples have religious and mythological significance inmany cultures, including Norse, Greek, and European Christian tradition.'
            treatment = 'This plant is health.'
        if(disease=='Corn Healthy'):
            descriptions = 'Maize (/meɪz/ MAYZ; Zea mays subsp. mays, from Spanish: maíz after Taino: mahiz), also known as corn (North American and Australian English), is a cereal grain first domesticated by indigenous peoples in southern Mexico about 10,000 years ago.'
            treatment = 'This plant is health.'
        if(disease=='Grape Healthy'):
            descriptions = 'A grape is a fruit, botanically a berry, of the deciduous woody vines of the flowering plant genus Vitis. Grapes can be eaten fresh as table grapes, used for making wine, jam, grape juice, jelly, grape seed extract, vinegar, and grape seed oil, or dried as raisins, currants and sultanas. Grapes are a non-climacteric type of fruit, generally occurring in clusters.'
            treatment = 'This plant is health.'
        if(disease=='Peach Healthy'):
            descriptions = 'The peach (Prunus persica) is a deciduous tree first domesticated and cultivated in Zhejiang province of Eastern China.[3] It bears edible juicy fruits with various characteristics, most called peaches and others (the glossy-skinned, non-fuzzy varieties), nectarines.The specific name persica refers to its widespread cultivation in Persia (modern-day Iran), from where it was transplanted to Europe. It belongs to the genus Prunus, which includes the cherry, apricot, almond, and plum, in the rose family. The peach is classified with the almond in the subgenus Amygdalus, distinguished from the other subgenera by the corrugated seed shell (endocarp).'
            treatment = 'This plant is health.'

        if(disease=='Pepper Bell Healthy'):
            descriptions = 'The bell pepper (also known as sweet pepper, pepper, or capsicum /ˈkæpsɪkəm/) is the fruit of plants in the Grossum cultivar group of the species Capsicum annuum. Cultivars of the plant produce fruits in different colors, including red, yellow, orange, green, white, and purple. Bell peppers are sometimes grouped with less pungent chili varieties as "sweet peppers". While they are fruits—botanically classified as berries—they are commonly used as a vegetable ingredient or side dish. The fruits of the Capsicum genus are categorized as chili peppers.'
            treatment = 'This plant is health.'
        
        if(disease=='Potato Healthy'):
            descriptions = 'The potato is a starchy tuber of the plant Solanum tuberosum and is a root vegetable native to the Americas. The plant is a perennial in the nightshade family Solanaceae. Wild potato species can be found from the southern United States to southern Chile. The potato was originally believed to have been domesticated by Native Americans independently in multiple locations, but later genetic studies traced a single origin, in the area of present-day southern Peru and extreme northwestern Bolivia. Potatoes were domesticated there approximately 7,000–10,000 years ago, from a species in the Solanum brevicaule complex. In the Andes region of South America, where the species is indigenous, some close relatives of the potato are cultivated.'
            treatment = 'This plant is health.'
        
        if(disease=='Strawberry Healthy'):
            descriptions = 'The garden strawberry (or simply strawberry; Fragaria × ananassa)[1] is a widely grown hybrid species of the genus Fragaria, collectively known as the strawberries, which are cultivated worldwide for their fruit. The fruit is widely appreciated for its characteristic aroma, bright red color, juicy texture, and sweetness. It is consumed in large quantities, either fresh or in such prepared foods as jam, juice, pies, ice cream, milkshakes, and chocolates. Artificial strawberry flavorings and aromas are also widely used in products such as candy, soap, lip gloss, perfume, and many others.'
            treatment = 'This plant is health.'
        
        if(disease=='Tomato Healthy'):
            descriptions = 'The tomato is the edible berry of the plant Solanum lycopersicum, commonly known as the tomato plant. The species originated in western South America and Central America.The Mexican Nahuatl word tomatl gave rise to the Spanish word tomate, from which the English word tomato derived. Its domestication and use as a cultivated food may have originated with the indigenous peoples of Mexico.'
            treatment = 'This plant is health.'
        
        if(disease=='Peach Bacterial Spot'):
            descriptions = 'Bacterial spot is an important disease of peaches, nectarines, apricots, and plums caused by Xanthomonas campestris pv. pruni. Symptoms of this disease include fruit spots, leaf spots, and twig cankers.'
            treatment = 'Apply fungicides every 10 to 14 days. You can  adjust the timing slightly depending on weather conditions and the level of disease presence. Use recommended fungicides. These include captan, chlorothalonil, and sulfur. Monitor twigs for peach scab lesions early in the season to anticipate and plan fungicide applications. Improve air circulation in the orchard by choosing planting sites with good drainage, providing adequate spacing between trees when planting and pruning. Begin applications at petal fall and continue until around 6 weeks before the fruit matures.'
        
        if(disease=='Pepper Bell Bacterial Spot'):
            descriptions = 'caused by Xanthomonas campestris pv. vesicatoria, is the most common and destructive disease for peppers in the eastern United States.'
            treatment = 'Washing seeds for 40 minutes in diluted Clorox (two parts Clorox plus eight parts water) is effective in reducing the bacterial population on a seed’s surface. Seed treatment with hot water, soaking seeds for 30 minutes in water pre-heated to 125 F/51 C, is effective in reducing bacterial populations on the surface and inside the seeds. Control of bacterial spot on greenhouse transplants is an essential step for preventing the spread of the leaf spot bacteria in the field. Transplants should be inspected regularly to identify symptomatic seedlings'

        if(disease=='Potato Early Blight'):
            descriptions = 'Early blight of potato is caused by the fungal pathogen Alternaria solani. The disease affects leaves, stems and tubers and can reduce yield, tuber size, storability of tubers, quality of fresh-market and processing tubers and marketability of the crop.'
            treatment = 'Select a late-season variety with a lower susceptibility to early blight. (Resistance is associated with plant maturity and early maturing cultivars are more susceptible). Time irrigation to minimize leaf wetness duration during cloudy weather and allow sufficient time for leaves to dry prior to nightfall. Avoid nitrogen and phosphorus deficiency. Scout fields regularly for infection beginning after plants reach 12 inches in height. Pay particular attention to edges of fields that are adjacent to fields planted to potato the previous year'
        
        if(disease=='Potato Late Blight'):
            descriptions = 'Late blight is caused by the funguslike oomycete pathogen Phytophthora infestans. This potentially devastating disease can infect potato foliage and tubers at any stage of crop development.'
            treatment = 'Destroy all cull and volunteer potatoes. Plant late blight-free seed tubers. Do not mix seed lots because cutting can transmit late blight. Avoid planting problem areas that may remain wet for extended periods or may be difficult to spray (the center of the pivot, along powerlines and tree lines). Avoid excessive and/or nighttime irrigation.'
        
        if(disease=='Squash Powdery Mildew'):
            descriptions = 'Powdery mildew is most commonly seen on the top of the leaves, but it can also appear on the leaf undersides, the stems, and even on the fruits.'
            treatment = 'A 2-year rotation out of cucurbits is helpful in case chasmothecia were produced on a previous cucurbit crop. Avoid establishment of plants where shaded by tall plants or structures. Avoid planting too dense of stands'
        
        if(disease=='Strawberry Leaf Scorch'):
            descriptions = 'Scorched strawberry leaves are caused by a fungal infection which affects the foliage of strawberry plantings. The fungus responsible is called Diplocarpon earliana.'
            treatment = 'removal of infected garden debris from the strawberry patch creation of new plantings and strawberry patches is key to maintaining a consistent strawberry harvest avoidance of waterlogged soil and frequent garden cleanup will help to reduce the likelihood of spread of this fungus.'
        
        if(disease=='Tomato Bacterial Spot'):
            descriptions = 'Bacterial spot of tomato is caused by Xanthomonas vesicatoria, Xanthomonas euvesicatoria, Xanthomonas gardneri, and Xanthomonas perforans. These bacterial pathogens can be introduced into a garden on contaminated seed and transplants, which may or may not show symptoms.'
            treatment = 'remove the affected leaves at the first sign to prevent the bacteria from jumping onto adjacent leaves.  Remove old vegetable debris in the garden and do not plant new crops where host plants were once growing.'

        if(disease=='Tomato Early Blight'):
            print("okayyy")
            descriptions = 'Blight on tomatoes is caused by a fungal infection and like all fungi, they are spread by spores and require damp, warm weather conditions to flourish which affects leaves, fruits and stems and can be severely yield-limiting when susceptible tomato cultivars are used and weather is favorable. Severe defoliation can occur.  In tomatoes, fruit can be damaged by sun.'
            treatment = 'Cover the soil under the plants with mulch, such as fabric, straw, plastic mulch, or dried leaves. Water at the base of each plant, using drip irrigation, a soaker hose, or careful hand watering. Most home gardeners don’t need to treat tomatoes with a fungicide. Tomato plants can tolerate a lot of early blight without reducing the number of tomatoes they produce. Keep leaves dry to reduce spreading the disease.'

        if(disease=='Tomato Late Blight'):
            descriptions = 'Late blight tomato disease is the rarest of the blights that affect both tomatoes and potatoes, but it is also the most destructive. Tomato Late Blight is a fungus-like organism that can destroy a crop within days if conditions are right. Vigilant observation and pre-treatment are the only defenses against late tomato blight.'
            treatment = 'Sanitation is the first step in controlling tomato late blight. Clean up all debris and fallen fruit from the garden area. There are no strains of tomato available that are resistant to late tomato blight, so plants should be inspected at least twice a week. Since late blight symptoms are more likely to occur during wet conditions, more care should be taken during those times.'

        if(disease=='Tomato Leaf Mold'):
            descriptions = 'Tomato leaf mold is a fungal disease that can develop when there are extended periods of leaf wetness and the relative humidity is high (greater than 85 percent). Due to this moisture requirement, the disease is seen primarily in hoophouses and greenhouses.'
            treatment = 'Sanitize the greenhouse between crop seasons.  If growing tomatoes in a greenhouse, maintain night temps higher than outside temperatures. When planting, use only certified disease-free seed or treated seed. Remove and destroy all crop debris post-harvest.'
        if(disease=='Tomato Mosaic Virus'):
            descriptions = 'Tomato mosaic virus is one of the oldest described plant viruses. It is extremely easily spread and can be devastating to crops. They are often seen as a general mottling or mosaic appearance on foliage'
            treatment = 'Sanitize the greenhouse between crop seasons.  If growing tomatoes in a greenhouse, maintain night temps higher than outside temperatures. When planting, use only certified disease-free seed or treated seed. Remove and destroy all crop debris post-harvest.'
        
        if(disease=='Tomato Leaf Mold'):
            descriptions = 'Tomato leaf mold is a fungal disease that can develop when there are extended periods of leaf wetness and the relative humidity is high (greater than 85 percent). Due to this moisture requirement, the disease is seen primarily in hoophouses and greenhouses.'
            treatment = 'Remove all infected plants and destroy them. Do NOT put them in the compost pile, as the virus may persist in infected plant matter. Burn infected plants or throw them out with the garbage. Monitor the rest of your plants closely, especially those that were located near infected plants. Disinfect gardening tools after every use. Keep a bottle of a weak bleach solution or other antiviral disinfectant to wipe your tools down with.'
        
        if(disease=='Tomato Septoria Leaf Spot'):
            descriptions = 'Septoria leaf spot is caused by a fungus, Septoria lycopersici.'
            treatment = 'It is okay to remove up to a third of the plants leaves if you catch the disease early.'
        
        if(disease=='Tomato Spider mites'):
            descriptions = 'They cannot be seen easily with the naked eye. Feeding damage caused by sucking sap appears as many shiny pale yellow marks on the top of the tomato leaf.'
            treatment = 'Remove leaves that are heavily infested. Clean the plant.  Use mixture of alcohol and water to remove and kill visible spider mites. '
        
        if(disease=='Tomato Target Spot'):
            descriptions = 'Also known as early blight, target spot of tomato is a fungal disease that attacks a diverse assortment of plants, including papaya, peppers, snap beans, potatoes, cantaloupe, and squash as well as passion flower and certain ornamentals.'
            treatment = 'Remove old plant debris at the end of the growing season; otherwise, the spores will travel from debris to newly planted tomatoes in the following growing season, thus beginning the disease anew. Dispose of the debris properly and don’t place it on your compost pile unless you’re sure your compost gets hot enough to kill the spores.'
        
        if(disease=='Tomato Yellow Leaf Curl Virus'):
            descriptions = 'Infected tomato plants initially show stunted and erect or upright plant growth; plants infected at an early stage of growth will show severe stunting. However, the most diagnostic symptoms are those in leaves.'
            treatment = 'Fields should be inspected daily for the presence of whiteflies. A trap can be made with a piece of board 12 inches x 12 inches painted bright yellow. Spread petroleum jelly or Biotac on it. The yellow colour attracts the whiteflies to the boards and they stick to them. The boards are placed at the height of the plants. Monitor all crops, not just tomato plants as the whitefly may have passed the virus onto another crop.'
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
    if(disease=='Apple Healthy'):
        descriptions = 'An apple is an edible fruit produced by an apple tree (Malus domestica). Apple trees are cultivatedworldwide and are the most widely grown species in the genus Malus. The tree originated in Central Asia, where its wild ancestor, Malus sieversii, is still found today. Apples have been grown for thousands of years in Asia and Europe and were. brought to North America by European colonists. Apples have religious and mythological significance inmany cultures, including Norse, Greek, and European Christian tradition.'
        treatment = 'This plant is health.'
    if(disease=='Corn Healthy'):
        descriptions = 'Maize (/meɪz/ MAYZ; Zea mays subsp. mays, from Spanish: maíz after Taino: mahiz), also known as corn (North American and Australian English), is a cereal grain first domesticated by indigenous peoples in southern Mexico about 10,000 years ago.'
        treatment = 'This plant is health.'
    if(disease=='Grape Healthy'):
        descriptions = 'A grape is a fruit, botanically a berry, of the deciduous woody vines of the flowering plant genus Vitis. Grapes can be eaten fresh as table grapes, used for making wine, jam, grape juice, jelly, grape seed extract, vinegar, and grape seed oil, or dried as raisins, currants and sultanas. Grapes are a non-climacteric type of fruit, generally occurring in clusters.'
        treatment = 'This plant is health.'
    if(disease=='Peach Healthy'):
        descriptions = 'The peach (Prunus persica) is a deciduous tree first domesticated and cultivated in Zhejiang province of Eastern China.[3] It bears edible juicy fruits with various characteristics, most called peaches and others (the glossy-skinned, non-fuzzy varieties), nectarines.The specific name persica refers to its widespread cultivation in Persia (modern-day Iran), from where it was transplanted to Europe. It belongs to the genus Prunus, which includes the cherry, apricot, almond, and plum, in the rose family. The peach is classified with the almond in the subgenus Amygdalus, distinguished from the other subgenera by the corrugated seed shell (endocarp).'
        treatment = 'This plant is health.'

    if(disease=='Pepper Bell Healthy'):
        descriptions = 'The bell pepper (also known as sweet pepper, pepper, or capsicum /ˈkæpsɪkəm/) is the fruit of plants in the Grossum cultivar group of the species Capsicum annuum. Cultivars of the plant produce fruits in different colors, including red, yellow, orange, green, white, and purple. Bell peppers are sometimes grouped with less pungent chili varieties as "sweet peppers". While they are fruits—botanically classified as berries—they are commonly used as a vegetable ingredient or side dish. The fruits of the Capsicum genus are categorized as chili peppers.'
        treatment = 'This plant is health.'
    
    if(disease=='Potato Healthy'):
        descriptions = 'The potato is a starchy tuber of the plant Solanum tuberosum and is a root vegetable native to the Americas. The plant is a perennial in the nightshade family Solanaceae. Wild potato species can be found from the southern United States to southern Chile. The potato was originally believed to have been domesticated by Native Americans independently in multiple locations, but later genetic studies traced a single origin, in the area of present-day southern Peru and extreme northwestern Bolivia. Potatoes were domesticated there approximately 7,000–10,000 years ago, from a species in the Solanum brevicaule complex. In the Andes region of South America, where the species is indigenous, some close relatives of the potato are cultivated.'
        treatment = 'This plant is health.'
    
    if(disease=='Strawberry Healthy'):
        descriptions = 'The garden strawberry (or simply strawberry; Fragaria × ananassa)[1] is a widely grown hybrid species of the genus Fragaria, collectively known as the strawberries, which are cultivated worldwide for their fruit. The fruit is widely appreciated for its characteristic aroma, bright red color, juicy texture, and sweetness. It is consumed in large quantities, either fresh or in such prepared foods as jam, juice, pies, ice cream, milkshakes, and chocolates. Artificial strawberry flavorings and aromas are also widely used in products such as candy, soap, lip gloss, perfume, and many others.'
        treatment = 'This plant is health.'
    
    if(disease=='Tomato Healthy'):
        descriptions = 'The tomato is the edible berry of the plant Solanum lycopersicum, commonly known as the tomato plant. The species originated in western South America and Central America.The Mexican Nahuatl word tomatl gave rise to the Spanish word tomate, from which the English word tomato derived. Its domestication and use as a cultivated food may have originated with the indigenous peoples of Mexico.'
        treatment = 'This plant is health.'
    
    if(disease=='Peach Bacterial Spot'):
        descriptions = 'Bacterial spot is an important disease of peaches, nectarines, apricots, and plums caused by Xanthomonas campestris pv. pruni. Symptoms of this disease include fruit spots, leaf spots, and twig cankers.'
        treatment = 'Apply fungicides every 10 to 14 days. You can  adjust the timing slightly depending on weather conditions and the level of disease presence. Use recommended fungicides. These include captan, chlorothalonil, and sulfur. Monitor twigs for peach scab lesions early in the season to anticipate and plan fungicide applications. Improve air circulation in the orchard by choosing planting sites with good drainage, providing adequate spacing between trees when planting and pruning. Begin applications at petal fall and continue until around 6 weeks before the fruit matures.'
    
    if(disease=='Pepper Bell Bacterial Spot'):
        descriptions = 'caused by Xanthomonas campestris pv. vesicatoria, is the most common and destructive disease for peppers in the eastern United States.'
        treatment = 'Washing seeds for 40 minutes in diluted Clorox (two parts Clorox plus eight parts water) is effective in reducing the bacterial population on a seed’s surface. Seed treatment with hot water, soaking seeds for 30 minutes in water pre-heated to 125 F/51 C, is effective in reducing bacterial populations on the surface and inside the seeds. Control of bacterial spot on greenhouse transplants is an essential step for preventing the spread of the leaf spot bacteria in the field. Transplants should be inspected regularly to identify symptomatic seedlings'

    if(disease=='Potato Early Blight'):
        descriptions = 'Early blight of potato is caused by the fungal pathogen Alternaria solani. The disease affects leaves, stems and tubers and can reduce yield, tuber size, storability of tubers, quality of fresh-market and processing tubers and marketability of the crop.'
        treatment = 'Select a late-season variety with a lower susceptibility to early blight. (Resistance is associated with plant maturity and early maturing cultivars are more susceptible). Time irrigation to minimize leaf wetness duration during cloudy weather and allow sufficient time for leaves to dry prior to nightfall. Avoid nitrogen and phosphorus deficiency. Scout fields regularly for infection beginning after plants reach 12 inches in height. Pay particular attention to edges of fields that are adjacent to fields planted to potato the previous year'
    
    if(disease=='Potato Late Blight'):
        descriptions = 'Late blight is caused by the funguslike oomycete pathogen Phytophthora infestans. This potentially devastating disease can infect potato foliage and tubers at any stage of crop development.'
        treatment = 'Destroy all cull and volunteer potatoes. Plant late blight-free seed tubers. Do not mix seed lots because cutting can transmit late blight. Avoid planting problem areas that may remain wet for extended periods or may be difficult to spray (the center of the pivot, along powerlines and tree lines). Avoid excessive and/or nighttime irrigation.'
    
    if(disease=='Squash Powdery Mildew'):
        descriptions = 'Powdery mildew is most commonly seen on the top of the leaves, but it can also appear on the leaf undersides, the stems, and even on the fruits.'
        treatment = 'A 2-year rotation out of cucurbits is helpful in case chasmothecia were produced on a previous cucurbit crop. Avoid establishment of plants where shaded by tall plants or structures. Avoid planting too dense of stands'
    
    if(disease=='Strawberry Leaf Scorch'):
        descriptions = 'Scorched strawberry leaves are caused by a fungal infection which affects the foliage of strawberry plantings. The fungus responsible is called Diplocarpon earliana.'
        treatment = 'removal of infected garden debris from the strawberry patch creation of new plantings and strawberry patches is key to maintaining a consistent strawberry harvest avoidance of waterlogged soil and frequent garden cleanup will help to reduce the likelihood of spread of this fungus.'
    
    if(disease=='Tomato Bacterial Spot'):
        descriptions = 'Bacterial spot of tomato is caused by Xanthomonas vesicatoria, Xanthomonas euvesicatoria, Xanthomonas gardneri, and Xanthomonas perforans. These bacterial pathogens can be introduced into a garden on contaminated seed and transplants, which may or may not show symptoms.'
        treatment = 'remove the affected leaves at the first sign to prevent the bacteria from jumping onto adjacent leaves.  Remove old vegetable debris in the garden and do not plant new crops where host plants were once growing.'

    if(disease=='Tomato Early Blight'):
        print("okayyy")
        descriptions = 'Blight on tomatoes is caused by a fungal infection and like all fungi, they are spread by spores and require damp, warm weather conditions to flourish which affects leaves, fruits and stems and can be severely yield-limiting when susceptible tomato cultivars are used and weather is favorable. Severe defoliation can occur.  In tomatoes, fruit can be damaged by sun.'
        treatment = 'Cover the soil under the plants with mulch, such as fabric, straw, plastic mulch, or dried leaves. Water at the base of each plant, using drip irrigation, a soaker hose, or careful hand watering. Most home gardeners don’t need to treat tomatoes with a fungicide. Tomato plants can tolerate a lot of early blight without reducing the number of tomatoes they produce. Keep leaves dry to reduce spreading the disease.'

    if(disease=='Tomato Late Blight'):
        descriptions = 'Late blight tomato disease is the rarest of the blights that affect both tomatoes and potatoes, but it is also the most destructive. Tomato Late Blight is a fungus-like organism that can destroy a crop within days if conditions are right. Vigilant observation and pre-treatment are the only defenses against late tomato blight.'
        treatment = 'Sanitation is the first step in controlling tomato late blight. Clean up all debris and fallen fruit from the garden area. There are no strains of tomato available that are resistant to late tomato blight, so plants should be inspected at least twice a week. Since late blight symptoms are more likely to occur during wet conditions, more care should be taken during those times.'

    if(disease=='Tomato Leaf Mold'):
        descriptions = 'Tomato leaf mold is a fungal disease that can develop when there are extended periods of leaf wetness and the relative humidity is high (greater than 85 percent). Due to this moisture requirement, the disease is seen primarily in hoophouses and greenhouses.'
        treatment = 'Sanitize the greenhouse between crop seasons.  If growing tomatoes in a greenhouse, maintain night temps higher than outside temperatures. When planting, use only certified disease-free seed or treated seed. Remove and destroy all crop debris post-harvest.'
    if(disease=='Tomato Mosaic Virus'):
        descriptions = 'Tomato mosaic virus is one of the oldest described plant viruses. It is extremely easily spread and can be devastating to crops. They are often seen as a general mottling or mosaic appearance on foliage'
        treatment = 'Sanitize the greenhouse between crop seasons.  If growing tomatoes in a greenhouse, maintain night temps higher than outside temperatures. When planting, use only certified disease-free seed or treated seed. Remove and destroy all crop debris post-harvest.'
    
    if(disease=='Tomato Leaf Mold'):
        descriptions = 'Tomato leaf mold is a fungal disease that can develop when there are extended periods of leaf wetness and the relative humidity is high (greater than 85 percent). Due to this moisture requirement, the disease is seen primarily in hoophouses and greenhouses.'
        treatment = 'Remove all infected plants and destroy them. Do NOT put them in the compost pile, as the virus may persist in infected plant matter. Burn infected plants or throw them out with the garbage. Monitor the rest of your plants closely, especially those that were located near infected plants. Disinfect gardening tools after every use. Keep a bottle of a weak bleach solution or other antiviral disinfectant to wipe your tools down with.'
    
    if(disease=='Tomato Septoria Leaf Spot'):
        descriptions = 'Septoria leaf spot is caused by a fungus, Septoria lycopersici.'
        treatment = 'It is okay to remove up to a third of the plants leaves if you catch the disease early.'
    
    if(disease=='Tomato Spider mites'):
        descriptions = 'They cannot be seen easily with the naked eye. Feeding damage caused by sucking sap appears as many shiny pale yellow marks on the top of the tomato leaf.'
        treatment = 'Remove leaves that are heavily infested. Clean the plant.  Use mixture of alcohol and water to remove and kill visible spider mites. '
    
    if(disease=='Tomato Target Spot'):
        descriptions = 'Also known as early blight, target spot of tomato is a fungal disease that attacks a diverse assortment of plants, including papaya, peppers, snap beans, potatoes, cantaloupe, and squash as well as passion flower and certain ornamentals.'
        treatment = 'Remove old plant debris at the end of the growing season; otherwise, the spores will travel from debris to newly planted tomatoes in the following growing season, thus beginning the disease anew. Dispose of the debris properly and don’t place it on your compost pile unless you’re sure your compost gets hot enough to kill the spores.'
    
    if(disease=='Tomato Yellow Leaf Curl Virus'):
        descriptions = 'Infected tomato plants initially show stunted and erect or upright plant growth; plants infected at an early stage of growth will show severe stunting. However, the most diagnostic symptoms are those in leaves.'
        treatment = 'Fields should be inspected daily for the presence of whiteflies. A trap can be made with a piece of board 12 inches x 12 inches painted bright yellow. Spread petroleum jelly or Biotac on it. The yellow colour attracts the whiteflies to the boards and they stick to them. The boards are placed at the height of the plants. Monitor all crops, not just tomato plants as the whitefly may have passed the virus onto another crop.'
      

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
                if i[19] >0.7:
                    text = "Peach Bacterial Spot"
                
                if i[20] >0.7:
                    text = "Pepper Bell Bacterial Spot"
                if i[21] >0.7:
                    text = "Potato Early Blight"
                if i[22] >0.7:
                    text = "Potato Late Blight"
                if i[23] >0.7:
                    text = "Squash Powdery Mildew"
                if i[24] >0.7:
                    text = "Strawberry Leaf Scorch"
                if i[25] >0.7:
                    text = "Tomato Bacterial Spot"
                if i[26] >0.7:
                    text = "Tomato Early Blight"
                if i[27] >0.7:
                    text = "Tomato Late Blight"
                if i[28] >0.7:
                    text = "Tomato Leaf Mold"
                if i[29] >0.7:
                    text = "Tomato Mosaic Virus"
                if i[30] >0.7:
                    text = "Tomato Septoria Leaf Spot"
                if i[31] >0.7:
                    text = "Tomato Spider mites"
                if i[32] >0.7:
                    text = "Tomato Target Spot"
                if i[33] >0.7:
                    text = "Tomato Yellow Leaf Curl Virus"
                
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
        if i[19] >0.7:
            text = "Peach Bacterial Spot"
        
        if i[20] >0.7:
            text = "Pepper Bell Bacterial Spot"
        if i[21] >0.7:
            text = "Potato Early Blight"
        if i[22] >0.7:
            text = "Potato Late Blight"
        if i[23] >0.7:
            text = "Squash Powdery Mildew"
        if i[24] >0.7:
            text = "Strawberry Leaf Scorch"
        if i[25] >0.7:
            text = "Tomato Bacterial Spot"
        if i[26] >0.7:
            text = "Tomato Early Blight"
        if i[27] >0.7:
            text = "Tomato Late Blight"
        if i[28] >0.7:
            text = "Tomato Leaf Mold"
        if i[29] >0.7:
            text = "Tomato Mosaic Virus"
        if i[30] >0.7:
            text = "Tomato Septoria Leaf Spot"
        if i[31] >0.7:
            text = "Tomato Spider mites"
        if i[32] >0.7:
            text = "Tomato Target Spot"
        if i[33] >0.7:
            text = "Tomato Yellow Leaf Curl Virus"
    print(prediction)
    print(text)
    return text
app.run(debug=True)
