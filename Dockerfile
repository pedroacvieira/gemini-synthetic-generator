FROM ubuntu:22.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (optimized for Gemini-only usage)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    curl \
    git \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project configuration
COPY pyproject.toml .
COPY README.md .

# Create source directory and copy source code
COPY src/ ./src/
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh

# Create virtual environment and install dependencies
RUN uv venv /app/.venv \
    && . /app/.venv/bin/activate \
    && uv pip install -e .

# Create data directories
RUN mkdir -p /app/data/{input,output,objects,texts} \
    && mkdir -p /app/models

# Create non-root user for security
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Activate virtual environment by default
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables for API keys (to be provided at runtime)
ENV GEMINI_API_KEY=""

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; from src.generator import GeminiSyntheticGenerator; sys.exit(0)"

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
CMD ["--help"]

# Example usage commands (commented):
# docker run -v $(pwd)/data:/app/data -e GEMINI_API_KEY=your_key_here gemini-synthetic:latest \
#   gemini-synthetic insert-object /app/data/scene.jpg /app/data/object.png /app/data/output.jpg
#
# docker run -v $(pwd)/data:/app/data -e GEMINI_API_KEY=your_key_here gemini-synthetic:latest \
#   gemini-synthetic insert-text /app/data/scene.jpg "Hello World" /app/data/output.jpg
#
# docker run -v $(pwd)/data:/app/data -e GEMINI_API_KEY=your_key_here gemini-synthetic:latest \
#   gemini-synthetic batch-process /app/data/input /app/data/output --num-variations 3