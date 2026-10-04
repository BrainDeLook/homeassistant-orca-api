import express from "express";
import { errorHandler } from "./middleware/error";
import health from "./routes/health/route";
import profiles from "./routes/profiles/route";
import asyncSlicing from "./routes/slicing/async.route";
import slicing from "./routes/slicing/route";
import cors from "cors";

export const configureApp = () => {
  const app = express();

  app.use(
    cors({
      origin: process.env.CORS_ORIGINS ?? "*", // if not set, allow all origins
      methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      allowedHeaders: ["Content-Type", "Authorization"],
      exposedHeaders: [
        "Content-Disposition",
        "ETag",
        "Last-Modified",
        "Content-Length",
        "X-Filament-Used-G",
        "X-Filament-Used-Mm",
        "X-Print-Time-Seconds",
      ],
    })
  );

  app.use(express.json());

  app.get("/", (_req, res) => {
    res.type("html").send(`<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OrcaSlicer API</title><style>body{font:16px system-ui,sans-serif;max-width:650px;margin:10vh auto;padding:24px;background:#171c20;color:#f1f5f3}main{background:#242d30;border-radius:16px;padding:28px}h1{color:#31d17b}a{color:#82b9ff}</style><main><h1>● OrcaSlicer API запущен</h1><p>Серверная нарезка для Bambuddy.</p><p>Проверка: <a href="/health">/health</a></p></main></html>`);
  });

  app.use("/health", health);
  app.use("/profiles", profiles);
  app.use("/slice", slicing);
  app.use("/slice-async", asyncSlicing);

  app.use(errorHandler);

  return app;
};

const app = configureApp();

const port = process.env.PORT || 3000;

// Production does not need swagger.json. The old HA package crashed because
// its runtime imported that file but the image did not include it.

// Importing this module must not bind a port under test. The e2e setup calls
// `configureApp()` and does its own `listen(0)`, and the unit tests re-import
// through `vi.resetModules()` -- so the module-level listen raced its own
// earlier instances for port 3000 and printed "App listening" once per import.
if (process.env.NODE_ENV !== "test") {
  app.listen(port, () => {
    console.log(`App listening on port ${port}`);
  });
}
