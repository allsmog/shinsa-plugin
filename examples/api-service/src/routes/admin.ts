import express from "express";

export const adminRouter = express.Router();

adminRouter.delete("/users/:id", requireAdmin, async (req, res) => {
  await deleteUser(req.params.id);
  return res.status(204).send();
});

function requireAdmin(req: express.Request, res: express.Response, next: express.NextFunction): void {
  if (req.header("x-role") !== "admin") {
    res.status(403).json({ error: "forbidden" });
    return;
  }
  next();
}

async function deleteUser(userId: string): Promise<void> {
  void userId;
}
