# GlobalTrustHub Backend

[![Python CI](https://github.com/asifgondal786/globaltrusthubbackend/actions/workflows/python_ci.yml/badge.svg)](https://github.com/asifgondal786/globaltrusthubbackend/actions/workflows/python_ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

The core API and machine learning engine for **GlobalTrustHub**, facilitating secure user verification, trusted service connections, and AI-driven recommendations.

## 🏗️ Architecture

-   **API Framework**: FastAPI (High performance, easy documentation)
-   **Database**: PostgreSQL (Structured data for users, services, reviews)
-   **Caching**: Redis (Session management, rate limiting)
-   **AI/ML**: Scikit-Learn (Trust scoring models), Pandas
-   **Task Queue**: Celery (Background tasks like email sending)
-   **Authentication**: OAuth2 with JWT (Role-based access control)

## 🔑 Key Features

-   **Role-Based Auth**: Secure management for Students, Agents, and Admins.
-   **Trust Score Engine**: ML-based algorithm to calculate credibility scores.
-   **Real-time Chat**: WebSocket support for direct user-to-service communication.
-   **Payment Processing**: Integration endpoints for secure transactions.
-   **News Aggregation**: API to serve global migration and education news.

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   PostgreSQL installed and running
-   Redis installed and running

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/asifgondal786/globaltrusthubbackend.git
    cd globaltrusthubbackend
    ```

2.  **Create Virtual Environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Setup**:
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL=postgresql://user:password@localhost:5432/globaltrusthub
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5.  **Run the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    Access API documentation at `http://127.0.0.1:8000/api/docs`.

## 📦 Deployment

This project includes a `runtime.txt` and `Procfile` (if added) for easy deployment on **Railway** or **Heroku**.

**Railway Deployment:**
1.  Connect your GitHub repo to Railway.
2.  Add PostgreSQL and Redis plugins.
3.  Set environment variables in the Railway dashboard.
4.  Deploy!

## 🤝 Contributing

We welcome contributions! Please verify your changes with:
```bash
flake8 .
pytest
```
See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
