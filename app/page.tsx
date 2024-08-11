"use client";
import Image from "next/image";
import Link from "next/link";
import {
  AppBar,
  Avatar,
  Box,
  Container,
  Toolbar,
  InputAdornment,
  TextField,
} from "@mui/material";
import { Mic, Send } from "@mui/icons-material";
import { useState } from "react";

interface ChatMessage {
  sender: string;
  text: string;
  answer?: string;
  tips?: string;
}

function ChatMessage({ sender, text, tips, answer }: ChatMessage) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: sender === "AI" ? "end" : "start",
        alignItems: "center",
        width: "100%",
        position: "relative",
        right: 0,
        marginTop: 2,
      }}
    >
      {sender !== "AI" && <Avatar sx={{ width: 50, height: 50 }} />}

      <Box
        sx={{
          padding: 2,
          width: "70%",
          bgcolor: sender === "AI" ? "orchid" : "lightblue",
          borderRadius: 2,
        }}
      >
        {answer}
        <br />
        <br />
        {text}
        {tips && (
          <Box
            sx={{
              marginTop: 1,
              backgroundColor: "lightyellow",
              padding: 1,
              borderRadius: 2,
            }}
          >
            {tips}
          </Box>
        )}
      </Box>

      {sender === "AI" && (
        <Avatar src="/logo.png" sx={{ width: 50, height: 50 }} />
      )}
    </Box>
  );
}

export default function Home() {
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  const fetchResponse = async (userMessage: string) => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_input: userMessage,
      }),
    });

    const data = await res.json();
    const analysisText = data?.question_analysis?.generations[0][0]?.text || "";
    const tipsText = data?.tips?.generations[0][0]?.text || "";
    const answer = data?.answer || "";

    // Add the AI response to chat history
    setChatHistory((prevChatHistory) => [
      ...prevChatHistory,
      { sender: "AI", text: analysisText, tips: tipsText, answer: answer },
    ]);
  };

  const handleSend = () => {
    if (!message.trim()) return;

    // Add the user's message to the chat history
    setChatHistory((prevChatHistory) => [
      ...prevChatHistory,
      { sender: "User", text: message },
    ]);

    // Fetch AI response
    fetchResponse(message);

    // Clear the message input
    setMessage("");
  };

  return (
    <main>
      <AppBar color="transparent" position="fixed">
        <Image src="/convo-ai.png" alt="logo" width={100} height={100} />
      </AppBar>
      <Toolbar />
      <Container
        sx={{
          marginTop: 6,
        }}
      >
        {chatHistory.map((chatMessage, index) => (
          <ChatMessage
            key={index}
            sender={chatMessage.sender}
            text={chatMessage.text}
            tips={chatMessage.tips}
            answer={chatMessage.answer}
          />
        ))}
        <TextField
          placeholder="Send a message"
          variant="outlined"
          sx={{
            width: "70%",
            position: "fixed",
            bgcolor: "white",
            left: "50%",
            transform: "translateX(-50%)",
            bottom: 0,
            marginBottom: 2,
          }}
          onChange={(e) => setMessage(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Mic />
              </InputAdornment>
            ),
            endAdornment: (
              <InputAdornment position="end">
                <Send sx={{ cursor: "pointer" }} onClick={handleSend} />
              </InputAdornment>
            ),
          }}
        />
      </Container>
    </main>
  );
}
