"use client";
import Image from "next/image";
import styles from "./page.module.css";
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

export default function Home() {
  const [message, setMessage] = useState("");

  return (
    <main className={styles.main}>
      <AppBar color="transparent" position="fixed">
        <Image src="/convo-ai.png" sx alt="logo" width={100} height={100} />
      </AppBar>
      <Toolbar />
      <Container
        sx={{
          marginTop: 6,
        }}
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "start",
            alignItems: "center",
            width: "100%",
            marginTop: 2,
          }}
        >
          <Avatar src="/logo.png" sx={{ width: 50, height: 50 }} />
          <Box
            sx={{
              padding: 2,
              width: "70%",

              bgcolor: "grey.300",
              borderRadius: 2,
            }}
          >
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
          </Box>
        </Box>

        <Box
          sx={{
            display: "flex",
            justifyContent: "end",
            alignItems: "center",
            width: "100%",
            position: "relative",
            right: 0,
            marginTop: 2,
          }}
        >
          <Box
            sx={{
              padding: 2,
              width: "70%",
              bgcolor: "orchid",
              borderRadius: 2,
            }}
          >
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
          </Box>
          <Avatar src="/logo.png" sx={{ width: 50, height: 50 }} />
        </Box>
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            marginTop: 10,
          }}
        ></Box>
        <TextField
          placeholder="Send a message"
          variant="outlined"
          sx={{
            width: "70%",
            position: "absolute",
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
                <Send />
              </InputAdornment>
            ),
          }}
        />
      </Container>
    </main>
  );
}
