import cv2
import mediapipe as mp
import pandas as pd
import time
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


vote = 'A'
user = 'Rosie'
video = '../data/phone_s22/'+vote+'/downsample_480p/'+user+'_'+vote+'_10_downsample_480p.mp4'

new_header = ['time_step']
for i in range(478):
    new_header.append(str(i)+'_x')
    new_header.append(str(i)+'_y')
    new_header.append(str(i)+'_z')
total_array = pd.DataFrame(columns=new_header)

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(video)

# For save meshed video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('../data/phone_s22/'+vote+'/downsample_480p/mesh_video.mp4', fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  
  frame_counter = 0
  # Play video segment
  while cap.isOpened():
    success, image = cap.read()
    if not success: 
      break
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
    frame_counter += 1

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # cv2.imwrite('../data/phone_s22/'+vote+'/'+user+'/'+str(frame_counter)+'.jpg', cv2.flip(image, 1))

    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:

        # save landmarks
        new_row = [time.time()]
        for idx, landmark in enumerate(face_landmarks.landmark):
          new_row.append(landmark.x)
          new_row.append(landmark.y)
          new_row.append(landmark.z)
        total_array.loc[len(total_array)] = new_row

        # Face tesselation
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())

        # Face contours
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())

        # Face irises
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))

    # Save the current frame number
    # cv2.imwrite('../data/phone_s22/'+vote+'/downsample_480p/'+str(frame_counter)+'.jpg', cv2.flip(image, 1))
    out.write(image)

    if cv2.waitKey(5) & 0xFF == 27:
      time_step = total_array.time_step
      time_diff = time_step.diff()
      FPS = 1/time_diff
      print('FPS:',FPS.mean())
      break
cap.release()
# total_array.to_csv('../data/phone_s22/'+vote+'/'+user+'/'+vote+'.csv', sep=',', index=False)