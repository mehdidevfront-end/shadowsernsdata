

const express = require("express");
const router = express.Router();


router.post("/", (req, res) => {
    res.json({ message: "Bienvenue sur l'API 🚀" });
  });
module.exports = router;
