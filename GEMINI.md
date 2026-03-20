# Project: Sefferweich Schulchronik Transcription

## Project Overview
This project is dedicated to the transcription and documentation of the historical "Schulchronik" (School Chronicle) of Sefferweich, Bitburg. The chronicle spans from 1851 through the mid-20th century, documenting the history, geography, and educational development of the village.

The transcription process involves using Gemini to analyze scans of the handwritten chronicle and convert them into digital text format, maintaining original layout and annotations where possible.

## Directory Overview
- `Scans/`: Contains the original JPEG images of the handwritten school chronicle.
- `Transkript/`: Contains individual Markdown (`.md`) files for each page or section of the chronicle. These files include the transcription and notes on formatting.
- `Transkript.txt`: A consolidated file containing the full transcription of the chronicle in a plain text format.
- `gemini_link.txt`: Contains a link to a shared Gemini conversation used during the transcription process.

## Key Files
- `Transkript.txt`: The primary consolidated transcription of the chronicle. It includes historical details about the village's location, origins, and school history.
- `Transkript/002.md` to `Transkript/010.md`: Individual page transcriptions that correspond to the image files in the `Scans/` directory.

## Transcription Conventions
- **Formatting:** Transcriptions aim to preserve the original indentation and layout using code blocks or specific Markdown formatting.
- **Repeat Marks:** Double quotes (`"`) are often used in the original text to indicate repetition of words (e.g., "Lehrer", "Fortgesetzt von").
- **Annotations:** Marginal notes and strike-throughs in the original document are captured and noted in the Markdown files.
- **Placeholders:** Unclear or illegible text is marked with `[?]` or specific notes about the difficulty of reading.

## Usage
When working with this directory:
1.  **Reference Scans:** Use the files in `Scans/` to verify transcriptions or transcribe new pages.
2.  **Update Transcripts:** New transcriptions should be added as individual `.md` files in the `Transkript/` folder and subsequently appended to `Transkript.txt`.
3.  **Contextual Research:** Refer to `Transkript.txt` for names of historical figures (teachers), geographical locations (Bickendorf, Seffern, Malbergweich), and historical events mentioned in the chronicle.
