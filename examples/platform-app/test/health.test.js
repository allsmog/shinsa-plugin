import { health } from "../src/server.js";

if (health().status !== "ok") {
  throw new Error("health check failed");
}
