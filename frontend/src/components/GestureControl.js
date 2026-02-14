import React, { useRef, useEffect } from "react";
import { Hands } from "@mediapipe/hands";
import { Camera } from "@mediapipe/camera_utils";
import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL + "/api";
const COOLDOWN = 800;

function GestureControl() {
  const videoRef = useRef(null);
  const lastActionTime = useRef(0);

  useEffect(() => {
    const hands = new Hands({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
      maxNumHands: 1,
      minDetectionConfidence: 0.7,
      minTrackingConfidence: 0.7,
    });

    hands.onResults((results) => {
      if (!results.multiHandLandmarks.length) return;
      if (Date.now() - lastActionTime.current < COOLDOWN) return;

      const hand = results.multiHandLandmarks[0];

      const thumb = hand[4];
      const index = hand[8];
      const middle = hand[12];
      const ring = hand[16];
      const pinky = hand[20];
      const wrist = hand[0];

      const pinchDist = Math.abs(thumb.x - index.x);

      const sendAction = (route) => {
        axios.post(`${API_BASE}/${route}`).catch(() => {});
        lastActionTime.current = Date.now();
      };

      if (thumb.y < index.y && index.y < middle.y && middle.y < ring.y && ring.y < pinky.y) {
        sendAction("play");
        return;
      }

      if (thumb.y > index.y && index.y > middle.y && middle.y > ring.y && ring.y > pinky.y) {
        sendAction("pause");
        return;
      }

      if (index.x - wrist.x > 0.25) {
        sendAction("next");
        return;
      }

      if (index.x - wrist.x < -0.25) {
        sendAction("prev");
        return;
      }

      if (pinchDist > 0.18) {
        sendAction("volume_up");
        return;
      }

      if (pinchDist < 0.04) {
        sendAction("volume_down");
        return;
      }

      if (thumb.y < index.y - 0.05) {
        sendAction("like");
        return;
      }

      if (thumb.y > index.y + 0.1) {
        sendAction("dislike");
        return;
      }
    });

    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        await hands.send({ image: videoRef.current });
      },
      width: 640,
      height: 480,
    });

    camera.start();
  }, []);

  return (
    <div style={{ marginTop: 10 }}>
      <video
        ref={videoRef}
        style={{
          width: "320px",
          borderRadius: "15px",
          border: "2px solid #444"
        }}
      />
    </div>
  );
}

export default GestureControl;