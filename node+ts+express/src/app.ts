import express from "express";
import { loadWebHookEndpoints } from "./webhook";
const app = express();
const port = 3000;

loadWebHookEndpoints(app);

app.listen(port, () => {
  return console.log(`Express is listening at http://localhost:${port}`);
});
