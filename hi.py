# import cv2

# cap = cv2.VideoCapture(1)  

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to capture frame")
#         break

#     cv2.namedWindow("Detection Output", cv2.WINDOW_NORMAL)
#     cv2.imshow("Detection Output", frame)
#     cv2.resizeWindow("Detection Output", 800, 600)  # Resize the window if it's too small

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2

cap = cv2.VideoCapture(1)  # Change the index if needed

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

