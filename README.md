# Product Image Tool

Streamlit-based product image workflow tool for scientific/ecommerce product rendering.

## Features

- Remove logos / supplier text / watermarks
- Generate different product angles
- Manual OpenAI API key input
- Multiple image size options
- Download generated images

## Setup

### Create virtual environment

```bash
python -m venv .venv
```

### Activate environment

Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run app

```bash
streamlit run app.py
```

## Security

API keys are NOT stored in the repository.

Use:
- sidebar API input
OR
- local `.env` file

## Notes

Designed for:
- scientific product catalogs
- ecommerce cleanup
- OEM/supplier debranding
- product rendering workflow testing
