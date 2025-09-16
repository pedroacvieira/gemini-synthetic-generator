# Gemini Synthetic Generator - Docker Usage Guide

This guide explains how to use the Gemini Synthetic Generator as a containerized application with NVIDIA GPU support.

## Prerequisites

### System Requirements
- Docker Engine 20.10+ with BuildKit support
- NVIDIA Container Toolkit (nvidia-docker2)
- NVIDIA GPU with CUDA support
- Docker Compose (optional, for easier usage)

### Setup NVIDIA Docker Support

1. **Install NVIDIA Container Toolkit:**
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
     sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

   sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

2. **Verify GPU Access:**
   ```bash
   docker run --rm --gpus all nvidia/cuda:12.1-runtime-ubuntu22.04 nvidia-smi
   ```

## Quick Start

### 1. Clone and Build
```bash
git clone <repository-url>
cd gemini-synthetic-generator

# Build the Docker image
docker build -t gemini-synthetic:latest .
```

### 2. Set Up Your Data Structure
```
data/
├── input/          # Scene images to process
│   ├── scene1.jpg
│   └── scene2.jpg
├── output/         # Generated results (auto-created)
├── objects/        # Objects to insert (optional)
│   ├── ball.png
│   └── cap.png
└── texts/          # Text files (optional)
    └── texts.txt   # One text per line
```

### 3. Basic Usage
```bash
# Set your API key
export GEMINI_API_KEY="your-gemini-api-key-here"

# Object insertion
docker run --rm --gpus all \
  -v $(pwd)/data:/app/data \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  gemini-synthetic:latest \
  insert-object \
  /app/data/input/scene.jpg \
  /app/data/objects/ball.png \
  /app/data/output/result.jpg

# Text insertion
docker run --rm --gpus all \
  -v $(pwd)/data:/app/data \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  gemini-synthetic:latest \
  insert-text \
  /app/data/input/scene.jpg \
  "Hello World" \
  /app/data/output/result.jpg \
  --target-area shirt

# Batch processing
docker run --rm --gpus all \
  -v $(pwd)/data:/app/data \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  gemini-synthetic:latest \
  batch-process \
  /app/data/input \
  /app/data/output \
  --objects-dir /app/data/objects \
  --texts-file /app/data/texts/texts.txt \
  --num-variations 3

# Scene analysis
docker run --rm --gpus all \
  -v $(pwd)/data:/app/data \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  gemini-synthetic:latest \
  analyze-scene \
  /app/data/input/scene.jpg
```

## Docker Compose Usage

### 1. Create Environment File
Create a `.env` file in your project root:
```bash
echo "GEMINI_API_KEY=your-gemini-api-key-here" > .env
```

### 2. Run Services
```bash
# Show help
docker-compose run --rm gemini-synthetic

# Object insertion
docker-compose run --rm object-inserter

# Text insertion
docker-compose run --rm text-inserter

# Batch processing
docker-compose run --rm batch-processor

# Scene analysis
docker-compose run --rm scene-analyzer

# Custom command
docker-compose run --rm gemini-synthetic insert-object \
  /app/data/input/custom.jpg \
  /app/data/objects/custom.png \
  /app/data/output/custom_result.jpg
```

## API Integration

### Python API Usage in Container
```python
# Create a Python script and mount it into the container
# my_script.py

import os
from src.generator import GeminiSyntheticGenerator

def main():
    # Initialize generator
    generator = GeminiSyntheticGenerator(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    # Process images
    generator.insert_object(
        scene_path="/app/data/input/scene.jpg",
        object_path="/app/data/objects/object.png",
        output_path="/app/data/output/result.jpg"
    )

if __name__ == "__main__":
    main()
```

```bash
# Run custom script
docker run --rm --gpus all \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/my_script.py:/app/my_script.py \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  gemini-synthetic:latest \
  python3 my_script.py
```

## Volume Mounts

The container expects the following volume structure:

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./data/input` | `/app/data/input` | Input scene images |
| `./data/output` | `/app/data/output` | Generated output images |
| `./data/objects` | `/app/data/objects` | Object images for insertion |
| `./data/texts` | `/app/data/texts` | Text files for insertion |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Your Gemini API key |
| `NVIDIA_VISIBLE_DEVICES` | No | GPU devices to use (default: all) |
| `NVIDIA_DRIVER_CAPABILITIES` | No | Driver capabilities (default: compute,utility) |

## Performance Optimization

### GPU Memory Management
```bash
# Limit GPU memory usage
docker run --rm --gpus all \
  --memory="4g" \
  --shm-size="2g" \
  -v $(pwd)/data:/app/data \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  gemini-synthetic:latest [commands...]
```

### Parallel Processing
```bash
# Process multiple images in parallel using multiple containers
for image in data/input/*.jpg; do
  docker run --rm --gpus all -d \
    -v $(pwd)/data:/app/data \
    -e GEMINI_API_KEY=$GEMINI_API_KEY \
    gemini-synthetic:latest \
    insert-object "/app/data/input/$(basename $image)" \
    /app/data/objects/object.png \
    "/app/data/output/$(basename $image .jpg)_result.jpg" &
done
wait
```

## Troubleshooting

### Common Issues

1. **GPU Not Detected:**
   ```bash
   # Check GPU access
   docker run --rm --gpus all nvidia/cuda:12.1-runtime-ubuntu22.04 nvidia-smi
   ```

2. **Permission Denied:**
   ```bash
   # Fix volume permissions
   sudo chown -R 1000:1000 ./data
   ```

3. **API Key Issues:**
   ```bash
   # Verify API key is set
   docker run --rm -e GEMINI_API_KEY=$GEMINI_API_KEY gemini-synthetic:latest \
     python3 -c "import os; print('API Key set:', bool(os.getenv('GEMINI_API_KEY')))"
   ```

### Debugging
```bash
# Interactive shell for debugging
docker run --rm -it --gpus all \
  -v $(pwd)/data:/app/data \
  -e GEMINI_API_KEY=$GEMINI_API_KEY \
  gemini-synthetic:latest bash

# Check logs
docker logs <container_id>
```

## Production Deployment

### Multi-stage Build for Smaller Images
The current Dockerfile uses a single-stage build. For production, consider:

```dockerfile
# Multi-stage build example
FROM nvidia/cuda:12.1-runtime-ubuntu22.04 as base
# ... build dependencies

FROM nvidia/cuda:12.1-runtime-ubuntu22.04 as production
COPY --from=base /app/.venv /app/.venv
# ... copy only runtime requirements
```

### Resource Limits
```yaml
# docker-compose.yml production settings
services:
  gemini-synthetic:
    # ... other config
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Support

For issues related to:
- **Docker setup**: Check NVIDIA Container Toolkit installation
- **GPU access**: Verify CUDA drivers and nvidia-docker2
- **API errors**: Confirm Gemini API key and quota
- **Performance**: Monitor GPU memory usage with `nvidia-smi`