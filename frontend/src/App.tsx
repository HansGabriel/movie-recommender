import { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import useWebSocket from "react-use-websocket";

const WS_URL = "ws://localhost:8000/ws";

type Message = {
	image: string;
	movies: string[];
	emotion: string;
};

function App() {
	const [image, setImage] = useState<string>("");
	const [movies, setMovies] = useState<string[]>([]);
	const [emotion, setEmotion] = useState<string>("");
	const webcamRef = useRef<Webcam>(null);

	const { sendMessage, lastMessage, readyState } = useWebSocket(WS_URL);

	useEffect(() => {
		const interval = setInterval(() => {
			const imageSrc = webcamRef.current?.getScreenshot();
			if (imageSrc) {
				const imageArray = Uint8Array.from(atob(imageSrc.split(",")[1]), (c) =>
					c.charCodeAt(0)
				);
				sendMessage(imageArray);
			}
			if (lastMessage) {
				const data = JSON.parse(lastMessage.data) as Message;
				setImage(data.image);
				setMovies(emotion === data.emotion ? movies : data.movies);
				setEmotion(data.emotion);
			}
		}, 500);

		return () => clearInterval(interval);
	}, [webcamRef, sendMessage, lastMessage]);

	return (
		<>
			<div
				style={{
					display: "flex",
					flexDirection: "row",
				}}
			>
				<Webcam audio={false} ref={webcamRef} mirrored={true} />

				{image && <img src={image} alt="result" />}
			</div>
			<div>
				{movies.map((movie) => (
					<p>{movie}</p>
				))}
			</div>
		</>
	);
}

export default App;
