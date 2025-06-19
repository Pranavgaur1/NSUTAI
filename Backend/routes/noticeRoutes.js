const express = require("express");
const router = express.Router();
const noticeController = require("../controllers/noticeController");

router.get("/", noticeController.getAllNotices);
router.post("/", noticeController.addNotice);

module.exports = router;

