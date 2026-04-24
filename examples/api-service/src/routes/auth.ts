import express from "express";
import { verifyPassword } from "../auth/password.js";
import { logger } from "../logger.js";

export const authRouter = express.Router();

authRouter.post("/login", async (req, res) => {
  const user = await findUserByEmail(req.body.email);
  if (!user || !(await verifyPassword(req.body.password, user.passwordHash))) {
    logger.warn("login failed", { user: req.body.email });
    return res.status(401).json({ error: "invalid credentials" });
  }

  return res.json({ token: issueSessionToken(user.id) });
});

async function findUserByEmail(email: string): Promise<{ id: string; passwordHash: string } | null> {
  return email ? { id: "user-123", passwordHash: "$2b$12$fixture" } : null;
}

function issueSessionToken(userId: string): string {
  return `session.${userId}.fixture`;
}
