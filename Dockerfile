FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Use gunicorn to serve the Django app (invoked via Python module)
CMD ["python", "-m", "gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000"]