import cv2
import numpy as np
import torch
import requests
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # You can use a different variant like yolov8s.pt for better accuracy

# Telegram bot credentials
BOT_TOKEN = "7911248469:AAGPwOXA_JxDEli4uZyruGZG54TJDD-w5w0"
CHAT_ID = "5234509488"

previous_human_count = 0  # Track the number of humans detected

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def send_telegram_photo(image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as photo:
        data = {"chat_id": CHAT_ID}
        files = {"photo": photo}
        requests.post(url, data=data, files=files)

def detect_moving_human():
    global previous_human_count
    cap = cv2.VideoCapture(0)  # Change index based on your webcam
    fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for better processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)
        fgmask = cv2.medianBlur(fgmask, 5)

        # Find contours of moving objects
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        moving_objects = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if 1500 < area < 50000:
                x, y, w, h = cv2.boundingRect(contour)
                moving_objects.append((x, y, w, h))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "Moving Object", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        # Detect objects using YOLOv8
        results = model(frame)
        human_count = 0
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = model.names[class_id]

                # Detect only humans
                if label == "person" and confidence > 0.5:
                    is_moving = any(abs(x1 - mx) < (x2 - x1) and abs(y1 - my) < (y2 - y1) for mx, my, _, _ in moving_objects)
                    if is_moving:
                        human_count += 1
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, "Human Detected", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Send alert and photo only when the human count increases
        if human_count > previous_human_count:
            send_telegram_message(f"Alert! {human_count} human(s) detected in the monitored area.")
            image_path = "detected_human.jpg"
            cv2.imwrite(image_path, frame)
            send_telegram_photo(image_path)
        previous_human_count = human_count
        
        # Show the output
        cv2.imshow("Detection Output", frame)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_moving_human()
