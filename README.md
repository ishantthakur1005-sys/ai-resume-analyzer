# 📄 AI Resume & Job Description Analyzer

A web application built with **Python**, **Streamlit**, and the **Google Gemini API** that evaluates resume-to-job-description alignment, identifies missing ATS keywords, and generates actionable resume improvements.

## ✨ Features
- **PDF Text Extraction:** Extracts clean text from PDF resumes using `pypdf`.
- **Structured AI Evaluation:** Uses Gemini's JSON output mode for reliable parsing.
- **Automatic Model Fallback:** Switches across Gemini Flash models automatically if a model hits high demand (`503` errors).

## 🛠️ Tech Stack
- Python, Streamlit, Google GenAI SDK (`google-genai`), `pypdf`, `python-dotenv`