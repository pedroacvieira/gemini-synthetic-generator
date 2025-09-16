"""
Gemini-based synthetic data generator CLI.
Uses Gemini's native image generation for object and text insertion.
"""

import os
import typer
from pathlib import Path
from typing import Optional
import logging

from .generator import GeminiSyntheticGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = typer.Typer(
    help="Gemini-powered synthetic data generator for object and text insertion"
)

api_key_env = os.getenv("GEMINI_API_KEY")
if not api_key_env:
    logger.warning("GEMINI_API_KEY environment variable not set. API key must be provided.")


@app.command()
def insert_object(
        primary_image: Path = typer.Argument(..., help="Path to primary/scene image"),
        object_image: Path = typer.Argument(..., help="Path to object to insert"),
        output_path: Path = typer.Argument(..., help="Path for output image"),
        object_type: Optional[str] = typer.Option(
            None, help="Object type (auto-detected if not specified)"
        ),
        api_key: Optional[str] = typer.Option(
            None, help="Gemini API key (or set GEMINI_API_KEY env var)"
        ),
):
    """Insert an object into a scene using Gemini's image generation."""
    logger.info(f"Starting object insertion with Gemini")

    # Validate inputs
    if not primary_image.exists():
        raise typer.BadParameter(f"Primary image not found: {primary_image}")
    if not object_image.exists():
        raise typer.BadParameter(f"Object image not found: {object_image}")

    # Initialize generator
    generator = GeminiSyntheticGenerator(api_key=api_key)

    try:
        # Generate synthetic image
        result_path = generator.insert_object(
            scene_path=str(primary_image),
            object_path=str(object_image),
            output_path=str(output_path),
            object_type=object_type,
        )

        logger.info(f"Object insertion completed. Saved to {result_path}")

    except Exception as e:
        logger.error(f"Object insertion failed: {e}")
        raise typer.Exit(1)


@app.command()
def insert_text(
        primary_image: Path = typer.Argument(..., help="Path to primary image"),
        text: str = typer.Argument(..., help="Text to insert"),
        output_path: Path = typer.Argument(..., help="Path for output image"),
        target_area: str = typer.Option("shirt", help="Target area (shirt, sign, etc.)"),
        style: Optional[str] = typer.Option(
            None, help="Text style preference (casual, formal, etc.)"
        ),
        api_key: Optional[str] = typer.Option(
            None, help="Gemini API key (or set GEMINI_API_KEY env var)"
        ),
):
    """Insert text into an image using Gemini's image generation."""
    logger.info(f"Starting text insertion: '{text}' on {target_area}")

    # Validate input
    if not primary_image.exists():
        raise typer.BadParameter(f"Primary image not found: {primary_image}")

    # Initialize generator
    generator = GeminiSyntheticGenerator(api_key=api_key)

    try:
        # Generate synthetic image with text
        result_path = generator.insert_text(
            scene_path=str(primary_image),
            text=text,
            output_path=str(output_path),
            target_area=target_area,
            style=style,
        )

        logger.info(f"Text insertion completed. Saved to {result_path}")

    except Exception as e:
        logger.error(f"Text insertion failed: {e}")
        raise typer.Exit(1)


@app.command()
def batch_process(
        input_dir: Path = typer.Argument(..., help="Directory with input images"),
        output_dir: Path = typer.Argument(..., help="Output directory"),
        objects_dir: Optional[Path] = typer.Option(
            None, help="Directory with object images for insertion"
        ),
        texts_file: Optional[Path] = typer.Option(
            None, help="Text file with texts to insert (one per line)"
        ),
        num_variations: int = typer.Option(3, help="Number of variations per image"),
        api_key: Optional[str] = typer.Option(
            None, help="Gemini API key (or set GEMINI_API_KEY env var)"
        ),
):
    """Process multiple images in batch mode."""
    logger.info(f"Starting batch processing: {input_dir} -> {output_dir}")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize generator
    generator = GeminiSyntheticGenerator(api_key=api_key)

    try:
        # Run batch processing
        results = generator.batch_process(
            input_dir=str(input_dir),
            output_dir=str(output_dir),
            objects_dir=str(objects_dir) if objects_dir else None,
            texts_file=str(texts_file) if texts_file else None,
            num_variations=num_variations,
        )

        logger.info(f"Batch processing completed. Generated {len(results)} images")

    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        raise typer.Exit(1)


@app.command()
def analyze_scene(
        image_path: Path = typer.Argument(..., help="Path to image for analysis"),
        api_key: Optional[str] = typer.Option(
            None, help="Gemini API key (or set GEMINI_API_KEY env var)"
        ),
):
    """Analyze a scene to suggest optimal object/text insertion opportunities."""
    logger.info(f"Analyzing scene: {image_path}")

    if not image_path.exists():
        raise typer.BadParameter(f"Image not found: {image_path}")

    # Initialize generator
    generator = GeminiSyntheticGenerator(api_key=api_key)

    try:
        # Analyze scene
        analysis = generator.analyze_scene(str(image_path))

        print("\n" + "=" * 50)
        print("SCENE ANALYSIS RESULTS")
        print("=" * 50)
        print(analysis)

    except Exception as e:
        logger.error(f"Scene analysis failed: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()