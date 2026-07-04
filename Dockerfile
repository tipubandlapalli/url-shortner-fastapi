FROM python:3.12.3

# Preven python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# print logs immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]