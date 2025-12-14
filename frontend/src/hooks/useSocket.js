import { useEffect, useRef } from "react";
import { io } from "socket.io-client";

const SOCKET_URL = process.env.REACT_APP_API_URL;

export default function useSocket(onNewEvent) {
  const socketRef = useRef(null);

  useEffect(() => {
    // initialize socket connection
    const socket = io(SOCKET_URL, {
      transports: ["websocket"],
      reconnection: true,
    });

    socketRef.current = socket;

    socket.on("connect", () => {
      console.log("connected to socket:", socket.id);
    });

    socket.on("disconnect", () => {
      console.log("disconnected from socket");
    });

    socket.on("new-event", (data) => {
      console.log("new event:", data);
      if (onNewEvent) onNewEvent(data);
    });

    // cleanup on unmount
    return () => {
      socket.disconnect();
    };
  }, [onNewEvent]);

  return socketRef;
}
