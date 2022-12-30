import base64
import numpy as np
import cv2
from fastapi import FastAPI, WebSocket
from deepface import DeepFace

app = FastAPI()

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
            await websocket.send_text(f'data:image/jpeg;base64,{image_data.decode("utf-8")}')
        except:
            _, buffer = cv2.imencode('.jpg', image)
            image_data = base64.b64encode(buffer)
            await websocket.send_text(f'data:image/jpeg;base64,{image_data.decode("utf-8")}')


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_bytes()
#         image = np.frombuffer(data, dtype=np.uint8)
#         image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#         _, buffer = cv2.imencode('.jpg', image)
#         image_data = base64.b64encode(buffer)
#         await websocket.send_text(f'data:image/jpeg;base64,{image_data.decode("utf-8")}')
        