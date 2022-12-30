import { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import useWebSocket from "react-use-websocket";

const WS_URL = "ws://localhost:8000/ws";

function App() {
	const [result, setResult] = useState<string | null>(null);
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
				setResult(lastMessage.data);
			}
		}, 500);

		return () => clearInterval(interval);
	}, [webcamRef, sendMessage, lastMessage]);

	return (
		<div
			style={{
				display: "flex",
				flexDirection: "row",
			}}
		>
			<Webcam audio={false} ref={webcamRef} mirrored={true} />

			{result && <img src={result} alt="result" />}
		</div>
	);
}

export default App;
