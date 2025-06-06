from flask import Flask, render_template, request, redirect, url_for
from fer import FER
import cv2
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Analyze emotions from uploaded video
def analyze_emotions_from_video(filepath):
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(filepath)
    emotions_list = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = detector.detect_emotions(frame)
        if results:
            emotions_list.append(results[0]["emotions"])
    cap.release()

    if emotions_list:
        aggregated = {}
        keys = emotions_list[0].keys()
        for key in keys:
            aggregated[key] = round(sum(d[key] for d in emotions_list) / len(emotions_list) * 100, 2)

        emoji_map = {
            "angry": "😠", "disgust": "🤢", "fear": "😨", "happy": "😄",
            "sad": "😢", "surprise": "😲", "neutral": "😐"
        }

        emotion_data = [
            {"emotion": k.capitalize(), "score": v, "emoji": emoji_map[k]} for k, v in aggregated.items()
        ]

        top_key = max(aggregated, key=aggregated.get)
        top_emotion = {
            "emotion": top_key.capitalize(),
            "score": aggregated[top_key],
            "emoji": emoji_map[top_key]
        }

        return emotion_data, top_emotion

    return None, None

# Index route (upload page)
@app.route('/', methods=['GET', 'POST'])
def index():
    emotion_data = None
    top_emotion = None

    if request.method == 'POST':
        file = request.files.get('video_file')
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            emotion_data, top_emotion = analyze_emotions_from_video(filepath)

    return render_template('index.html', emotions=emotion_data, top=top_emotion)

# Live camera emotion detection route
@app.route('/camera')
def camera():
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)

    emoji_map = {
        "angry": "😠", "disgust": "🤢", "fear": "😨", "happy": "😄",
        "sad": "😢", "surprise": "😲", "neutral": "😐"
    }

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        emotions = detector.detect_emotions(frame)
        if emotions:
            scores = emotions[0]['emotions']
            top_emotion = max(scores, key=scores.get)
            top_score = scores[top_emotion]

            # Display all emotions
            y0 = 20
            for i, (emo, score) in enumerate(scores.items()):
                label = f"{emoji_map.get(emo, '')} {emo.capitalize()}: {round(score * 100, 2)}%"
                cv2.putText(frame, label, (10, y0 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Display top emotion
            top_label = f"Top: {emoji_map[top_emotion]} {top_emotion.capitalize()} ({round(top_score * 100, 2)}%)"
            cv2.putText(frame, top_label, (10, y0 + len(scores) * 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow('🎥 Live Emotion Detector (Press Q to quit)', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
