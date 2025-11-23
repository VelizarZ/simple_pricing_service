FROM python:3.11

WORKDIR /code

# Copy requirements
COPY requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app code
COPY app /code/app

# Run FastAPI application using FastAPI's built-in run command
# This automatically detects the FastAPI app instance in the file
# The --host and --port flags are automatically set to 0.0.0.0 and 8000
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
