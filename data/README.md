# Data Directory Structure

This directory contains the data files used by the Gemini Synthetic Generator.

## Directory Structure

```
data/
├── input/          # Input scene images
├── output/         # Generated output images (auto-created)
├── objects/        # Object images for insertion
├── texts/          # Text files for batch processing
└── README.md       # This file
```

## Usage Examples

### Input Directory (`input/`)
Place your scene images here. Supported formats:
- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)

Example files:
- `person_standing.jpg` - Person in a field
- `sports_scene.jpg` - Sports environment
- `indoor_scene.png` - Indoor setting

### Objects Directory (`objects/`)
Place object images you want to insert into scenes. These should be:
- Clear, well-defined objects
- Preferably with transparent backgrounds (PNG)
- Good quality and resolution

Example files:
- `baseball.png` - Baseball object
- `basketball.png` - Basketball object
- `cap.png` - Baseball cap
- `phone.png` - Mobile phone

### Texts Directory (`texts/`)
Create text files with content for batch text insertion:

#### `sample_texts.txt`
```
Hello World
Sample Text
Team Alpha
Victory
Champion
```

### Output Directory (`output/`)
This directory will be automatically created and populated with:
- Generated images from object insertion
- Generated images from text insertion
- Batch processing results

File naming conventions:
- Single operations: User-specified filename
- Batch operations: `{original_name}_obj_{variation}.jpg` or `{original_name}_text_{variation}.jpg`

## Docker Volume Mounting

When using Docker, mount this entire `data/` directory:

```bash
docker run -v $(pwd)/data:/app/data gemini-synthetic:latest [command]
```

## File Requirements

### Input Images
- Minimum resolution: 512x512 pixels
- Maximum file size: 20MB
- Clear, well-lit scenes work best

### Object Images
- PNG format recommended for transparency
- Objects should be the main focus of the image
- Resolution: 256x256 to 1024x1024 pixels

### Text Files
- UTF-8 encoding
- One text entry per line
- Keep text short (1-10 words work best)
- Avoid special characters that might cause encoding issues

## Performance Tips

1. **Image Quality**: Higher resolution images produce better results but take longer to process
2. **Batch Size**: For large batches, process in chunks of 10-20 images
3. **Object Clarity**: Objects with clear edges and good contrast work best
4. **Text Length**: Shorter text strings integrate more naturally

## Troubleshooting

### Common Issues

1. **"File not found" errors**:
   - Check file paths are correct
   - Ensure files are in the mounted directory

2. **"Permission denied" errors**:
   - Run `sudo chown -R 1000:1000 data/` to fix permissions

3. **Poor insertion quality**:
   - Try higher resolution input images
   - Ensure object images have good contrast
   - Use shorter, simpler text strings

### Supported File Formats

| Type | Supported Formats |
|------|------------------|
| Input Images | JPEG, PNG, BMP |
| Object Images | PNG (recommended), JPEG, BMP |
| Text Files | TXT (UTF-8) |
| Output Images | JPEG, PNG (matches input format) |