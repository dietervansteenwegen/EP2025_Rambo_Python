# Demo of a Python app image
#
# To build the image, use:
#   docker build -t <image-name> <path-to-Dockerfile>
#
# To run the image, use:
#  docker run [-ti] --rm <image-name>

# First stage, the build
FROM ghcr.io/astral-sh/uv:python3.13-bookworm as build

# Avoid interaction at the prompt
ENV DEBIAN_FRONTEND=noninteractive
# Ensure docker uses bash as a shell (and not dash or whatever)
SHELL ["/bin/bash", "-c"]
# Change directory to /app
WORKDIR /app

# Copy the repo
COPY . .

# Install the dependencies with uv
RUN uv sync --frozen --no-dev

# Second stage, keeping only the project and the virtualenv installed by uv
FROM python:3.13-slim as final

# Change directory to /app
WORKDIR /app

# Copy the repository parts from the previous image
COPY --from=build  /app/  /app
RUN mkdir log

ENTRYPOINT ["/app/.venv/bin/python", "/app/main.py"]
