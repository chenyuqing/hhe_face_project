import cv2
import imutils
import numpy as np
import dlib


# Function for creating landmark coordinate list
def land2coords(landmarks, dtype="int"):
    # initialize the list of tuples
    # (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (a, b)-coordinates
    for i in range(0, 68):
        coords[i] = (landmarks.part(i).x, landmarks.part(i).y)

    # return the list of (a, b)-coordinates
    return coords


# main Function
if __name__ == "__main__":
    # loading dlib's Hog Based face detector
    face_detector = dlib.get_frontal_face_detector()

    # loading dlib's 68 points-shape-predictor
    # get file:shape_predictor_68_face_landmarks.dat from
    # link: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
    landmark_predictor = dlib.shape_predictor('../model/shape_predictor_68_face_landmarks.dat')

    # Open the input movie file
    vid_name = 'Utolaba_tanweiwei.mp4'
    vid = cv2.VideoCapture('../'+vid_name)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create an output movie file (make sure resolution/frame rate matches input video!)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_movie = cv2.VideoWriter('output_'+vid_name+'.avi', fourcc, 24.97, (640, 360))

    frame_number = 0

    while True:
        ret, frame = vid.read()

        frame_number += 1

        # Quit when the input video file ends
        if not ret:
            break

        # resizing frame
        # you can use cv2.resize but I recommend imutils because its easy to use
        # frame = imutils.resize(frame, width=400)
        # frame = cv2.resize(frame, (400, 400))

        # grayscale conversion of image because it is computationally efficient
        # to perform operations on single channeled (grayscale) image
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detecting faces
        face_boundaries = face_detector(frame_gray, 0)

        for (enum, face) in enumerate(face_boundaries):
            # let's first draw a rectangle on the face portion of image
            x = face.left()
            y = face.top()
            w = face.right() - x
            h = face.bottom() - y
            # Drawing Rectangle on face part
            cv2.rectangle(frame, (x, y), (x + w, y + h), (120, 160, 230), 2)

            # Now when we have our ROI(face area) let's
            # predict and draw landmarks
            landmarks = landmark_predictor(frame_gray, face)
            # converting co-ordinates to NumPy array
            landmarks = land2coords(landmarks)
            print('landmarks[0:17] : {}'.format(landmarks[0:17]))
            pts = landmarks[0:17]
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, pts, True, (255, 255, 0), thickness=5)
            # for (a, b) in landmarks:
            #     # Drawing points on face
            #     cv2.circle(frame, (a, b), 2, (255, 0, 0), -1)

            # Writing face number on image
            cv2.putText(frame, "Face :{}".format(enum + 1), (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 128), 2)

        # Write the resulting image to the output video file
        print("Writing frame {} / {}".format(frame_number, length))
        output_movie.write(frame)

        cv2.imshow("frame", frame)

        #  Stop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break;

    # All done!
    vid.release()
    output_movie.release()
    cv2.destroyAllWindows()