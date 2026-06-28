FROM python:3.13-slim

WORKDIR /app

# Install pip-tools
RUN pip install pip-tools

# Copy .in first, then compile, then install
COPY requirements.in .
RUN pip-compile requirements.in && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "wsgi:app"]