import numpy as np
import cv2
from keras.preprocessing import image
from keras.models import load_model
from keras.models import model_from_json
import face_recognition
import sqlite3
import marshal


# _______________ connecting to database _________________
conn = sqlite3.connect('customers.sqlite')
cursor = conn.cursor()
print('Opened Successfully')


# __________________ delete function ___________________________
def delete_from_known_faces(match,known_face_encodings):
    list_size = len(match)
    i=0
    idx=0
    for i in range(0,list_size,1):
        if match[i] == True:
            idx = i
            break

    known_face_encodings.pop(idx)


# __________________ get_unique_id ___________________________
def get_unique_id(match,known_face_encodings):
    list_size = len(match)
    i=0
    idx=0
    for i in range(0,list_size,1):
        if match[i] == True:
            idx = i
            break

    return idx

# __________________ check function ___________________________
def check(match):
    for element in match:
        if element == True:
            return True
    return False
    
    
# __________________________ update __________________________
def upd(records,scl):
    new_record=[None]*7
    for i in range(0,7):
        new_record[i]=records[i]+(scl[i])

    return new_record


#________________________ calculate ____________________________

def calculate(records):
    # 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral 
    ans=0
    ans+=2*records[3]
    ans+=records[6]
    ans+=2*records[5]
    ans-=2*records[0]
    ans-=2*records[1]
    ans-=2*records[2]
    ans-=2*records[4]
    ans/=(records[7]+1)
    return ans


#opencv initialization

# face_cascade = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')

entry_video = 'sad.mp4' #input from CCTV 1 on entrance
exit_video = 'happy.mp4' #input from CCTV 2 on exit gate

cap = cv2.VideoCapture(entry_video)
cap_exit = cv2.VideoCapture(exit_video)


# face expression recognizer initialization
from keras.models import model_from_json
model = model_from_json(open(r"facial_expression_model_structure.json", "r").read())
model.load_weights(r'facial_expression_model_weights.h5') #load weights

#_______________________________
# detector = MTCNN()
# detector_exit = MTCNN()
#-----------------------------

emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
face_locations = []
face_encodings = []
face_names = []


known_face_encodings = []
exit_known_face_encodings = []


while(True):
    flag=0
    try:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_recognition.face_locations(img)

        for (top, right, bottom, left) in faces:
            # print('inside faces')
            cv2.rectangle(img,(left,top),(right,bottom),(255,0,0),2) #draw rectangle to main image
            detected_face = img[int(top):int(bottom), int(left):int(right)] #crop detected face
            
            face_encodings = face_recognition.face_encodings(detected_face)
            detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
            detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
            img_pixels = image.img_to_array(detected_face)
            img_pixels = np.expand_dims(img_pixels, axis = 0)
            img_pixels /= 255 # pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
            predictions = model.predict(img_pixels) #store probabilities of 7 expressions
            #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral 
            max_index = np.argmax(predictions[0])
            emotion = emotions[max_index]
            # print(predictions[0])
            # my_formatted_list = [ '%.4f' % elem for elem in predictions[0]]
            # print(my_formatted_list)


            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]
                match = face_recognition.compare_faces(known_face_encodings,face_encoding,tolerance=0.6)
                if check(match) == False:
                    print('new face detected')
                    known_face_encodings.append(face_encoding)
                    data = marshal.dumps(face_encoding)

                    scl=[None]*7
                    for i in range(0,7): scl[i]=int(predictions[0][i] * 10000)
                    insert_statement = '''insert into customer (Id,Entry_angry,Entry_disgust,Entry_fear,Entry_happy,Entry_sad,Entry_surprise,Entry_neutral,Entry_cnt,Entry_mood) values (?,?,?,?,?,?,?,?,?,?)'''
                    cursor.execute(insert_statement,(data,scl[0],scl[1],scl[2],scl[3],scl[4],scl[5],scl[6],1,0))
                    conn.commit()
                else:
                    idx = get_unique_id(match,known_face_encodings)
                    unique_id = known_face_encodings[idx]
                    data = marshal.dumps(unique_id)
                    statement='''select Entry_angry,Entry_disgust,Entry_fear,Entry_happy,Entry_sad,Entry_surprise,Entry_neutral,Entry_cnt,Entry_mood from customer where Id = ?'''
                    cursor.execute(statement,(data,))
                    conn.commit()

                    records=cursor.fetchone()
                    scl=[None]*7
                    for i in range(0,7): scl[i]=int(predictions[0][i] * 10000)
                    updated = upd(records,scl)
                    ans=calculate(records)
                    # print(ans)
                    upd_statement = ''' UPDATE customer SET Entry_angry=?,Entry_disgust=?,Entry_fear=?,Entry_happy=?,Entry_sad=?,Entry_surprise=?,Entry_neutral = ?,Entry_cnt = ?,Entry_mood=?   WHERE id = ?'''
                    cursor.execute(upd_statement,(updated[0],updated[1],updated[2],updated[3],updated[4],updated[5],updated[6],(records[7])+1,ans,data))
                    conn.commit()

            #write emotion text above rectangle
            cv2.putText(img, emotion, (int(left), int(top)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            #process on detected face end
            #-------------------------

        cv2.imshow('img',img)
        
    except:
        flag=1
# ______________________________________________________________________________________________________


    try:
        ret_exit, img_exit= cap_exit.read()
        gray = cv2.cvtColor(img_exit, cv2.COLOR_BGR2GRAY)
        faces = face_recognition.face_locations(img_exit)

        for (top, right, bottom, left) in faces:
            cv2.rectangle(img_exit,(left,top),(right,bottom),(255,0,0),2) #draw rectangle to main image

            detected_face_exit = img_exit[int(top):int(bottom), int(left):int(right)] #crop detected face
            face_encodings_exit = face_recognition.face_encodings(detected_face_exit)
            detected_face_exit = cv2.cvtColor(detected_face_exit, cv2.COLOR_BGR2GRAY) #transform to gray scale
            detected_face_exit = cv2.resize(detected_face_exit, (48, 48)) #resize to 48x48
            img_pixels_exit = image.img_to_array(detected_face_exit)
            img_pixels_exit = np.expand_dims(img_pixels_exit, axis = 0)
            img_pixels_exit /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
            predictions_exit = model.predict(img_pixels_exit) #store probabilities of 7 expressions
            #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral 
            max_index_exit = np.argmax(predictions_exit[0])
            emotion_exit = emotions[max_index_exit]

            if len(face_encodings_exit) > 0:
                face_encoding_exit = face_encodings_exit[0]
                match = face_recognition.compare_faces(exit_known_face_encodings,face_encoding_exit,tolerance=0.6)
                match_for_entry = face_recognition.compare_faces(known_face_encodings,face_encoding_exit,tolerance=0.6)

                if check(match):
                    idx=get_unique_id(match_for_entry,known_face_encodings)
                    unique_id=known_face_encodings[idx]

                    data = marshal.dumps(unique_id)
                    statement='''select Exit_angry,Exit_disgust,Exit_fear,Exit_happy,Exit_sad,Exit_surprise,Exit_neutral,Exit_cnt,Exit_mood,Entry_mood from customer where Id = ?'''
                    cursor.execute(statement,(data,))

                    records=cursor.fetchone()
                    scl=[None]*7
                    for i in range(0,7): scl[i]=int(predictions_exit[0][i] * 10000)
                    updated = upd(records,scl)

                    ans=calculate(records)
                    res=ans-records[9]
                    # print('Entry mood ',records[9])
                    # print('Exit mood' ,ans)

                    upd_statement = ''' UPDATE customer SET Exit_angry=?,Exit_disgust=?,Exit_fear=?,Exit_happy=?,Exit_sad=?,Exit_surprise=?,Exit_neutral = ?,Exit_cnt=?,Exit_mood=?,Result=?   WHERE id = ?'''
                    cursor.execute(upd_statement,(updated[0],updated[1],updated[2],updated[3],updated[4],updated[5],updated[6],records[7]+1,ans,res,data))
                    conn.commit()

                elif check(match_for_entry) == True:
                    idx = get_unique_id(match_for_entry,known_face_encodings)
                    unique_id = known_face_encodings[idx]
                    exit_known_face_encodings.append(unique_id)

                    data = marshal.dumps(unique_id)

                    scl=[None]*7
                    for i in range(0,7): scl[i]=int(predictions_exit[0][i] * 10000)
                    ans=0
                    for i in range(0,7): ans=ans+scl[i]

                    upd_statement = ''' UPDATE customer SET Exit_angry=?,Exit_disgust=?,Exit_fear=?,Exit_happy=?,Exit_sad=?,Exit_surprise=?,Exit_neutral = ?,Exit_cnt=?,Exit_mood=?   WHERE id = ?'''
                    cursor.execute(upd_statement,(scl[0],scl[1],scl[2],scl[3],scl[4],scl[5],scl[6],1,ans,data))
                    conn.commit()

            #write emotion text above rectangle
            cv2.putText(img_exit, emotion_exit, (int(left), int(top)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            #process on detected face end
            #-------------------------

        cv2.imshow('img_exit',img_exit)
    except:
        if flag==1:
            break
            
# ____________________________________


    if cv2.waitKey(1) & 0xFF == ord('q') or (ret==False and ret_exit==False): #press q to quit
        break
#kill open cv things
print(len(known_face_encodings))
cap.release()
cv2.destroyAllWindows()
