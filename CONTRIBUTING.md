# Contributing to GlobalTrustHub Backend

We welcome contributions to the API and logic layer of GlobalTrustHub!

## Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork**:
    ```bash
    git clone https://github.com/YOUR_USERNAME/globaltrusthubbackend.git
    cd globaltrusthubbackend
    ```
3.  **Set up Virtual Environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Development Standards

-   **Framework**: We use [FastAPI](https://fastapi.tiangolo.com/).
-   **Style**: Follow PEP 8. We encourage using type hints strictly.
-   **Testing**: Run tests using `pytest` before submitting.

## Pull Request Process

1.  Create a new branch for your feature.
2.  Keep changes focused and atomic.
3.  Ensure the application starts without errors (`uvicorn app.main:app`).
4.  Submit a PR to `main` with a clear description.

## Reporting Bugs

Please include full tracebacks and steps to reproduce in your issue reports.
