const mongoose = require("mongoose");

const noticeSchema = new mongoose.Schema({
  title: { type: String, required: true },
  content: { type: String, required: true },
  summary: { type: String },
  category: { type: String, default: "General" },
  pdfUrl: { type: String },
  date: { type: Date, default: Date.now }
});

module.exports = mongoose.model("Notice", noticeSchema);

