import React from "react";

export default function VoiceHelp() {
  return (
    <div className="voice-help">

      <h3>🎙 Voice Commands</h3>

      <ul>
        <li>▶ kiki play song</li>
        <li>⏸ kiki stop song</li>
        <li>⏭ kiki next song</li>
        <li>⏮ kiki previous song</li>
        <h4>Spotify Commands</h4>
        <li>🎧 kiki spotify play</li>
        <li>❤️ kiki spotify stop</li>
        <li>❤️ kiki spotify previous song</li>
        <li>❤️ kiki spotify next song</li>

        <li>⛔ player stop listening</li>
      </ul>

      <p>💡 Tip: Speak clearly after saying player</p>

    </div>
  );
}
