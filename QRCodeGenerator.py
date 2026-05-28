import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os
import sys
from datetime import datetime
import platform


class QRCodeGenerator:
    def __init__(self):
        self.output_dir = "qr_codes"
        self.create_output_directory()

    def create_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}/")

    def generate_filename(self, custom_name=None):
        """Generate filename with timestamp if custom name not provided"""
        if custom_name:
            # Validate and clean filename
            custom_name = custom_name.strip()
            if not custom_name:
                print("Error: Filename cannot be empty!")
                return None

            # Remove invalid characters
            invalid_chars = '<>:"|?*'
            for char in invalid_chars:
                custom_name = custom_name.replace(char, '_')

            if not custom_name.endswith('.png'):
                custom_name += '.png'
            return custom_name
        else:
            # Auto-generate with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"qrcode_{timestamp}.png"

    def generate_qr_code(self, data, filename=None, open_file=False):
        """Generate a single QR code"""
        if not data or not data.strip():
            print("Error: QR code data cannot be empty!")
            return False

        data = data.strip()

        # Generate filename
        output_filename = self.generate_filename(filename)
        if not output_filename:
            return False

        output_path = os.path.join(self.output_dir, output_filename)

        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            # Create image with rounded corners
            img = qr.make_image(fill_color="black", back_color="white")

            # Save the image
            img.save(output_path)

            # Get absolute path
            absolute_path = os.path.abspath(output_path)
            print(f"\n✓ QR code generated successfully!")
            print(f"  Data: {data[:50]}{'...' if len(data) > 50 else ''}")
            print(f"  File: {absolute_path}")

            # Option to open the image
            if open_file:
                if self.open_image(output_path):
                    print("  Opening image...")

            return True

        except Exception as e:
            print(f"Error: Failed to generate QR code - {str(e)}")
            return False

    def open_image(self, file_path):
        """Open the generated image with default application"""
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'open "{file_path}"')
            else:  # Linux
                os.system(f'xdg-open "{file_path}"')
            return True
        except Exception as e:
            print(f"Warning: Could not open image - {str(e)}")
            return False

    def batch_generate(self, urls_file="urls.txt", open_files=False):
        """Generate QR codes from a batch file"""
        if not os.path.exists(urls_file):
            print(f"Error: File '{urls_file}' not found!")
            print(f"Please create '{urls_file}' with one URL/text per line.")
            return False

        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                urls = f.readlines()

            if not urls:
                print(f"Error: '{urls_file}' is empty!")
                return False

            # Filter empty lines and comments
            urls = [url.strip() for url in urls if url.strip() and not url.strip().startswith('#')]

            if not urls:
                print(f"Error: No valid URLs found in '{urls_file}'!")
                return False

            print(f"\nFound {len(urls)} URL(s) to process...")

            successful = 0
            failed = 0

            for i, url in enumerate(urls, 1):
                print(f"\n[{i}/{len(urls)}] Processing: {url[:60]}{'...' if len(url) > 60 else ''}")

                # Generate filename based on index
                filename = f"qrcode_batch_{i:03d}.png"

                if self.generate_qr_code(url, filename, open_files):
                    successful += 1
                else:
                    failed += 1

            print(f"\n{'='*50}")
            print(f"Batch Processing Complete!")
            print(f"  Successful: {successful}")
            print(f"  Failed: {failed}")
            print(f"  Output directory: {os.path.abspath(self.output_dir)}/")
            print(f"{'='*50}\n")

            return True

        except Exception as e:
            print(f"Error: Failed to process batch file - {str(e)}")
            return False

    def display_menu(self):
        """Display main menu and get user choice"""
        print("\n" + "="*50)
        print("         QR Code Generator")
        print("="*50)
        print("1. Generate Single QR Code")
        print("2. Generate QR Codes from Batch File (urls.txt)")
        print("3. Exit")
        print("="*50)
        print(f"Output Directory: {os.path.abspath(self.output_dir)}/")
        print("="*50)

        choice = input("Enter your choice (1-3): ").strip()
        return choice

    def get_yes_no_input(self, prompt):
        """Get yes/no input from user"""
        while True:
            response = input(prompt + " (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    def run(self):
        """Main application loop"""
        print("\n" + "="*50)
        print("    Welcome to QR Code Generator")
        print("="*50)

        while True:
            choice = self.display_menu()

            if choice == '1':
                # Single QR code mode
                print("\n--- Generate Single QR Code ---")
                data = input("Enter URL or text: ").strip()

                if not data:
                    print("Error: Please enter valid data!")
                    continue

                use_custom_name = self.get_yes_no_input("Use custom filename?")
                filename = None

                if use_custom_name:
                    filename = input("Enter filename (without .png): ").strip()

                open_file = self.get_yes_no_input("Open image after creation?")
                self.generate_qr_code(data, filename, open_file)

            elif choice == '2':
                # Batch mode
                print("\n--- Generate QR Codes from Batch File ---")

                # Check if urls.txt exists
                if not os.path.exists("urls.txt"):
                    print("File 'urls.txt' not found!")
                    create_sample = self.get_yes_no_input("Create sample urls.txt?")

                    if create_sample:
                        try:
                            with open("urls.txt", 'w', encoding='utf-8') as f:
                                f.write("https://www.github.com\n")
                                f.write("https://www.python.org\n")
                                f.write("https://www.stackoverflow.com\n")
                                f.write("# Add your URLs below, one per line\n")
                            print("Sample 'urls.txt' created successfully!")
                            print("Please edit the file and add your URLs.")
                        except Exception as e:
                            print(f"Error: Failed to create urls.txt - {str(e)}")
                    continue

                open_files = self.get_yes_no_input("Open images after generation?")
                self.batch_generate("urls.txt", open_files)

            elif choice == '3':
                # Exit
                print("\nThank you for using QR Code Generator. Goodbye!")
                break

            else:
                print("Error: Invalid choice! Please enter 1, 2, or 3.")


def main():
    """Entry point"""
    try:
        generator = QRCodeGenerator()
        generator.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
