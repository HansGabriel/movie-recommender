import { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import useWebSocket from "react-use-websocket";

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

	const { sendMessage, lastMessage, readyState } = useWebSocket(
		import.meta.env.VITE_WS_URL
	);

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
		<div style={{ padding: "20px" }}>
			<h1 style={{ textAlign: "center", fontFamily: "Poppins" }}>
				Mood Detector and Movie Recommendations System
			</h1>
			<div style={{ display: "flex", justifyContent: "center", gap: "20px" }}>
				<Webcam audio={false} ref={webcamRef} mirrored={true} height={400} />
				{image && <img src={image} alt="result" height={400} width={500} />}
			</div>
			<h2 style={{ textAlign: "center", fontFamily: "Poppins" }}>
				Recommended Movies based on Mood
			</h2>
			<div
				style={{
					display: "flex",
					flexDirection: "row",
					alignItems: "center",
					flexWrap: "wrap",
					justifyContent: "center",
					gap: 40,
				}}
			>
				{movies.map((movie) => (
					<div
						style={{
							display: "flex",
							flexDirection: "column",
							alignItems: "center",
							gap: "20px",
						}}
					>
						<img
							src={movie.poster_url}
							alt="poster"
							height={200}
							width={150}
							style={{ objectFit: "contain" }}
						/>
						<p
							style={{
								fontFamily: "Poppins",
							}}
						>
							{movie.title}
						</p>
					</div>
				))}
			</div>
		</div>
	);
}

export default App;
