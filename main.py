from PIL import Image, UnidentifiedImageError, ImageEnhance
import json

class DisplayImage:
    """
    Represents a single image loaded into ASCII art and it's display settings
    size, brightness and contrast used when rendering as ASCII
    """
    # Corrects aspect of image, due to characters being 1:2 ratio
    ASPECT_CORRECTION = 0.5

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
        self.brightness = 1.0
        self.contrast = 1.0
        self.target_width = 50
        self.target_height = self._height_for_width(self.target_width)

    def _height_for_width(self, width):
        """Internal class help function, calculates 
        height that preserves aspect ratio for a given width.
        Not intended to be called outside the class but nothing prevents that"""
        return int(self.img.height / self.img.width * width * self.ASPECT_CORRECTION)

    def _width_for_height(self, height):
        """Internal class help function, calculates 
        width that preserves aspect ratio for a given height.
        Not intended to be called outside the class but nothing prevents that"""
        return int(height * self.img.width / (self.img.height * self.ASPECT_CORRECTION))

    def set_width(self, width):
        """Sets target width: height is recalculated to preserve aspect ratio.
        Not intended to be called outside the class but nothing prevents that"""
        try:
            width = int(width)
        except ValueError:
            print("Felaktig typ av värde för bredd")
            return
        self.target_width = width
        self.target_height = self._height_for_width(self.target_width)

    def set_height(self, height):
        """Sets target height: width is recalculated to preserve aspect ratio."""
        try:
            height = int(height)
        except ValueError:
                    print("Felaktig typ av värde för höjd")
                    return
        self.target_height = int(height)
        self.target_width = self._width_for_height(self.target_height)


    def render(self):
        """
        Returns a multi line string which represents the image in ASCII art.
        brightness/contrast/size adjustments applied.

        Parameters:
            width (int): character width of the output
            No default passed, the object has default w attribute 50.

        Returns:
            str: multi-line ASCII of image
        """

        width, height = self.target_width, self.target_height
        resized = self.img.resize((width, height))

        grayscale = resized.convert('L')
        grayscale = ImageEnhance.Brightness(grayscale).enhance(self.brightness)
        grayscale = ImageEnhance.Contrast(grayscale).enhance(self.contrast)

        ramp = " .:-=+*#%@"
        lines = []
        for y in range(height):
            row = ""
            for x in range(width):
                gray_value = grayscale.getpixel((x, y))
                index = int(gray_value / 255 * (len(ramp) - 1))
                row += ramp[index]
            lines.append(row)
        return "\n".join(lines)

    def set_brightness(self, factor):
        """
        Used to set the brightness for the ASCII art object

        Parameters: 
            float: factor for brightness
        """
        try:
            factor = float(factor)
        except ValueError:
                print("Felaktig typ av värde för ljusstyrka")
                return
        self.brightness = factor

    def set_contrast(self, factor):
        
            """
            Used to set the contrast for the ASCII art object
    
            Parameters: 
                float: factor for contrast
            """
            try:
                factor = float(factor)
            except ValueError:
                    print("Felaktig typ av värde för kontrast")
                    return
            self.contrast = factor

    def info(self):
        """
        Returns:
            dict: filename, original size, target size, brightness,
            contrast. All info for the ASCII art object
        """

        return {
        "filename": self.filename,
        "orgiginal size": self.org_size,
        "target size": (self.target_width, self.target_height),
        "brightness": self.brightness,
        "contrast": self.contrast,
    }

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
        Returns: 
            DisplayImage object: the DisplayImage marked as current.
            None if no image has been loaded yet
        """
        if self.current is None:
            return None
        return self.images[self.current]

    def info(self):
        """
        Returns a string listing all loaded images for display.
        """

        if not self.images:
            return "No image loaded"

        lines = ["===== Current session images ====="]
        for key, image in self.images.items():
            lines.append(key)
            for field, value in image.info().items():
                lines.append(f"    {field}: {value}")
        lines.append(f"Current image: {self.current}")
        return "\n".join(lines)

    def save_session(self, session_name):
        """
        Saves the current session to a text file. Adds no file extension.
        Overwrites existing file.

        Parameters:
            str session_name: The name for the file to be saved as.
        """
        if session_name is None:
            return "No save file name given for session save file"
        
        data = {
            "current": self.current,
            "images": {
                key: {
                    "filename": image.filename,
                    "target_width": image.target_width,
                    "target_height": image.target_height,
                    "brightness": image.brightness,
                    "contrast": image.contrast,
                }
                for key, image in self.images.items()
            },
        }
        with open(session_name, "w") as f:
            json.dump(data, f)

    def load_session(self, session_name):
        """
        Loads provided session_name file and reads in as current session

        Parameters:
            str: session name. The name of the session file to be loaded
        """
        try: 
            with open(session_name) as f:
                data = json.load(f)
        except FileNotFoundError:
            print("The file does not exist.")
            return
        except OSError:
            print("Cannot open the session file.")
            return
        
        for key, settings in data["images"].items():
            self.load_image(settings["filename"], alias=key if key != settings["filename"] else None)
            image = self.images[key]
            image.set_width(settings["target_width"])
            image.set_brightness(settings["brightness"])
            image.set_contrast(settings["contrast"])

        self.current = data["current"]

    def get_image(self, name=None):
        """
        Help function to resolves an image reference to a DisplayImage object.

        Parameters:
            name (str or None): alias or filename used when the image
                was loaded, or the literal word 'current'. If None,
                returns the current image.

        Returns:
            DisplayImage or None: the resolved image, or None if no
                matching image is loaded/found
        """
        if name is None or name == "current":
            return self.get_current()
        return self.images.get(name)

def run():
    """Starts the ASCII Art Studio command loop."""
    session = Session()
    print("Welcome to ASCII Art Studio!")
    while True:
        command = input("AAS: ")
        if not handle_command(session, command):
            break
    print("Bye!")

def handle_command(session, command):
    """
    Takes one command and executes against session.

    Returns: 
        bool: True unless the command is quit. On quit return False
    """
    parts = command.split()
    if not parts:
        return True

    action = parts[0]

    if action == "load":
        filename = parts[2]
        if parts[1] == "image":
            if len(parts) <= 3:
                session.load_image(filename)
                return True
            else:
                alias = parts[4]
                session.load_image(filename, alias)
                return True
        if parts[1] == "session":
            session.load_session(filename)
            return True

    elif action == "save":
        filename = parts[3]
        session.save_session(filename)
        return True

    elif action == "info":
        print(session.info())
        return True

    elif action == "render":
        if len(parts) >= 4 and parts[2] == "to":
            image = session.get_image(parts[1])
            output_filename = parts[3]
            if image is None:
                print(f"No such image: {parts[1]}")
                return True
            with open(output_filename, "w") as f:
                f.write(image.render())
            return True

        name = parts[1] if len(parts) > 1 else None
        image = session.get_image(name)
        if image is None:
            print("No image loaded")
            return True
        print(image.render())
        return True

    elif action == "set":
        if len(parts) < 4:
            return True
        name, prop, value = parts[1], parts[2], parts[3]
        image = session.get_image(name)
        if image is None:
            print(f"No such image: {name}")
            return True

        if prop == "width":
            image.set_width(value)
        elif prop == "height":
            image.set_height(value)
        elif prop == "brightness":
            image.set_brightness(value)
        elif prop == "contrast":
            image.set_contrast(value)
        else:
            print(f"Unknown property: {prop}")
        return True

    return True

if __name__ == '__main__':
    d = DisplayImage('peng.png')
    print(d.filename, d.org_size, d.brightness, d.contrast)

    try:
        bad = DisplayImage('finns_inte.jpg')
    except FileNotFoundError:
        print("Fångade FileNotFoundError korrekt, som väntat")

    try:
        bad2 = DisplayImage('text.jpg')
    except UnidentifiedImageError:
        print("Fångade UnidentifiedImageError korrekt, som väntat")

    print("--- Testar via Session.load_image() ---")
    s = Session()
    s.load_image('text.jpg')

    run()