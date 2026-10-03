# Smart Camera Analytics

Live webcam intrusion detection that only alerts on **moving people**. Background subtraction gates YOLOv8 so a person in a photo on the wall, a mannequin, or a parked reflection never triggers an alert — only something that actually moved and is actually a human.

When the human count goes up, it fires a Telegram message plus a snapshot of the frame.

---

## Why the two-stage approach

Running YOLO alone on a static camera produces constant false positives: posters, TV screens, a jacket on a chair. Running motion detection alone triggers on cats, curtains and shadows.

This runs both and takes the intersection:

```
Frame
  ├─► MOG2 background subtractor ──► median blur ──► contours
  │        keep blobs 1,500–50,000 px  →  "moving regions"
  │
  └─► YOLOv8n inference ──► boxes where class == "person" and confidence > 0.5
                                   │
                                   ▼
          Person box overlaps a moving region?  ──► count as a human
                                   │
                                   ▼
          Count increased since last frame?     ──► Telegram alert + photo
```

Alerting on the *increase* rather than the raw count means one intruder standing in frame for a minute produces one alert, not 1,800.

---

## Stack

| Component | Tech |
|---|---|
| Detection | YOLOv8n (Ultralytics) |
| Motion | OpenCV `createBackgroundSubtractorMOG2`, history 500, varThreshold 50 |
| Video | OpenCV VideoCapture |
| Alerting | Telegram Bot API (`sendMessage` and `sendPhoto`) |

---

## Running it

```bash
pip install ultralytics opencv-python requests python-dotenv
```

Create a `.env`:

```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Then:

```bash
python main.py
```

Press `q` in the preview window to quit. Change the `VideoCapture` index if you have more than one camera.

---

## Files

```
main.py             # detection loop, motion gating, Telegram alerting
hi.py               # YOLO inference experiments
test.py             # camera and model smoke test
yolov8n.pt          # nano weights — fast enough for real-time CPU
detected_human.jpg  # last captured alert frame
```

---

## Tuning

| Parameter | Effect |
|---|---|
| `1500 < area < 50000` | Contour size window — raise the floor to ignore small movement, lower the ceiling to ignore lighting shifts |
| `confidence > 0.5` | YOLO person threshold — raise it in busy scenes |
| `varThreshold=50` | MOG2 sensitivity — lower is more sensitive to subtle motion |
| `history=500` | How many frames feed the background model before it stabilises |
