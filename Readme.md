# Repo Analyzer

## Overview

RepoAnalyzer is a Python script that utilizes the OpenAI GPT API to analyze a local Git repository. The script evaluates the repository files against a given set of specifications, provides a detailed report with a grade, and saves the report in Markdown format. It can also use OpenAI API compatible APIs.

## Features

- Analyzes all non-binary files in a local Git repository.
- Ignores files in `.git` directory and binary files.
- Uses the OpenAI GPT API for exhaustive analysis based on specified requirements.
- Generates a detailed Markdown report with individual file evaluations and an overall grade.
- Supports both OpenAI and local endpoints.
- Customizable with parameters for model, note, and endpoint.

## Requirements

- Python 3.x
- OpenAI Python Client Library
- A local Git repository for analysis

## Installation

1. **Clone the repository** (if applicable):
   ```bash
   git clone https://github.com/pedropachecog/repo-grader
   cd repo-grader
   ```

2. **Create a Python Virtual Environment and activate it**:

    Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   Linux:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```


2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The script can be run from the command line with various parameters. Here's the basic usage:

```bash
python analyze_repo.py --repo_path <path-to-repo> --note <note> [--model <model>] [--endpoint <endpoint>]
```

### Parameters

- `--repo_path` (required): Path to the local Git repository.
- `--note` (required): A note to be included at the top of the report. Usually meant to specify the model used in LMStudio.
- `--model` (optional): GPT model to use (default: GPT-4 turbo).
- `--endpoint` (optional): Custom OpenAI endpoint URL (default: http://localhost:1234/v1, which is the URL for LMStudio).

### Example

```bash
python analyze_repo.py --repo_path ../aws-challenge --note "Mistral-7B-Instruct-v0.3-Q8_0.gguf" --endpoint http://localhost:1234/v1
```

### Batch File

You can use the provided batch file `analyze.bat` for quick execution:

```batch
analyze [note]
```

It uses the http://localhost:1234/v1 endpoint (LMStudio) and `../aws-challenge` as repo.

## Environment Variables

- `OPENAI_API_KEY`: Set this environment variable with your OpenAI API key to authenticate the requests.

## Output

The script generates a Markdown report with the following structure:

- **Note:** Custom note provided via the `--note` parameter.
- **Grade:** Overall grade out of 100 based on the analysis.
- **Detailed Analysis:** Individual evaluations for each file.

The report is saved in the `reports` directory with the filename format `report-[note]-date-time.md`.

## Example Report

```
# Analysis Report

**Note:** GPT-4

**Grade:** 85.00/100

## Detailed Analysis

### path/to/file1.py
[Analysis content]

### path/to/file2.js
[Analysis content]
```