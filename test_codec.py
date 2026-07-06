import cv2

# Open the webcam (usually device 0, but you can change the index if needed)
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object to save the output file
# Using 'mp4v' codec for .mp4 file format
fourcc = cv2.VideoWriter_fourcc(*'avc1')

# Define the name of the output file, frame rate, and resolution
out = cv2.VideoWriter('output.mp4', fourcc, 30, (1920, 1080))

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Capture one frame to get the frame size
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from webcam.")
    cap.release()
    exit()

# Print frame size
height, width, _ = frame.shape
print(f"Frame size: {width}x{height}")

# Loop to capture frames from the webcam
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # Write the frame to the output file
        out.write(frame)

        # Display the frame to the user
        cv2.imshow('Webcam Feed', frame)

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Error: Could not read frame.")
        break

# Release the webcam and output file, and close display window
cap.release()
out.release()
cv2.destroyAllWindows()