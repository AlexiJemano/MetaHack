from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from prettytable import PrettyTable
import os
import sys
import datetime
from colorama import Fore, Style
import time
import magic

def save_to_file(metadata_table, gps_data=None, gps_url=None):
    """Save metadata to a file"""
    try:
        # Create output directory if it doesn't exist
        output_dir = "metadata_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"metadata_{timestamp}.txt")
        
        with open(filename, 'w') as f:
            if gps_data:
                f.write("GPS Information:\n")
                f.write("-" * 50 + "\n")
                for key, value in gps_data.items():
                    f.write(f"{key.capitalize()}: {value:.6f}°\n")
                
                if gps_url:
                    f.write(f"\nGoogle Maps Link:\n{gps_url}\n")
                f.write("\n")
            
            f.write("EXIF Metadata:\n")
            f.write("-" * 50 + "\n")
            f.write(metadata_table.get_string())
            
        print(f"\nMetadata saved to: {filename}")
        return True
    except Exception as e:
        print(f"Error saving metadata: {str(e)}")
        return False

def get_gps_refs_and_coords(img):
    """Extract GPS data from image's getexif() output, including mobile formats"""
    try:
        exif = img._getexif()
        if not exif:
            return None
        
        for key, value in exif.items():
            tag_name = TAGS.get(key, key)
            if tag_name == 'GPSInfo':
                # If it's just a number (mobile phone format), get the real GPS data
                if isinstance(value, int):
                    try:
                        # Get the actual GPS data from the image
                        exif_data = img.getexif()
                        if hasattr(exif_data, '_get_ifd'):
                            gps_info = exif_data._get_ifd(0x8825)  # GPS IFD
                            if gps_info:
                                return parse_gps_data(gps_info)
                    except Exception as e:
                        print(f"Error extracting mobile GPS data: {str(e)}")
                else:
                    return parse_gps_data(value)
    except Exception as e:
        print(f"Error reading EXIF data: {str(e)}")
    return None

def parse_gps_data(gps_info):
    """Parse GPS data from various formats"""
    try:
        gps_data = {}
        
        # Get latitude
        if 2 in gps_info:
            lat = gps_info[2]
            lat_ref = gps_info.get(1, 'N')
            
            if isinstance(lat, tuple):
                lat = lat[0]
            elif isinstance(lat, bytes):
                lat = lat.decode('utf-8')
                
            gps_data['latitude'] = convert_to_decimal(lat)
            if lat_ref == 'S':
                gps_data['latitude'] = -gps_data['latitude']
        
        # Get longitude
        if 4 in gps_info:
            lon = gps_info[4]
            lon_ref = gps_info.get(3, 'E')
            
            if isinstance(lon, tuple):
                lon = lon[0]
            elif isinstance(lon, bytes):
                lon = lon.decode('utf-8')
                
            gps_data['longitude'] = convert_to_decimal(lon)
            if lon_ref == 'W':
                gps_data['longitude'] = -gps_data['longitude']
        
        return gps_data
    except Exception as e:
        print(f"Error parsing GPS data: {str(e)}")
        return None

def convert_to_decimal(value):
    """Convert GPS coordinates to decimal format"""
    if isinstance(value, tuple):
        # Handle traditional degree/minute/second format
        d = float(value[0][0]) / float(value[0][1])
        m = float(value[1][0]) / float(value[1][1])
        s = float(value[2][0]) / float(value[2][1])
        return d + (m / 60.0) + (s / 3600.0)
    elif isinstance(value, str):
        # Handle string format
        try:
            return float(value)
        except ValueError:
            parts = value.split(',')
            if len(parts) == 3:
                d, m, s = map(float, parts)
                return d + (m / 60.0) + (s / 3600.0)
    elif isinstance(value, (int, float)):
        return float(value)
    return 0.0

class IntroClass:
    def __init__(self):
        ascii_art = """
          ____                                          ,--,                                
        ,'  , `.             ___                      ,--.'|                           ,-.  
     ,-+-,.' _ |           ,--.'|_                 ,--,  | :                       ,--/ /|  
  ,-+-. ;   , ||           |  | :,'             ,---.'|  : '                     ,--. :/ |  
 ,--.'|'   |  ;|           :  : ' :             |   | : _' |                     :  : ' /   
|   |  ,', |  ':  ,---.  .;__,'  /    ,--.--.   :   : |.'  |  ,--.--.     ,---.  |  '  /    
|   | /  | |  || /     \ |  |   |    /       \  |   ' '  ; : /       \   /     \ '  |  :    
'   | :  | :  |,/    /  |:__,'| :   .--.  .-. | '   |  .'. |.--.  .-. | /    / ' |  |   \   
;   . |  ; |--'.    ' / |  '  : |__  \__\/: . . |   | :  | ' \__\/: . ..    ' /  '  : |. \  
|   : |  | ,   '   ;   /|  |  | '.'| ," .--.; | '   : |  : ; ," .--.; |'   ; :__ |  | ' \ \ 
|   : '  |/    '   |  / |  ;  :    ;/  /  ,.  | |   | '  ,/ /  /  ,.  |'   | '.'|'  : |--'  
;   | |`-'     |   :    |  |  ,   /;  :   .'   \;   : ;--' ;  :   .'   \   :    :;  |,'     
|   ;/          \   \  /    ---`-' |  ,     .-./|   ,/     |  ,     .-./\   \  / '--'       
'---'            `----'             `--`---'    '---'       `--`---'     `----'             
        """

        print(ascii_art)
        BOLD = '\033[1m'
        RESET = '\033[0m'

        print(f"{BOLD}Welcome to MetaHack!{RESET}")
        print(f"{BOLD}This is a simple hacking tool to view metadata of files{RESET}")
        print(f"{BOLD}To see currently supported files, type 'help_supported_files'{RESET}")
        print(f"{BOLD}WARNING: Transfering files via apps like: Telegram,Viber,Drive,etc. will cause the file to lose its EXIF data.{RESET}")
        print(f"{BOLD}To start using 'MetaHack', type the file address of the wanted file, e.g: 'C:/Users/Administrator/Desktop/image.png'{RESET}")
        file_address = input("Enter the file address: ")
        
        self.file_address = file_address.strip('"\'').strip()
        self.file_address = os.path.normpath(self.file_address)
        
        if self.file_address.lower() == "help_supported_files":
            HelpClass()
        else:
            try:
                MainClass(self.file_address)
            except FileNotFoundError:
                print(f"Error: File '{self.file_address}' not found.")
            except Image.UnidentifiedImageError:
                print(f"Error: File '{self.file_address}' is not a valid image file.")
            except Exception as e:
                print(f"Error: {str(e)}")
            
            # Ask if user wants to continue
            self.continue_prompt()
    
    def continue_prompt(self):
        while True:
            choice = input("\nDo you want to analyze another file? (y/n): ").lower()
            if choice == 'y':
                IntroClass()
                break
            elif choice == 'n':
                print("Thank you for using MetaHack! Goodbye!")
                sys.exit()
            else:
                print("Please enter 'y' for yes or 'n' for no.")

class HelpClass:
    def __init__(self):
        print("\nCurrently supported files:")
        self.supported_files()
        
        while True:
            choice = input("\nType 'back' to return to main menu: ").lower()
            if choice == 'back':
                IntroClass()
                break
            else:
                print("Please type 'back' to return to the main menu.")

    def supported_files(self):
        print("\n### Image and Graphics Files")
        print("- JPEG/JPG")
        print("- PNG")
        print("- TIFF")
        print("- GIF")
        print("- BMP")
        print("- RAW (e.g., CR2, NEF, ARW, ORF, DNG)")
        print("- HEIC/HEIF")
        print("- ICO")
        print("- WEBP")
        print("- SVG")
        print("- EPS")
        print("- PSD")
        print("- AI")

        # Video Files
        print("\n### Video Files")
        print("- MP4")
        print("- AVI")
        print("- MKV")
        print("- MOV")
        print("- WMV")
        print("- FLV")
        print("- MPEG/MPG")
        print("- 3GP")
        print("- OGV")
        print("- WEBM")

        # Audio Files
        print("\n### Audio Files")
        print("- MP3")
        print("- WAV")
        print("- FLAC")
        print("- AAC")
        print("- OGG")
        print("- M4A")
        print("- AIFF")
        print("- WMA")
        print("- ALAC")
        print("- MID/MIDI")

        # Document Files
        print("\n### Document Files")
        print("- PDF")
        print("- DOC/DOCX (Microsoft Word)")
        print("- XLS/XLSX (Microsoft Excel)")
        print("- PPT/PPTX (Microsoft PowerPoint)")
        print("- ODT (OpenDocument Text)")
        print("- ODS (OpenDocument Spreadsheet)")
        print("- ODP (OpenDocument Presentation)")
        print("- RTF")
        print("- TXT (limited metadata via filesystem or comments)")

        # Web Files
        print("\n### Web Files")
        print("- HTML")
        print("- CSS")
        print("- JS")
        print("- PHP")
        print("- XML")
        print("- JSON")
        print("- YAML")

        # Compressed and Archive Files
        print("\n### Compressed and Archive Files")
        print("- ZIP")
        print("- 7Z")
        print("- RAR")
        print("- TAR")
        print("- GZ")
        print("- ISO")

        # 3D Modeling and CAD Files
        print("\n### 3D Modeling and CAD Files")
        print("- OBJ")
        print("- STL")
        print("- FBX")
        print("- BLEND")
        print("- DWG/DXF")
        print("- GLTF/GLB")
        print("- PLY")
        print("- 3DS")
        print("- VRML/WRL")

        # Font Files
        print("\n### Font Files")
        print("- TTF")
        print("- OTF")
        print("- WOFF/WOFF2")

        # Programming and Data Files
        print("\n### Programming and Data Files")
        print("- CSV")
        print("- TSV")
        print("- JSON")
        print("- XML")
        print("- HDF5")
        print("- MAT")
        print("- SQL")
        print("- PY")
        print("- JAVA")
        print("- JS")
        print("- C/C++ (.c, .cpp)")
        print("- R")
        print("- GO")
        print("- YAML")
        print("- INI")

        # Geospatial Files
        print("\n### Geospatial Files")
        print("- KML/KMZ")
        print("- GeoTIFF")
        print("- Shapefiles (.shp, .shx, .dbf)")
        print("- GPX")
        print("- DEM")
        print("- LAS/LAZ")

        # System and Application Files
        print("\n### System and Application Files")
        print("- EXE/DLL")
        print("- ISO")
        print("- DMG")
        print("- LOG")
        print("- CFG")

        # E-Book Files
        print("\n### E-Book Files")
        print("- EPUB")
        print("- MOBI")
        print("- AZW")
        print("- FB2")

        # Gaming Files
        print("\n### Gaming Files")
        print("- SAVE Files")
        print("- ROM Files")
        print("- PKG (PlayStation)")
        print("- NDS (Nintendo DS)")
        print("- NES")

        # Blockchain and Cryptocurrency Files
        print("\n### Blockchain and Cryptocurrency Files")
        print("- JSON-LD")
        print("- Wallet Files (.dat)")

        # Backup and Disk Image Files
        print("\n### Backup and Disk Image Files")
        print("- VHD/VHDX")
        print("- QCOW2")
        print("- DMG")

        # Specialized Files
        print("\n### Specialized Files")
        print("- ICS (iCalendar)")
        print("- VCF (vCard)")
        print("- SPSS (.sav)")
        print("- SAS (.sas7bdat)")
        print("- DICOM (medical imaging)")
        print("- FIT (fitness tracking data)")
        pass

class MainClass:
    def __init__(self, file_address):
        try:
            if not os.path.exists(file_address):
                print(f"Error: File '{file_address}' does not exist.")
                return

            # Check if file is an image
            mime_type = magic.from_file(file_address, mime=True)
            if mime_type.startswith('image/'):
                # Use existing image code unchanged
                my_image = Image.open(file_address)
                img_exif_data = my_image.getexif()
                
                # Get GPS data first
                gps_data = get_gps_refs_and_coords(my_image)
                gps_url = None
                
                if gps_data:
                    print("\nGPS Information:")
                    gps_table = PrettyTable()
                    gps_table.field_names = ["Information", "Value"]
                    for key, value in gps_data.items():
                        gps_table.add_row([key.capitalize(), f"{value:.6f}°"])
                    print(gps_table)
                    
                    # Generate Google Maps link
                    gps_url = f"https://www.google.com/maps?q={gps_data['latitude']},{gps_data['longitude']}"
                    print(f"\nView location on Google Maps:")
                    print(gps_url)
                
                # Show other EXIF data
                print("\nOther EXIF Data:")
                table = PrettyTable()
                table.field_names = ["MetaTags", "Values"]
                
                if not img_exif_data:
                    print("No additional EXIF data found in the image.")
                    return
                    
                for id in img_exif_data:
                    if id != 34853:  # Skip raw GPSInfo tag
                        try:
                            tag_name = TAGS.get(id, id)
                            data = img_exif_data.get(id)
                            if isinstance(data, bytes):
                                try:
                                    data = data.decode()
                                except UnicodeDecodeError:
                                    data = str(data)
                            table.add_row([tag_name, data])
                        except Exception as e:
                            continue
                
                print(table)
                
                # Ask if user wants to save the data
                while True:
                    save_choice = input("\nWould you like to save this metadata to a file? (y/n): ").lower()
                    if save_choice == 'y':
                        print("\nSaving metadata to a file (metadata_output/metadata_<timestamp>.txt)...")
                        save_to_file(table, gps_data, gps_url)
                        print("Metadata saved successfully.")
                        break
                    elif save_choice == 'n':
                        break
                    else:
                        print("Please enter 'y' for yes or 'n' for no.")

            else:
                # For non-image files, get all available metadata
                print("\nFile Metadata:")
                table = PrettyTable()
                table.field_names = ["MetaTags", "Values"]
                
                # Get all metadata we can find using python-magic
                file_info = magic.Magic(mime=True, keep_going=True)
                metadata = file_info.from_file(file_address)
                
                # Get file attributes
                file_stats = os.stat(file_address)
                
                # Add whatever metadata we found to table
                for key, value in vars(file_stats).items():
                    if not key.startswith('_'):  # Skip private attributes
                        table.add_row([key, str(value)])
                        
                print(table)
                
                # Ask if user wants to save the data
                while True:
                    save_choice = input("\nWould you like to save this metadata to a file? (y/n): ").lower()
                    if save_choice == 'y':
                        print("\nSaving metadata to a file (metadata_output/metadata_<timestamp>.txt)...")
                        save_to_file(table)
                        print("Metadata saved successfully.")
                        break
                    elif save_choice == 'n':
                        break
                    else:
                        print("Please enter 'y' for yes or 'n' for no.")

        except Exception as e:
            print(f"Error processing file: {str(e)}")

if __name__ == '__main__':
    IntroClass()