# Gemini Synthetic Data Generator

AI-powered synthetic data generation using Google's Gemini vision model for seamless object and text insertion into images.

**Author:** Pedro Vieira

---

## Overview

This tool leverages Google's Gemini 2.5 Flash model to create realistic synthetic datasets by intelligently inserting objects and text into existing images. Unlike traditional computer vision approaches, it uses advanced AI reasoning to understand scene context, lighting, and spatial relationships for photorealistic results.

## Key Features

- **Object Insertion**: Seamlessly place objects into scenes with automatic scaling, lighting, and perspective correction
- **Text Insertion**: Add text to clothing, signs, banners, and other surfaces with realistic styling and positioning
- **Scene Analysis**: AI-powered analysis to identify optimal insertion opportunities
- **Batch Processing**: Process multiple images efficiently with configurable variations
- **Auto-Detection**: Automatic object type detection for optimal placement strategies
- **CLI & Python API**: Both command-line interface and programmatic access

## Installation

### Prerequisites

- Python 3.10+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Install with uv (recommended)

```bash
git clone https://github.com/pedroacvieira/gemini-synthetic-generator.git
cd gemini-synthetic-generator
uv sync
```

### Install with pip

```bash
git clone https://github.com/pedroacvieira/gemini-synthetic-generator.git
cd gemini-synthetic-generator
pip install -e .
```

### Docker Installation

```bash
docker-compose up --build
```

## Quick Start

### 1. Set API Key

```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### 2. Scene Analysis

```bash
# Analyze a scene to verify that installations worked well
gemini-synthetic analyze-scene data/input/tennis_player.png
```

## Usage Examples

### Command Line Interface

```bash
# Object insertion with specific type
gemini-synthetic insert-object data/input/tennis_player.png data/objects/baseball.png data/output/result.png

# Text insertion with style
gemini-synthetic insert-text data/input/tennis_player.png "TEAM ALPHA" data/output/text_result.png --target-area shirt

# Scene analysis - Get detailed insertion recommendations
gemini-synthetic analyze-scene data/input/tennis_player.png

# Batch processing with 5 variations per image
gemini-synthetic batch-process data/input/ data/output/ --objects-dir data/objects/ --texts-file data/texts/sample_texts.txt --num-variations 5
```

### Python API

```python
from src.generator import GeminiSyntheticGenerator

# Initialize generator
generator = GeminiSyntheticGenerator(api_key="your-api-key")

# Object insertion
generator.insert_object(
    scene_path="scene.jpg",
    object_path="ball.png",
    output_path="result.jpg",
    object_type="ball"  # Optional: auto-detected if None
)

# Text insertion
generator.insert_text(
    scene_path="person.jpg",
    text="TEAM ALPHA",
    output_path="result.jpg",
    target_area="shirt",
    style="sporty"
)

# Scene analysis - Get detailed placement recommendations
analysis = generator.analyze_scene("data/input/tennis_player.png")
print(analysis)
# Returns detailed analysis with optimal placement zones, lighting considerations,
# and specific recommendations for object/text insertion opportunities

# Batch processing
results = generator.batch_process(
    input_dir="input/",
    output_dir="output/",
    objects_dir="objects/",
    texts_file="texts.txt",
    num_variations=3
)
```

## Project Structure

```
gemini-synthetic-generator/
├── src/
│   ├── generator.py      # Core generation logic
│   ├── main.py          # CLI interface
│   └── __init__.py
├── data/
│   ├── input/           # Input scene images
│   ├── objects/         # Objects for insertion
│   ├── texts/           # Text files
│   └── output/          # Generated results
├── examples/
│   └── python_api_example.py
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

## Supported Operations

### Object Insertion
- **Sports Equipment**: Balls, caps, equipment
- **Everyday Items**: Keys, phones, books
- **Accessories**: Glasses, jewelry, bags
- **Custom Objects**: Any PNG/JPEG with clean background

### Text Insertion
- **Clothing**: Shirts, jackets, hats
- **Signage**: Signs, banners, posters
- **Publications**: Books, magazines, displays
- **Surfaces**: Walls, ground, vehicles

### Supported Formats
- **Input**: JPEG, PNG, BMP
- **Output**: Same format as input with preserved quality
- **Objects**: PNG preferred for transparency support

## API Configuration

### Object Types
The system supports automatic detection, using Gemini vision to analyze object images

### Text Areas
- `shirt` - Clothing chest area
- `sign` - Sign surfaces with perspective correction
- `banner` - Flexible banner/poster surfaces
- `book` - Book covers and pages
- `wall` - Wall surfaces
- `ground` - Floor/pavement surfaces

### Text Styles
- `casual` - Handwritten-style, relaxed positioning
- `formal` - Clean, professional typography
- `sporty` - Bold, athletic lettering
- `artistic` - Creative, stylized text
- `vintage` - Retro styling with aged appearance

## Docker Support

Full containerization with development and production configurations:

```bash
# Development with mounted volumes
docker-compose up

# Production build
docker build -t gemini-synthetic-generator .
docker run -e GEMINI_API_KEY=your-key gemini-synthetic-generator
```

## Development

### Setup Development Environment

```bash
uv sync --dev
pre-commit install
```

### Code Quality

```bash
# Format code
black src/

# Lint code
ruff src/

# Run tests
pytest
```

## Limitations

- Requires internet connection for Gemini API
- Processing speed limited by API rate limits
- Generation quality varies with scene complexity
- Generation quality varies with context match between scene and object/text
- API costs scale with usage volume

## Examples Gallery

The `data/output/` directory contains example results:
- Object insertions: tennis_player_obj_*.png, car_obj_*.png
- Text insertions: tennis_player_text_*.png, musician_text_*.png

## API Key Setup

Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and set:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or pass directly to the CLI:
```bash
gemini-synthetic --api-key your-key insert-object ...
```
