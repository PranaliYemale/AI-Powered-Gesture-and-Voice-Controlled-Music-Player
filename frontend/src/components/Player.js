import React, { useState, useRef } from "react";

function Player({ songs }) {

    const API = process.env.REACT_APP_API_URL;

    const [currentIndex, setCurrentIndex] = useState(0);
    const audioRef = useRef(null);

    const play = () => audioRef.current?.play();
    const pause = () => audioRef.current?.pause();

    const next = () => setCurrentIndex((prev) => (prev + 1) % songs.length);

    const prev = () =>
        setCurrentIndex((prev) => (prev - 1 + songs.length) % songs.length);

    const likeSong = async () => {
        await fetch(`${API}/api/like`, {
            method: "POST",
        });
        alert("Song liked!");
    };

    return (
        <div className="player">
            {songs.length > 0 && (
                <>
                    <h2>{songs[currentIndex]}</h2>

                    <audio
                        ref={audioRef}
                        src={`${API}/songs/${songs[currentIndex]}`}
                        controls
                    />

                    <div className="controls">
                        <button onClick={prev}>Prev</button>
                        <button onClick={play}>Play</button>
                        <button onClick={pause}>Pause</button>
                        <button onClick={next}>Next</button>
                        <button onClick={likeSong}>Like</button>
                    </div>
                </>
            )}
        </div>
    );
}

export default Player;