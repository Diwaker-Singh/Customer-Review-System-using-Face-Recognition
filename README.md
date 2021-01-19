# Face-Recognition-System-SDL-Project

# Realtime Customer Review system Using Facial Expression Recognition

The purpose of this project is to help various restaurants, malls and other shops to get a real time review of their services from their customers by reading their facial expression when they enter and are about to exit the store using CCTV cameras, so that they can improve their services to its maximum extent and offer their customers an even  greater experience in the future.

### Idea
* We built a system which reads two video footages (supposedly from a CCTV camera) and extracts frames (2D images) from them.
* The facial expression of the customer in that frame is read and stored in the database when he enters and leaves the restaurant, respectively.
* A calculation based on the facial expressions captured in these two instances is made, and the result obtained by this tells us about the customer experience (i.e., whether it was positive, negative or neutral).

### Implementation
* Facial Detection — Ability to detect the location of face in any input image or frame. The output is the bounding box coordinates of the detected faces
* Facial Recognition — Compare multiple faces together to identify which faces belong to the same person. This is done by comparing face embedding vectors
* Emotion Detection — Classifying the emotion on the face as happy, angry, sad, neutral, surprise, disgust or fear
* Saving in database — Doing some calculations and storing the Realtime reviews of the customers

### Python libraries used
* numpy
* Open CV
* keras
* face_recognition
* SQLite3
* marshal
* mathplotlib

### pre-trained model used
* facial_expression_model_structure.json
* facial_expression_model_weights.h5

### Applications
* Customer feedback System is essential to guide and inform your decision making and influence innovations and changes/ modify to your product or service.
* It's also essential for measuring customer satisfaction among your current customers. 
* FER system can be deployed at Receptions to measure the efficiency of responsible staff in handling the queries of Visitors.
* Remote monitoring of Health of elderly people.
* Can be used for Drowsiness detection for drivers.

### Future Scope
* To make a login page for different user to independently access their account.
* Use 3D image recognition instead of 2D image recognition Using STEM systems replacing CC-TV cameras to improve Expression recognition and use minute expressions for rating which are hard to fake or get mis-interpreted.
* This Web-application can be converted to an android application to provide feedback to shop owners as well as to the customers about the shop they seek.
* We can build our own model by applying transfer learning. Models like VGG or Inception can be adapted. Or we can use some other model for more accuracy.

## Credits

Team Name        Team Members

    D        Diwaker Singh
    
    A        Akshit Mamgain
    
    D        Diwakar Singh
    
    S        Shreya Dubey
