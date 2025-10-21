// XOXO/Anime/server.js
import express from "express";
import cors from "cors";
import { spawn } from "child_process";
import * as dotenv from "dotenv";
dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

app.post("/recommend", (req, res) => {
  const { query } = req.body;
  if (!query) return res.status(400).json({ error: "query is required" });

  const py = spawn(process.env.PYTHON_PATH || "python", [
    "-m",
    "pipeline.pipeline_cli",
    "--query",
    query,
  ], {
    cwd: process.cwd(),
    env: { ...process.env },
  });

  let out = "";
  let err = "";

  py.stdout.on("data", (d) => (out += d.toString()));
  py.stderr.on("data", (d) => (err += d.toString()));
  py.on("close", (code) => {
    if (code !== 0) return res.status(500).json({ error: "Pipeline failed", details: err });
    try {
      res.json(JSON.parse(out));
    } catch {
      res.json({ result: out.trim() });
    }
  });
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Node API listening on http://localhost:${port}`));
