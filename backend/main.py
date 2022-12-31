import base64
import numpy as np
import cv2
from fastapi import FastAPI, WebSocket
from deepface import DeepFace
import json
import random

app = FastAPI()


def get_emotion(emotion: str, n: int):
    # open the json file
    with open('emotion_dict.json') as json_file:
        data = json.load(json_file)

        # map the emotion to the emotion in the json file
        mapped_emotion = ''
        match emotion:
            case "angry":
                mapped_emotion = 'anger'
            case "disgust":
                mapped_emotion = 'fear'
            case "fear":
                mapped_emotion = 'fear'
            case "happy":
                mapped_emotion = 'joy'
            case "sad":
                mapped_emotion = 'sadness'
            case "surprise":
                mapped_emotion = 'surprise'
            case "neutral":
                mapped_emotion = ''
        
        # if mapped_emotion is empty, choose a random emotion and return num_movies movies from the list
        if mapped_emotion == '':
            # choose a random emotion and get n movies from the list
            random_emotion = random.choice(list(data.keys()))
            # get n random movies from the list
            random_movies = random.sample(data[random_emotion], n)
            # return the movies
            return random_movies

        # if mapped_emotion is not empty, return num_movies movies from the list
        else:
            # get n random movies from the list
            random_movies = random.sample(data[mapped_emotion], n)
            # return the movies
            return random_movies


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        image = np.frombuffer(data, dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        try: 
            result = DeepFace.analyze(image, actions=['emotion'], detector_backend='opencv')

            cv2.rectangle(image, (result['region']['x'], result['region']['y']), (result['region']['x'] + result['region']['w'], result['region']['y'] + result['region']['h']), (0, 255, 0), 2)
            cv2.putText(image, result['dominant_emotion'], (result['region']['x'], result['region']['y'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            _, buffer = cv2.imencode('.jpg', image)
            image_data = base64.b64encode(buffer)
            # get 5 random movies from the emotion
            movies = get_emotion(result['dominant_emotion'], 5)
            # return a json object with the image and the movies
            await websocket.send_json({'image': f'data:image/jpeg;base64,{image_data.decode("utf-8")}', 'movies': movies, 'emotion': result['dominant_emotion']})
        except:
            _, buffer = cv2.imencode('.jpg', image)
            image_data = base64.b64encode(buffer)
            # return a json object with the image and the movies
            await websocket.send_json({'image': f'data:image/jpeg;base64,{image_data.decode("utf-8")}', 'movies': [], 'emotion': ''})

