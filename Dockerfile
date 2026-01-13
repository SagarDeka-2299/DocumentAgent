FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Sync the dependencies
# Using --frozen to ensure we use exactly the versions in uv.lock
RUN uv sync --frozen

# Expose the application port
EXPOSE 8000

# Run the application using uv
CMD ["uv", "run", "main.py"]
