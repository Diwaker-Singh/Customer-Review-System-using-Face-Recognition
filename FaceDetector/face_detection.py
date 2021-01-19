import cv2
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
img = cv2.imread("shreya_img.jpg", 1)
# img = cv2.imread("Screenshot (101).png", 1)
# print(type(img))
# print(img.shape)
img = cv2.resize(img, (int(1*img.shape[1]/2), int(1*img.shape[0]/2)))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray_img, scaleFactor = 1.05, minNeighbors = 5)
for x,y,w,h in faces:
    img = cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
cv2.imshow("Face Detection", img)
cv2.waitKey()
cv2.destroyAllWindows()
listOfFaces = []
for x,y,w,h in faces:
    x = img[y:y+h, x:x+w]
    x = cv2.resize(x, (48, 48))
    listOfFaces.append(x)
    cv2.imshow("faces", x)
    cv2.waitKey()
    cv2.destroyAllWindows()
print(listOfFaces)