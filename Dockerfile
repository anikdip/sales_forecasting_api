# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Command to run both FastAPI and Streamlit
CMD ["python", "main.py"]
