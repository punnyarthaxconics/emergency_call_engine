FROM python:3.11-slim

# Add uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Copy the current directory contents into the container at /app

COPY . /app

# Set the working directory

WORKDIR /app


# Install any needed packages specified in requirements.txt

RUN uv sync --frozen

# Set Python to be unbuffered
ENV PYTHONUNBUFFERED=1

# Run

CMD ["uv", "run", "main.py"]
