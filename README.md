# Metadata Extractor

Metadata Extractor is a Python-based tool designed to extract and analyze metadata from various file types. It supports images, videos, audio files, and more, offering a user-friendly CLI and robust error handling.

## Features

- **Metadata Extraction**:
  - Extracts EXIF metadata from images, including GPS data.
  - Supports a wide range of file formats (images, videos, audio, documents, etc.).
- **GPS Data Parsing**:
  - Converts GPS coordinates into a human-readable format.
  - Handles mobile-specific and other edge cases.
- **User-Friendly CLI**:
  - Interactive interface with ASCII art and bold text.
  - Help section listing supported file types.
- **Output Management**:
  - Saves metadata to a timestamped file in a dedicated directory.
- **Error Handling**:
  - Catches and reports exceptions without crashing.

## Supported File Types

- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`
- Videos: `.mp4`, `.avi`, `.mkv`, `.mov`
- Audio: `.mp3`, `.wav`, `.flac`
- Documents: `.pdf`, `.docx`, `.xlsx`
- Archives: `.zip`, `.7z`, `.rar`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/metadata-extractor.git
   cd metadata-extractor
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:

   ```bash
   python metadata_extractor.py
   ```

2. Follow the on-screen instructions to select a file and extract its metadata.

3. Metadata will be saved in the `output` directory with a timestamped filename.

## Installation (.EXE file)

1. Go to the github repo, releases tap and downloaad the latest version:
   ```https://github.com/AlexiJemano/MetaHack/releases/tag/release```

## Example Output

```plaintext
File: example.jpg

Metadata:
- Camera Model: Canon EOS 80D
- Date Taken: 2024-12-29
- GPS Coordinates: 37.7749° N, 122.4194° W
```

## Project Structure

```
metadata-extractor/
├── metadata_extractor.py   # Main script
├── requirements.txt        # Python dependencies
├── output/                 # Directory for metadata output files
└── README.md               # Project documentation
```

## Dependencies

- Python 3.8+
- `pillow`
- `exifread`
- `magic`

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [Pillow](https://python-pillow.org/) for image processing.
- [ExifRead](https://pypi.org/project/ExifRead/) for EXIF metadata extraction.
- ASCII art generator tools for enhancing the CLI experience.

---

Feel free to report issues or suggest features by opening an issue on the GitHub repository.
