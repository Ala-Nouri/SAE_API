from cryptography.fernet import Fernet
from fpdf import FPDF
from PIL import Image


class Crypter():
    def __init__(self):
        pass

    def generateKey(self):
        return Fernet.generate_key().decode()
    
    def encrypt(self, file, key):
        with open(file, 'rb') as f:
            data = f.read()

        fernet = Fernet(key.encode())
        encrypted = fernet.encrypt(data)
        with  open(file, 'wb') as f:
            f.write(encrypted)
        
        return encrypted

    def decrypt(self, file, key):
        with open(file, 'rb') as f:
            data = f.read()

        fernet = Fernet(key.encode())
        decrypted = fernet.decrypt(data)
        with  open(file, 'wb') as f:
            f.write(decrypted)
        return decrypted
    
    def create_pdf(self, image_files, output_path):
        pdf = FPDF()

        for image_file in image_files:
            # Open the image file
            cover = Image.open(image_file)
            
            # Convert the image to RGB mode if it's not already
            if cover.mode != 'RGB':
                cover = cover.convert('RGB')
            
            # Get the size of the image
            width, height = cover.size
            
            # Convert pixels to millimeters (1 px = 0.264583 mm)
            width, height = width * 0.264583, height * 0.264583
            
            # Add a new page with the size of the image
            pdf.add_page()
            
            # Get the dimensions of the page to ensure the image covers the whole page
            page_width = pdf.w
            page_height = pdf.h
            
            # Add the image to the page with dimensions of the page
            pdf.image(image_file, x=0, y=0, w=page_width, h=page_height)

        # Save the PDF to the specified output path
        pdf.output(output_path)