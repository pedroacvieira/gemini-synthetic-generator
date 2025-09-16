#!/bin/bash

# Quick Start Script for Gemini Synthetic Generator
set -e

echo "🚀 Gemini Synthetic Generator - Quick Start"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if nvidia-docker is available
if ! docker run --rm --gpus all nvidia/cuda:12.1-runtime-ubuntu22.04 nvidia-smi &> /dev/null; then
    print_warning "GPU support not detected. Running in CPU mode."
    GPU_FLAG=""
else
    print_status "GPU support detected."
    GPU_FLAG="--gpus all"
fi

# Check for API key
if [ -z "$GEMINI_API_KEY" ]; then
    print_warning "GEMINI_API_KEY not set."
    echo "Please set your API key:"
    echo "export GEMINI_API_KEY='your-api-key-here'"
    echo ""
    echo "Or create a .env file with:"
    echo "GEMINI_API_KEY=your-api-key-here"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build the Docker image
echo ""
print_info "Building Docker image..."
if docker build -t gemini-synthetic:latest . > /dev/null 2>&1; then
    print_status "Docker image built successfully."
else
    print_error "Failed to build Docker image."
    exit 1
fi

# Create data directories
echo ""
print_info "Setting up data directories..."
mkdir -p data/{input,output,objects,texts}
print_status "Data directories created."

# Check if there are any input images
if [ -z "$(ls -A data/input/ 2>/dev/null)" ]; then
    print_warning "No input images found in data/input/"
    echo "Please add some images to data/input/ and run again."
    echo ""
    echo "Example usage after adding images:"
    echo "1. Object insertion:"
    echo "   ./quick-start.sh object scene.jpg object.png output.jpg"
    echo ""
    echo "2. Text insertion:"
    echo "   ./quick-start.sh text scene.jpg 'Hello World' output.jpg"
    echo ""
    echo "3. Batch processing:"
    echo "   ./quick-start.sh batch"
    exit 0
fi

# Handle command line arguments
case "${1:-help}" in
    "help"|"--help"|"-h")
        echo ""
        print_info "Usage: $0 [command] [args...]"
        echo ""
        echo "Commands:"
        echo "  help              Show this help message"
        echo "  object <scene> <object> <output>  Insert object into scene"
        echo "  text <scene> <text> <output>      Insert text into scene"
        echo "  batch             Process all images in batch mode"
        echo "  analyze <image>   Analyze scene for insertion opportunities"
        echo "  shell            Open interactive shell in container"
        echo ""
        echo "Examples:"
        echo "  $0 object data/input/scene.jpg data/objects/ball.png data/output/result.jpg"
        echo "  $0 text data/input/person.jpg 'Team Alpha' data/output/result.jpg"
        echo "  $0 batch"
        echo "  $0 analyze data/input/scene.jpg"
        ;;

    "object")
        if [ $# -ne 4 ]; then
            print_error "Usage: $0 object <scene> <object> <output>"
            exit 1
        fi
        print_info "Running object insertion..."
        docker run --rm $GPU_FLAG \
            -v $(pwd)/data:/app/data \
            -e GEMINI_API_KEY="$GEMINI_API_KEY" \
            gemini-synthetic:latest \
            insert-object "/app/$2" "/app/$3" "/app/$4"
        ;;

    "text")
        if [ $# -ne 4 ]; then
            print_error "Usage: $0 text <scene> <text> <output>"
            exit 1
        fi
        print_info "Running text insertion..."
        docker run --rm $GPU_FLAG \
            -v $(pwd)/data:/app/data \
            -e GEMINI_API_KEY="$GEMINI_API_KEY" \
            gemini-synthetic:latest \
            insert-text "/app/$2" "$3" "/app/$4"
        ;;

    "batch")
        print_info "Running batch processing..."
        docker run --rm $GPU_FLAG \
            -v $(pwd)/data:/app/data \
            -e GEMINI_API_KEY="$GEMINI_API_KEY" \
            gemini-synthetic:latest \
            batch-process /app/data/input /app/data/output \
            --objects-dir /app/data/objects \
            --texts-file /app/data/texts/sample_texts.txt \
            --num-variations 2
        ;;

    "analyze")
        if [ $# -ne 2 ]; then
            print_error "Usage: $0 analyze <image>"
            exit 1
        fi
        print_info "Analyzing scene..."
        docker run --rm $GPU_FLAG \
            -v $(pwd)/data:/app/data \
            -e GEMINI_API_KEY="$GEMINI_API_KEY" \
            gemini-synthetic:latest \
            analyze-scene "/app/$2"
        ;;

    "shell")
        print_info "Opening interactive shell..."
        docker run --rm -it $GPU_FLAG \
            -v $(pwd)/data:/app/data \
            -e GEMINI_API_KEY="$GEMINI_API_KEY" \
            gemini-synthetic:latest \
            bash
        ;;

    *)
        print_error "Unknown command: $1"
        echo "Run '$0 help' for usage information."
        exit 1
        ;;
esac

print_status "Quick start completed!"
echo ""
print_info "Check data/output/ for generated images."