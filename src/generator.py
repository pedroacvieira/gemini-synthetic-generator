"""
Gemini-based synthetic data generator.
Uses Google's Gemini model for intelligent object and text insertion.
"""

import os
import logging
from pathlib import Path
from typing import Optional, List
from io import BytesIO

from google import genai
from PIL import Image
import random

logger = logging.getLogger(__name__)


class GeminiSyntheticGenerator:
    """Synthetic data generator using Gemini's image generation capabilities."""

    def __init__(
            self,
            api_key: Optional[str] = None,
            model_name: str = "gemini-2.5-flash-image-preview",
    ):
        """Initialize the Gemini synthetic generator.

        Args:
            api_key: Gemini API key (uses GEMINI_API_KEY env var if None)
            model_name: Gemini model to use for generation
        """
        # Setup Gemini client
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key required. Set GEMINI_API_KEY env var or pass api_key parameter."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name


    def auto_detect_object_type(self, object_path: str) -> str:
        """Auto-detect object type using Gemini visual analysis.

        Args:
            object_path: Path to object image

        Returns:
            Detected object type string
        """
        try:
            # Load the object image
            object_image = Image.open(object_path)

            # Create prompt for object identification
            prompt = """
            Analyze this image and identify the main object. Provide a single, concise object name that best describes what you see.

            Requirements:
            - Return only the object name (e.g., "baseball", "cap", "phone", "book")
            - Use simple, common terms
            - Focus on the most prominent object in the image
            - Keep it to 1-2 words maximum
            """

            # Get object identification from Gemini
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, object_image],
            )

            # Extract the object type from response
            object_type = "object"  # fallback
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    object_type = part.text.strip().lower()
                    # Clean up the response to get just the object name
                    object_type = object_type.split('\n')[0].strip()
                    break

            logger.info(f"Gemini detected object type: {object_type}")
            return object_type

        except Exception as e:
            logger.warning(f"Gemini object detection failed: {e}")
            return "object"

    @staticmethod
    def create_object_insertion_prompt(
            object_type: str,
            enhancement_level: str = "realistic"
    ) -> str:
        """Create optimized prompt for object insertion.

        Args:
            object_type: Type of object to insert
            enhancement_level: Level of realism (basic, realistic, photorealistic)

        Returns:
            Optimized prompt for Gemini
        """
        # Scene context will be analyzed by Gemini directly from the image

        # Enhancement specifications
        enhancements = {
            "basic": "natural placement and basic lighting matching",
            "realistic": "realistic lighting, shadows, perspective correction, and natural integration",
            "photorealistic": "photorealistic lighting analysis, accurate shadow casting, precise perspective transformation, color temperature matching, and seamless blending"
        }

        # Object-specific placement rules
        placement_rules = {
            "baseball": "in hands, being thrown/caught, or positioned naturally in a sports context",
            "cap": "properly fitted on a person's head with natural positioning",
            "glasses": "correctly positioned on a person's face",
            "book": "in hands, on surfaces, or in natural reading positions",
            "phone": "in hands or natural usage positions",
            "ball": "in hands, on ground, or in active play context"
        }

        object_guidance = placement_rules.get(object_type, "in the most semantically appropriate location")

        prompt = f"""
        Analyze the scene and seamlessly insert the {object_type} into the image.

        REQUIREMENTS:
        1. PLACEMENT: Position the {object_type} {object_guidance}
        2. REALISM: Apply {enhancements.get(enhancement_level, enhancements['realistic'])}
        3. SCALING: Size the object appropriately for the scene scale and perspective
        4. LIGHTING: Match ambient lighting, shadows, and reflections
        5. INTEGRATION: Ensure the object looks naturally part of the original scene

        TECHNICAL CONSIDERATIONS:
        - Analyze depth and perspective to position correctly in 3D space
        - Consider object occlusion and layering
        - Maintain consistent lighting direction and intensity
        - Apply appropriate surface reflections and material properties
        - Ensure edge blending is seamless and natural

        Generate the final composite image with the {object_type} naturally integrated.
        """

        return prompt

    @staticmethod
    def create_text_insertion_prompt(
            text: str,
            target_area: str,
            style: Optional[str] = None
    ) -> str:
        """Create optimized prompt for text insertion.

        Args:
            text: Text to insert
            target_area: Target area for insertion
            style: Optional style preference

        Returns:
            Optimized prompt for Gemini
        """
        # Scene context will be analyzed by Gemini directly from the image

        # Style specifications
        style_specs = {
            "casual": "casual, handwritten-style font with relaxed positioning",
            "formal": "clean, professional typography with precise alignment",
            "artistic": "creative, stylized text with artistic flair",
            "sporty": "bold, athletic-style lettering appropriate for sports context",
            "vintage": "retro-style typography with aged appearance"
        }

        style_guidance = style_specs.get(style, "natural, contextually appropriate styling")

        # Target area specifications
        area_specs = {
            "shirt": "on the chest/front area of clothing, following fabric contours and wrinkles",
            "sign": "on visible sign surfaces with appropriate perspective correction",
            "banner": "on banner or poster surfaces with natural draping",
            "book": "on book covers or visible pages",
            "wall": "on wall surfaces with appropriate perspective",
            "ground": "on ground surfaces like pavement or floor"
        }

        area_guidance = area_specs.get(target_area, f"on the {target_area} surface")

        prompt = f"""
        Insert the text "{text}" naturally into the image on the {target_area}.

        REQUIREMENTS:
        1. PLACEMENT: Position text {area_guidance}
        2. TYPOGRAPHY: Use {style_guidance}
        3. PERSPECTIVE: Apply correct perspective transformation to match surface angle
        4. INTEGRATION: Ensure text follows surface contours (wrinkles, curves, etc.)
        5. VISIBILITY: Choose colors that provide good contrast and readability
        6. REALISM: Make text appear as if originally part of the scene

        TECHNICAL CONSIDERATIONS:
        - Match lighting conditions (shadows, highlights on text)
        - Apply surface material properties (fabric texture, reflections)
        - Ensure text perspective matches viewing angle
        - Consider text size appropriate for distance and context
        - Apply subtle distortions for fabric/surface conformity

        Generate the image with "{text}" naturally integrated on the {target_area}.
        """

        return prompt

    def insert_object(
            self,
            scene_path: str,
            object_path: str,
            output_path: str,
            object_type: Optional[str] = None
    ) -> str:
        """Insert object into scene using Gemini generation.

        Args:
            scene_path: Path to scene/primary image
            object_path: Path to object image
            output_path: Output path for generated image
            object_type: Object type (auto-detected if None)

        Returns:
            Path to generated image
        """
        logger.info(f"Inserting object into scene using Gemini")

        # Load images
        scene_image = Image.open(scene_path)
        object_image = Image.open(object_path)

        # Auto-detect object type if not provided
        if not object_type:
            object_type = self.auto_detect_object_type(object_path)
            logger.info(f"Auto-detected object type: {object_type}")

        # Create optimized prompt
        prompt = self.create_object_insertion_prompt(object_type)

        try:
            # Generate with Gemini
            logger.info("Calling Gemini for image generation...")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, scene_image, object_image],
            )

            # Save generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    generated_image = Image.open(BytesIO(part.inline_data.data))
                    generated_image.save(output_path)
                    logger.info(f"Generated image saved to: {output_path}")
                    return output_path
                elif part.text is not None:
                    logger.info(f"Gemini response: {part.text}")

            raise Exception("No image generated in Gemini response")

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise

    def insert_text(
            self,
            scene_path: str,
            text: str,
            output_path: str,
            target_area: str = "shirt",
            style: Optional[str] = None
    ) -> str:
        """Insert text into scene using Gemini generation.

        Args:
            scene_path: Path to scene image
            text: Text to insert
            output_path: Output path for generated image
            target_area: Target area for text insertion
            style: Optional text style

        Returns:
            Path to generated image
        """
        logger.info(f"Inserting text '{text}' into {target_area}")

        # Load scene image
        scene_image = Image.open(scene_path)

        # Create optimized prompt
        prompt = self.create_text_insertion_prompt(text, target_area, style)

        try:
            # Generate with Gemini
            logger.info("Calling Gemini for text insertion...")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, scene_image],
            )

            # Save generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    generated_image = Image.open(BytesIO(part.inline_data.data))
                    generated_image.save(output_path)
                    logger.info(f"Generated image saved to: {output_path}")
                    return output_path
                elif part.text is not None:
                    logger.info(f"Gemini response: {part.text}")

            raise Exception("No image generated in Gemini response")

        except Exception as e:
            logger.error(f"Gemini text insertion failed: {e}")
            raise

    def analyze_scene(self, image_path: str) -> str:
        """Analyze scene to suggest optimal insertion opportunities.

        Args:
            image_path: Path to image for analysis

        Returns:
            Scene analysis and suggestions
        """
        logger.info(f"Analyzing scene: {image_path}")

        # Load image
        image = Image.open(image_path)

        # Scene context will be analyzed by Gemini directly from the image
        detection_context = ""

        prompt = f"""
        Analyze this image and provide detailed suggestions for synthetic data augmentation.

        {detection_context}

        Please provide:
        1. SCENE DESCRIPTION: What's in the image and the overall context
        2. OBJECT INSERTION OPPORTUNITIES: What objects could be naturally added and where
        3. TEXT INSERTION OPPORTUNITIES: Where text could be placed (shirts, signs, etc.)
        4. OPTIMAL PLACEMENT ZONES: Specific areas that would work best for insertions
        5. LIGHTING CONSIDERATIONS: How lighting affects insertion realism
        6. CHALLENGES: Potential difficulties for synthetic insertion

        Be specific about coordinates or regions where possible.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt, image],
            )

            analysis = ""
            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    analysis += part.text

            return analysis

        except Exception as e:
            logger.error(f"Scene analysis failed: {e}")
            raise

    def batch_process(
            self,
            input_dir: str,
            output_dir: str,
            objects_dir: Optional[str] = None,
            texts_file: Optional[str] = None,
            num_variations: int = 3
    ) -> List[str]:
        """Process multiple images in batch mode.

        Args:
            input_dir: Directory with input scene images
            output_dir: Output directory for generated images
            objects_dir: Optional directory with object images
            texts_file: Optional file with texts for insertion
            num_variations: Number of variations per input image

        Returns:
            List of generated image paths
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        # Get input images
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        scene_images = [
            f for f in input_path.iterdir()
            if f.suffix.lower() in image_extensions
        ]

        # Get object images if provided
        object_images = []
        if objects_dir:
            objects_path = Path(objects_dir)
            object_images = [
                f for f in objects_path.iterdir()
                if f.suffix.lower() in image_extensions
            ]

        # Load texts if provided
        texts = []
        if texts_file:
            with open(texts_file, 'r') as f:
                texts = [line.strip() for line in f if line.strip()]

        generated_images = []

        for i, scene_img in enumerate(scene_images):
            logger.info(f"Processing {scene_img.name} ({i + 1}/{len(scene_images)})")

            for var in range(num_variations):
                try:
                    if object_images and random.choice([True, False]):
                        # Object insertion
                        obj_img = random.choice(object_images)
                        output_file = output_path / f"{scene_img.stem}_obj_{var}{scene_img.suffix}"

                        result = self.insert_object(
                            scene_path=str(scene_img),
                            object_path=str(obj_img),
                            output_path=str(output_file)
                        )
                        generated_images.append(result)

                    elif texts:
                        # Text insertion
                        text = random.choice(texts)
                        target_area = random.choice(["shirt", "sign", "banner"])
                        output_file = output_path / f"{scene_img.stem}_text_{var}{scene_img.suffix}"

                        result = self.insert_text(
                            scene_path=str(scene_img),
                            text=text,
                            output_path=str(output_file),
                            target_area=target_area
                        )
                        generated_images.append(result)

                except Exception as e:
                    logger.error(f"Failed to process {scene_img.name} variation {var}: {e}")
                    continue

        logger.info(f"Batch processing completed. Generated {len(generated_images)} images")
        return generated_images