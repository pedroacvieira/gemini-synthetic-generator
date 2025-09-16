#!/usr/bin/env python3
"""
Example usage of the Gemini Synthetic Generator Python API.

This script demonstrates how to use the GeminiSyntheticGenerator class
for various synthetic data generation tasks.
"""

import os
import sys
from pathlib import Path
from typing import List

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from generator import GeminiSyntheticGenerator


def setup_generator() -> GeminiSyntheticGenerator:
    """Initialize the Gemini Synthetic Generator."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable must be set. "
            "Get your API key from https://makersuite.google.com/app/apikey"
        )

    return GeminiSyntheticGenerator(api_key=api_key)


def example_object_insertion():
    """Example: Insert an object into a scene."""
    print("=== Object Insertion Example ===")

    generator = setup_generator()

    # Paths (adjust as needed)
    scene_path = "../data/input/scene.jpg"
    object_path = "../data/objects/ball.png"
    output_path = "../data/output/object_insertion_result.jpg"

    try:
        result = generator.insert_object(
            scene_path=scene_path,
            object_path=object_path,
            output_path=output_path,
            object_type="ball"  # Optional: auto-detected if None
        )
        print(f"✅ Object insertion completed: {result}")
    except Exception as e:
        print(f"❌ Object insertion failed: {e}")


def example_text_insertion():
    """Example: Insert text into a scene."""
    print("\n=== Text Insertion Example ===")

    generator = setup_generator()

    # Paths
    scene_path = "../data/input/person.jpg"
    output_path = "../data/output/text_insertion_result.jpg"
    text = "Team Alpha"

    try:
        result = generator.insert_text(
            scene_path=scene_path,
            text=text,
            output_path=output_path,
            target_area="shirt",
            style="casual"
        )
        print(f"✅ Text insertion completed: {result}")
    except Exception as e:
        print(f"❌ Text insertion failed: {e}")


def example_batch_processing():
    """Example: Batch process multiple images."""
    print("\n=== Batch Processing Example ===")

    generator = setup_generator()

    # Directories
    input_dir = "../data/input"
    output_dir = "../data/output"
    objects_dir = "../data/objects"
    texts_file = "../data/texts/sample_texts.txt"

    try:
        results = generator.batch_process(
            input_dir=input_dir,
            output_dir=output_dir,
            objects_dir=objects_dir,
            texts_file=texts_file,
            num_variations=2
        )
        print(f"✅ Batch processing completed: {len(results)} images generated")
        for result in results:
            print(f"  - {result}")
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")


def example_scene_analysis():
    """Example: Analyze a scene for insertion opportunities."""
    print("\n=== Scene Analysis Example ===")

    generator = setup_generator()

    # Image path
    image_path = "../data/input/scene.jpg"

    try:
        analysis = generator.analyze_scene(image_path)
        print("✅ Scene analysis completed:")
        print("=" * 50)
        print(analysis)
        print("=" * 50)
    except Exception as e:
        print(f"❌ Scene analysis failed: {e}")


def example_auto_detection():
    """Example: Demonstrate automatic object type detection."""
    print("\n=== Auto Object Detection Example ===")

    generator = setup_generator()

    # Test with different object images
    object_images = [
        "../data/objects/ball.png",
        "../data/objects/cap.png",
        "../data/objects/phone.png",
    ]

    for obj_path in object_images:
        if os.path.exists(obj_path):
            try:
                detected_type = generator.auto_detect_object_type(obj_path)
                print(f"✅ {obj_path}: Detected as '{detected_type}'")
            except Exception as e:
                print(f"❌ {obj_path}: Detection failed: {e}")
        else:
            print(f"⚠️  {obj_path}: File not found")


class SyntheticDataPipeline:
    """Example pipeline class for processing multiple images."""

    def __init__(self, api_key: str = None):
        self.generator = GeminiSyntheticGenerator(
            api_key=api_key or os.getenv("GEMINI_API_KEY")
        )

    def process_folder(
        self,
        input_folder: str,
        output_folder: str,
        operations: List[str] = None
    ) -> List[str]:
        """
        Process all images in a folder with specified operations.

        Args:
            input_folder: Folder containing input images
            output_folder: Folder for output images
            operations: List of operations ["object", "text", "both"]

        Returns:
            List of generated image paths
        """
        if operations is None:
            operations = ["both"]

        input_path = Path(input_folder)
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []

        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        images = [f for f in input_path.iterdir()
                 if f.suffix.lower() in image_extensions]

        for img_file in images:
            print(f"Processing: {img_file.name}")

            if "object" in operations or "both" in operations:
                # Object insertion example
                output_file = output_path / f"{img_file.stem}_with_object.jpg"
                try:
                    # This would need actual object files
                    print(f"  - Object insertion: {output_file}")
                    # result = self.generator.insert_object(...)
                    # results.append(result)
                except Exception as e:
                    print(f"  - Object insertion failed: {e}")

            if "text" in operations or "both" in operations:
                # Text insertion example
                output_file = output_path / f"{img_file.stem}_with_text.jpg"
                try:
                    result = self.generator.insert_text(
                        scene_path=str(img_file),
                        text="Sample Text",
                        output_path=str(output_file),
                        target_area="shirt"
                    )
                    results.append(result)
                    print(f"  - Text insertion: {output_file}")
                except Exception as e:
                    print(f"  - Text insertion failed: {e}")

        return results


def main():
    """Run all examples."""
    print("🚀 Gemini Synthetic Generator - Python API Examples")
    print("=" * 60)

    # Check if API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set!")
        print("Please set your Gemini API key:")
        print("export GEMINI_API_KEY='your-api-key-here'")
        return

    # Run examples
    try:
        # example_object_insertion()
        # example_text_insertion()
        # example_batch_processing()
        # example_scene_analysis()
        example_auto_detection()

        # Pipeline example
        print("\n=== Pipeline Example ===")
        pipeline = SyntheticDataPipeline()
        # results = pipeline.process_folder("../data/input", "../data/output", ["text"])
        print("Pipeline ready for processing")

    except Exception as e:
        print(f"❌ Example execution failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()