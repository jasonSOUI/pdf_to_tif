
import os
import sys
import configparser
from pdf2image import convert_from_path
from PIL import Image

def get_poppler_path():
    """
    Determines the Poppler path by first checking config.ini,
    then falling back to a bundled relative path.
    """
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        # Assume the script is run from the project root
        script_dir = os.path.abspath(os.path.dirname(__file__))
        # Navigate up to the project root from core/
        script_dir = os.path.dirname(script_dir)

    # Default path (fallback)
    default_poppler_path = os.path.join(script_dir, "poppler-25.07.0", "Library", "bin")
    poppler_path = default_poppler_path

    # Prioritize reading from config.ini
    config = configparser.ConfigParser()
    config_file = os.path.join(script_dir, 'config.ini')

    if os.path.exists(config_file):
        try:
            config.read(config_file, encoding='utf-8')
            if 'Settings' in config and 'poppler_path' in config['Settings']:
                config_path = config['Settings']['poppler_path'].strip()
                if config_path:
                    poppler_path = config_path
        except Exception as e:
            print(f"Error reading config.ini: {e}")
            
    return poppler_path

def convert_pdf_to_tif(pdf_path: str, output_dir: str, compression: str, dpi: int = 300):
    """
    Converts a single PDF file to a multi-page TIF file.

    Args:
        pdf_path (str): The full path to the source PDF file.
        output_dir (str): The directory to save the TIF file.
        compression (str): The compression algorithm to use ('LZW' or 'CCITT T.6').
        dpi (int): The resolution for the conversion.

    Returns:
        tuple[bool, str]: A tuple containing a success flag and a message
                         (path to TIF on success, error message on failure).
    """
    POPPLER_PATH = get_poppler_path()
    if not os.path.isdir(POPPLER_PATH):
        return False, f"Poppler path not found or is not a directory: {POPPLER_PATH}"

    compression_map = {
        "CCITT T.6": "group4",
        "LZW": "tiff_lzw"
    }
    compression_algorithm = compression_map.get(compression, "group4")

    filename = os.path.basename(pdf_path)
    
    try:
        # Convert PDF to a list of PIL images
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            poppler_path=POPPLER_PATH,
            grayscale=True
        )

        if not images:
            return False, "PDF conversion resulted in no images. The file might be empty or corrupted."

        # Convert images to 1-bit black and white mode
        bw_images = [img.convert('1') for img in images]

        # Set up TIF filename and path
        tif_filename = os.path.splitext(filename)[0] + '.tif'
        tif_path = os.path.join(output_dir, tif_filename)

        # Save the first image and append the rest
        bw_images[0].save(
            tif_path,
            'TIFF',
            save_all=True,
            append_images=bw_images[1:],
            compression=compression_algorithm,
            dpi=(204, 196) # Standard fax DPI
        )
        
        return True, tif_path

    except Exception as e:
        error_message = f"An error occurred while converting {filename}: {e}"
        return False, error_message
