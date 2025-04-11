
# Build all containers defined in docker-compose.yml
build:
    docker-compose -f docker-compose.yml build

# Start containers in the background
up:
    docker-compose -f docker-compose.yml up -d

# Stop and remove containers
down:
    docker-compose -f docker-compose.yml down

# Apply any new database migrations
migrate:
    docker-compose -f docker-compose.yml run web python manage.py migrate

# Collect static files (make sure your Django settings are configured for collectstatic)
collectstatic:
    docker-compose -f docker-compose.yml run web python manage.py collectstatic --noinput

# Follow container logs for debugging
logs:
    docker-compose -f docker-compose.yml logs -f