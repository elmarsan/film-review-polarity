# Server

## Usage

### Requirements

- Define `DATABASE_URL` environment variable
    - (Option 1): Create .env file
    - (Option 2): Export variable in terminal session. E.g: `export DATABASE_URL=sqlite:///test.db`

1. Execute: `uvicorn app.main:app --reload`