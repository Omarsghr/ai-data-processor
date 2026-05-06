#  Universal AI Director Toolkit
An automated video editing pipeline using AI-driven logic and signal analysis.

## The Workflow
Our project uses a 4-Step Pipeline to turn raw footage into a cinematic edit:
1. AI Logic: Transcribes audio via Groq API and detects keywords for Zooms, Images, and Music.
2. Signal Analysis: Identifies silence and "dead air" for automatic Cuts.
3. Data Formatter: Merges all findings into a JSON Screenplay.
4. Database: A central `sqlite3` memory that logs every action automatically.

## 👥 The Team
- Architect (omar): Logic, API Management, and AI Director Engine.
- Production Hub (houssam): Heavy processing, Image/Video Generation, and Signal Analysis.
- Assembler (abdo): Data Formatting and JSON generation for Adobe Premiere.

## 🛠 Tech Stack
- Language: Python
- Database: SQLite3
- APIs: Groq (Transcription), Image/Video Gen APIs.
- Software: Adobe Premiere Pro (via custom JSX Extension).
