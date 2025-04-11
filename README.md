# 🛒 Python Ecommerce

A modern **e-commerce** web application built with [Django](https://www.djangoproject.com/) and powered by Docker Compose. This project leverages multiple services for a robust, production-ready environment:

- **Web (Django + Gunicorn):** Serves your application.
- **PostgreSQL DB:** Manages your data.
- **MinIO:** Object storage for media files (S3-compatible).
- **Nginx:** Reverse proxy for serving static files and load balancing.

---

## 🚀 Features

- **Dockerized Environment:** Easily run and manage all services with Docker Compose.
- **Django Admin:** Custom admin views including product reporting.
- **REST API:** Endpoints for products and categories.
- **Media Storage:** Integrated with MinIO for storing images and files.
- **Nginx:** Handles static files and request routing.

---

## 🛠️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## ⚙️ Getting Started

1. **Clone the Repository**

   ```bash
   git clone https://github.com/RONEW2J/PythonEcommerce.git
   cd PythonEcommerce
   ```

2. **Configure Environment Variables**

   Create a `.env.prod` file in the project root with the following content (update with your own secrets):

   ```dotenv
   DJANGO_SECRET_KEY=your_production_secret_key
   DJANGO_DEBUG=False

   # PostgreSQL settings
   POSTGRES_DB=pythonecommerce
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=db_pass25
   DATABASE_URL=postgres://postgres:db_pass25@db:5432/pythonecommerce

   # MinIO settings
   MINIO_ACCESS_KEY=your_minio_access_key
   MINIO_SECRET_KEY=your_minio_secret_key
   MINIO_BUCKET_NAME=your_bucket_name
   ```

3. **Build and Run the Containers**

   Use Docker Compose to build and start all services:

   ```bash
   docker-compose up -d --build
   ```

4. **Run Migrations and Collect Static Files**

   Inside the container, run migrations and collect static files:

   ```bash
   docker-compose run web python manage.py migrate
   docker-compose run web python manage.py collectstatic --noinput
   ```

5. **Access the Application**

   - **Site:** [http://localhost:8000](http://localhost:8000)
   - **Admin:** [http://localhost:8000/admin](http://localhost:8000/admin)  
     *(Login using your Django superuser credentials.)*

---

## 📝 Docker Compose Overview

Below is a snippet of the `docker-compose.yml` to give you an idea of the services configured:

```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000
    env_file: .env.prod
    depends_on:
      - db
      - minio
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"

  db:
    image: postgres:15
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_DB: pythonecommerce
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: db_pass25
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  minio:
    image: minio/minio:latest
    command: server /data
    environment:
      MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY}
      MINIO_SECRET_KEY: ${MINIO_SECRET_KEY}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - static_volume:/app/staticfiles:ro
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro

volumes:
  postgres_data:
  static_volume:
  media_volume:
  minio_data:
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or create pull requests for improvements.

---

Happy coding! 😃
