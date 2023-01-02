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

# create a websocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # receive the image from the frontend
        data = await websocket.receive_bytes()

        # convert the image to a numpy array
        image = np.frombuffer(data, dtype=np.uint8)

        # decode the image
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        try: 
            # if there is a face in the image, draw a rectangle and the emotion

            # analyze the image
            result = DeepFace.analyze(image, actions=['emotion'], detector_backend='opencv')

            # get the emotion and the coordinates of the face
            x = result['region']['x']
            y = result['region']['y']
            width = result['region']['w']
            height = result['region']['h']
            emotion = result['dominant_emotion']
            
            # setup attributes for the rectangle and text
            rectangle_color = (0, 255, 0)
            text_color = (36,255,12)
            text_scale = 0.9
            thickness = 2

            # draw the rectangle and the text
            cv2.rectangle(image, (x, y), (x + width, y + height), rectangle_color, thickness)

            # draw the text
            cv2.putText(image, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, text_scale, text_color, thickness)

            # encode the image
            _, buffer = cv2.imencode('.jpg', image)

            # convert the image to base64
            image_data = base64.b64encode(buffer)

            # get 5 movies based on the emotion
            movies = get_emotion(result['dominant_emotion'], 5)

            # return a json object with the image and the movies
            response = {
                'image': f'data:image/jpeg;base64,{image_data.decode("utf-8")}',
                'movies': movies,
                'emotion': result['dominant_emotion']
            }
            await websocket.send_json(response)
        except:
            # if there is no face in the image, return the image without the rectangle and text

            # encode the image
            _, buffer = cv2.imencode('.jpg', image)

            # convert the image to base64
            image_data = base64.b64encode(buffer)

            # return a json object with the image and the movies
            response = {
                'image': f'data:image/jpeg;base64,{image_data.decode("utf-8")}',
                'movies': [],
                'emotion': ''
            }
            await websocket.send_json(response)
