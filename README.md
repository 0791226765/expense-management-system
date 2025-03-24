# Expense Management System

This project is an expenses management system that consists of streamlit frontend application and a FastAPI backend server.

## Project structure

- **frontend/**: Contains the streamlit application code.
- **backend/**: Contains the FastAPI backend server code.
- **tests/**: Contains the test cases for both frontend and backend.
- **requirements.txt**: Lists the required Python packages.
- **README.md**: Provides an overview and instructions for the project.

## Setup instructions
1. **Clone the repository**:
    ```bash
   git clone https://github.com/yourusername/expense-management-system
   cd expense-management-system
    ```
2. **Install dependencies**:
    ```commandline
   pip install -r requirements.txt
    ```
3. **Run the FastAPI server**:
    ```commandline
   uvicorn server.server:app --reload
   ```
4. **Run the streamlit app**:
    ```commandline
   streamlit run frontend/app.py
   ```