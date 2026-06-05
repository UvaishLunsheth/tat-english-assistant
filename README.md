# TAT English Exam Preparation Assistant

## Overview
An end-to-end AI utility designed to extract, process, and generate exam-style questions directly from the Standard 12 English textbook. This project automates the creation of mock tests, chapter-wise questions, and revision notes perfectly aligned with the Teacher Aptitude Test (TAT) paper style.

## Architecture
- `data/`: Contains raw textbook PDFs and processed JSON units.
- `scripts/`: Core Python scripts for PDF OCR extraction, LLM question generation, and mock test assembly.
- `app/`: Streamlit interface for seamless interaction.
- `prompts/`: Template text files calibrated for generating specific TAT question formats (Q1 through Q5).

## Setup Instructions
1. Clone the repository.
2. Create and activate a conda environment: 
   `conda create -n tat-env python=3.10`
   `conda activate tat-env`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the extraction pipeline: `python scripts/extract_units.py`
5. Launch the app: `streamlit run app/main.py`