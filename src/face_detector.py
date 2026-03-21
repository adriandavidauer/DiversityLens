"""
This module is responsible for detecting human faces within a given dataset,
which may include both images and videos.
"""

import os, dlib, cv2


model_dir= "dlib_models"
#face_detector_path= os.path.join(model_dir, "mmod_human_face_detector.dat")    #real face detector file
shape_detector_path= os.path.join(model_dir, "shape_predictor_5_face_landmarks.dat")

try:
    #detector= dlib.cnn_face_detection_model_v1(face_detector_path)     #the real face detector
    detector = dlib.get_frontal_face_detector()   #basic face detector with lower accuracy
    sp= dlib.shape_predictor(shape_detector_path)
    print("Done !")
except Exception as e:
    print(f"Something is wrong. Error : {e}")
    exit()

image_path= "person.jpeg"

if not os.path.exists(image_path):
    print(f"Error: '{image_path}'")
else:
    print("Loading image...")
    img= cv2.imread(image_path)
    rgb_img= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print("face is searching")
    dets= detector(rgb_img, 1)

    if len(dets)==0:
        print("No face, or inaccurate detection.")
    else:
        print(f"Done! {len(dets)} number of face is found")
 
        for i, d in enumerate(dets):  # go into a for loop for each face
            face= d
            print(f"face {i} coordinates: {face}")
            shape= sp(rgb_img, face)

            (x1,y1,x2,y2)= (face.left(), face.top(), face.right(), face.bottom())
            cv2.rectangle(img, (x1,y1),(x2,y2), (0, 0, 255), 6)
        
        output_file= "test_output.jpeg"
        cv2.imwrite(output_file, img)
        print("go head bud !")