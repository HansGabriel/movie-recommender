import { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import useWebSocket from "react-use-websocket";

const WS_URL = "ws://localhost:8000/ws";

type Movie = {
	title: string;
	poster_url: string;
};

type Message = {
	image: string;
	movies: Movie[];
	emotion: string;
};

function App() {
	const [image, setImage] = useState<string>("");
	const [movies, setMovies] = useState<Movie[]>([]);
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
				setMovies(emotion !== data.emotion ? data.movies : movies);
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
					justifyContent: "center",
				}}
			>
				<Webcam audio={false} ref={webcamRef} mirrored={true} height={400} />

				{image && <img src={image} alt="result" height={400} width={500} />}
			</div>
			<div
				style={{
					display: "flex",
					flexDirection: "column",
					justifyContent: "center",
				}}
			>
				{movies.map((movie) => (
					<div
						style={{
							display: "flex",
							flexDirection: "column",
							justifyContent: "center",
						}}
					>
						<img
							src={movie.poster_url}
							alt="poster"
							height={200}
							width={150}
							style={{ objectFit: "contain" }}
						/>
						<p>{movie.title}</p>
					</div>
				))}
			</div>
		</>
	);
}

export default App;
