const Notice = require("../models/Notice");

const sanitize = (str) => str.replace(/<[^>]*>?/gm, '');

exports.getAllNotices = async (req, res) => {
  try {
    const notices = await Notice.find().sort({ date: -1 });
    res.json(notices);
  } catch (err) {
    console.error("Error fetching notices:", err);
    res.status(500).json({ message: "Server error" });
  }
};

// POST /api/notices - Add a new notice (used by OCR/scraper)
exports.addNotice = async (req, res) => {
  const { title, content, summary, category, pdfUrl } = req.body;

  if (!title || !content) {
    return res.status(400).json({ message: "Title and content are required." });
  }

  try {
    const newNotice = new Notice({
      title: sanitize(title),
      content: sanitize(content),
      summary: summary ? sanitize(summary) : "",
      category: category || "General",
      pdfUrl,
      date: new Date()
    });

    await newNotice.save();
    res.status(201).json(newNotice);
  } catch (err) {
    console.error("Failed to save notice:", err);
    res.status(500).json({ message: "Failed to add notice." });
  }
};

