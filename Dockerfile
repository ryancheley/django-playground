# Multi-stage Dockerfile for Django application
# Stage 1: Builder - compile dependencies
FROM python:3.14-slim AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install uv for fast package installation
RUN pip install --upgrade pip uv

# Copy minimal files needed for installation
COPY pyproject.toml README.md /tmp/
# Create minimal package structure for installation
RUN mkdir -p /tmp/api /tmp/blsdata /tmp/candidates /tmp/companies /tmp/core /tmp/departments \
    /tmp/employees /tmp/pages /tmp/positions /tmp/questions /tmp/reports /tmp/resumes /tmp/theme && \
    touch /tmp/api/__init__.py /tmp/blsdata/__init__.py /tmp/candidates/__init__.py /tmp/companies/__init__.py /tmp/core/__init__.py /tmp/departments/__init__.py /tmp/employees/__init__.py /tmp/pages/__init__.py /tmp/positions/__init__.py /tmp/questions/__init__.py /tmp/reports/__init__.py /tmp/resumes/__init__.py /tmp/theme/__init__.py

# Install runtime dependencies only by default. Dev/debug tooling
# (django-debug-toolbar, django-extensions) MUST NOT ship in the production image (GH #1869).
# Local docker-compose opts in by building with --build-arg INSTALL_DEV=true.
ARG INSTALL_DEV=false
WORKDIR /tmp
RUN if [ "$INSTALL_DEV" = "true" ]; then \
        uv pip install --no-cache-dir -r pyproject.toml --extra dev; \
    else \
        uv pip install --no-cache-dir -r pyproject.toml; \
    fi

# Stage 2: Runtime - minimal production image
FROM python:3.14-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=core.settings

# Install runtime dependencies including Node.js for django-tailwind
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash django && \
    mkdir -p /app /app/staticfiles /app/static && \
    chown -R django:django /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=django:django . /app/

# Copy and set permissions for entrypoint script
COPY --chown=django:django docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run entrypoint script
CMD ["/app/docker-entrypoint.sh"]