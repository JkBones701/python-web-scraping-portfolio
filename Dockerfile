FROM python:3.10-slim

WORKDIR /app

# Install dependencies first (leverages Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY validator.py .
COPY scraped_quotes.csv .

# Run validation on container start
CMD ["python", "validator.py", "scraped_quotes.csv"]