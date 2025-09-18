# Gebruik een lichte Python image
FROM python:3.13-slim

# Zorg dat pip up-to-date is
RUN pip install --no-cache-dir --upgrade pip

# Werkdirectory in container
WORKDIR /app

# Kopieer requirements en installeer dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer projectbestanden
COPY . .

# Start Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
