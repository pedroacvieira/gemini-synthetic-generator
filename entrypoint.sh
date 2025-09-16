#!/bin/bash

# Entrypoint script for Gemini Synthetic Generator Docker container
set -e

# Function to print usage
print_usage() {
    echo "=== Gemini Synthetic Generator Docker Container ==="
    echo ""
    echo "Environment Variables:"
    echo "  GEMINI_API_KEY: Required - Your Gemini API key"
    echo ""
    echo "Volume Mounts:"
    echo "  /app/data/input    - Input images directory"
    echo "  /app/data/output   - Output images directory"
    echo "  /app/data/objects  - Objects for insertion directory"
    echo "  /app/data/texts    - Text files directory"
    echo ""
    echo "Available Commands:"
    echo "  insert-object <scene> <object> <output> [options]"
    echo "  insert-text <scene> <text> <output> [options]"
    echo "  batch-process <input_dir> <output_dir> [options]"
    echo "  analyze-scene <image>"
    echo ""
    echo "Examples:"
    echo "  docker run -v \$(pwd)/data:/app/data -e GEMINI_API_KEY=\$GEMINI_API_KEY gemini-synthetic:latest \\"
    echo "    insert-object /app/data/input/scene.jpg /app/data/objects/ball.png /app/data/output/result.jpg"
    echo ""
    echo "  docker run -v \$(pwd)/data:/app/data -e GEMINI_API_KEY=\$GEMINI_API_KEY gemini-synthetic:latest \\"
    echo "    insert-text /app/data/input/person.jpg 'Hello World' /app/data/output/result.jpg --target-area shirt"
    echo ""
    echo "  docker run -v \$(pwd)/data:/app/data -e GEMINI_API_KEY=\$GEMINI_API_KEY gemini-synthetic:latest \\"
    echo "    batch-process /app/data/input /app/data/output --objects-dir /app/data/objects --num-variations 3"
}

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "ERROR: GEMINI_API_KEY environment variable is not set!"
    echo "Please provide your Gemini API key:"
    echo "  -e GEMINI_API_KEY=your_api_key_here"
    echo ""
    print_usage
    exit 1
fi

# Create required directories if they don't exist
mkdir -p /app/data/{input,output,objects,texts}

# Check if any arguments were passed
if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    print_usage
    echo ""
    echo "Run 'gemini-synthetic --help' for detailed command options"
    exit 0
fi

# Handle different command patterns
case "$1" in
    "insert-object"|"insert-text"|"batch-process"|"analyze-scene")
        # Direct CLI command
        exec python3 -m src.main "$@"
        ;;
    "gemini-synthetic")
        # CLI wrapper command
        shift
        exec python3 -m src.main "$@"
        ;;
    *)
        # Default to CLI with all arguments
        exec python3 -m src.main "$@"
        ;;
esac