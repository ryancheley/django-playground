# --------------------------------------------------
# Core Utilities
# --------------------------------------------------

# Show list of available recipes when just is run without arguments
[group('utils')]
@_default:
    just --list

# --------------------------------------------------
# Docker Containers
# --------------------------------------------------

# Builds the Docker Images with optional arguments
[group('docker')]
@build *ARGS:
    docker compose {{ ARGS }} build

# Build Docker images for CI
[group('docker')]
@cibuild:
    just build

# Bring down Docker containers
[group('docker')]
@down *ARGS:
    docker compose down {{ ARGS }}

# View output from running containers
[group('docker')]
@logs *ARGS:
    docker compose logs {{ ARGS }}

# Restart all services
[group('docker')]
@restart *ARGS:
    docker compose restart {{ ARGS }}

# Start all services
[group('docker')]
@start *ARGS="--detach":
    docker compose up {{ ARGS }}

# Show status of running containers
[group('docker')]
@status:
    docker compose ps

# Stop all services
[group('docker')]
@stop:
    docker compose down

# Tail service logs
[group('docker')]
@tail:
    just logs --follow

# Start Docker containers
[group('docker')]
@up *ARGS:
    docker compose up {{ ARGS }}

# Drop into a bash shell in the Django container
[group('docker')]
@console:
    docker compose run --rm web /bin/bash

# Take container down and then bring back up with rebuild
[group('docker')]
@rebuild:
    just down && just up --build -d



# --------------------------------------------------
# Django Management
# --------------------------------------------------

# Create a Django superuser
[group('django')]
@createsuperuser USERNAME EMAIL:
    docker compose run --rm web uv run manage.py createsuperuser \
        --username={{ USERNAME }} \
        --email={{ EMAIL }}

# Collect static files
[group('django')]
@collectstatic *ARGS="--no-input":
    docker compose run --rm web uv run manage.py collectstatic {{ ARGS }}

# Run Django shell
[group('django')]
@shell *ARGS:
    docker compose run --rm web uv run manage.py shell {{ ARGS }}

# Run a Django management command
[group('django')]
@run ARGS:
    docker compose run --rm web uv run manage.py {{ ARGS }}


[group('tailwind')]
@css:
    npx tailwindcss build styles.css -o static/css/tailwind.css
