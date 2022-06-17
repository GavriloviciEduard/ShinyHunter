import re

import easyocr


class OCR:
    def __init__(self):
        print("Initializing OCR...")
        self.reader = easyocr.Reader(["en"])
        self.confidence_threshold = 0.7

    def get_image_text(self, image) -> list[str]:
        """Get text from image given as input.

        Args:
            image: Input image where text is located.

        Returns:
            list[str]: List containing all the text from the image.
        """

        text = self.reader.readtext(image, detail=0)
        return list(map(lambda x: re.sub(r"[^A-Za-z]+", "", x), text))
