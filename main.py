from PIL import Image, UnidentifiedImageError


class DisplayImage:
    """
    Represents a single image loaded into ASCII art and it's display settings
    size, brightness and contrast used when rendering as ASCII
    """

    def __init__(self, filename):
        """
        Loads the provided file in root folder and sets default settings

        Parameters:
            filename (str): name of the JPG/PNG image file to be loaded

        Raises:
            FileNotFoundError / OSError: If the file doesn't exist or can't be
            opened as a JPG/PNG image file
        """

        with Image.open(filename) as img:
            img.load()
        
        self.filename = filename
        self.img = img
        self.org_size = self.img.size
        self.brightness = 1
        self.contrast = 1


    def render(self, width=50):
        """
        Returns a multi line string which represents the image in ASCII art.
        brightness/contrast/size adjustments applied.

        Parameters:
            width (int): character width of the output
            Deafult 50 if no parameter is passed

        Returns:
            str: multi-line ASCII of image
        """

    def set_brightness(self, factor):
        """
        Used to set the brightness for the ASCII art object

        Parameters: 
            int: factor for brightness to be applied
        """

    def set_contrast(self, factor):
        
            """
            Used to set the contrast for the ASCII art object
    
            Parameters: 
                int: factor for contrast to be applied
            """

    def info(self):
        """
        Returns:
            dict: filename, original size, target size, brightness,
            contrast. All info for the ASCII art object
        """

class Session:
    """
    Holds all images loaded during one ASCII Art Studio session and
    tracks which image is current.
    exposes methods that operate on images by name.
    """

    def __init__(self):
        self.images = {}
        self.current = None

    def load_image(self, filename, alias=None):
        """
        Loads filename as a new DisplayImage, stored under alias if given
        Otherwise stored as filename. Sets the image to current

        Raises:
            FileNotFoundError / OSError: If the file doesn't exist or can't be
            opened as a JPG/PNG image file

        """
        try:
            image = DisplayImage(filename)
        except FileNotFoundError:
            print("The file does not exist.")
            return
        except UnidentifiedImageError:
            print("The file is broken or not a valid image.")
            return
        except OSError:
            print("Cannot open the image.")
            return
        key = alias if alias else filename
        self.images[key] = image
        self.current = key

    def get_current(self):
        """
        Returns the DisplayImage currently marked as current.
        """

    def info(self):
        """
        Returns a string listing all loaded images for display.
        """

def run():
    """Starts the ASCII Art Studio command loop."""
    session = Session()
    print("Welcome to ASCII Art Studio!")
    while True:
        command = input("AAS: ")
        if not handle_command(session, command):
            break

def handle_command(session, command):
    """
    Takes one command and executes against session.

    Returns: 
        bool: True unless the command is quit. On quit return False
    """

if __name__ == '__main__':
    d = DisplayImage('peng.png')
    print(d.filename, d.org_size, d.brightness, d.contrast)

    try:
        bad = DisplayImage('finns_inte.jpg')
    except FileNotFoundError:
        print("Fångade FileNotFoundError korrekt, som väntat")