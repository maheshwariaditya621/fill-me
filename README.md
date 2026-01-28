# Quick Commerce Survey Backend

A production-ready FastAPI backend for collecting survey responses.

## 1. Setup

### Prerequisites
- Python 3.10+
- MariaDB Server (Running)

### Installation
1.  Create a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    # source venv/bin/activate  # Mac/Linux
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 2. Database Configuration
1.  Open `database.py`.
2.  Update `SQLALCHEMY_DATABASE_URL` with your actual MariaDB credentials:
    ```python
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE_NAME"
    ```
    *Example: `mysql+pymysql://root:my-secret-pw@localhost:3306/survey_db`*
3.  Ensure the database (e.g., `survey_db`) exists in MariaDB. The API will create the tables automatically on first run.

## 3. Running the Server

Start the API server:
```bash
uvicorn main:app --reload
```

The server will run at `http://127.0.0.1:8000`.

## 4. Testing (Swagger UI)

1.  Open your browser to: **http://127.0.0.1:8000/docs**
2.  **POST /submit-response**:
    -   Click "Try it out".
    -   Paste the content of `sample_request.json` into the Request Body.
    -   Click "Execute".
3.  **GET /responses**:
    -   Click "Try it out" -> "Execute" to see stored data.
4.  **GET /export-excel**:
    -   Paste `http://127.0.0.1:8000/export-excel` in your browser URL bar to download the Excel report.

## 5. API Design Notes
-   **Validation**: Uses strict Pydantic Enums to reject invalid answers.
-   **Database**: Stores multi-select answers (Platforms, Categories) as JSON arrays.
-   **Export**: Generates a flattened `.xlsx` file ready for SPSS/Analysis.
