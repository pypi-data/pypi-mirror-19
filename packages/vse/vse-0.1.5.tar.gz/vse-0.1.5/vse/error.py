import vse


class VisualSearchEngineError(Exception):
    """Base class for vse exceptions."""
    pass


class DuplicatedImageError(VisualSearchEngineError):
    """Raised when trying to add already existing image to the image index."""

    def __init__(self, image_id):
        message = 'Image {} already exists in the index'.format(image_id)
        VisualSearchEngineError.__init__(self, message)


class NoImageError(VisualSearchEngineError):
    """Raised when trying to delete non-existing image path from the image index."""

    def __init__(self, image_id):
        message = 'Image {} does not exist in the index'.format(image_id)
        VisualSearchEngineError.__init__(self, message)


class ImageSizeError(VisualSearchEngineError):
    """Raised if loaded image width or height is smaller than IMAGE_MIN_SIZE."""

    def __init__(self, image_id='image'):
        message = 'Both width and height of the {} must be greater than {}'.format(image_id, vse.utils.IMAGE_MIN_SIZE)
        VisualSearchEngineError.__init__(self, message)


class ImageLoaderError(VisualSearchEngineError):
    """Raised if cannot read image from file or buffer"""

    def __init__(self, image_path=''):
        if image_path:
            message = 'Cannot read file: {}'.format(image_path)
        else:
            message = 'Cannot read image from buffer'
        VisualSearchEngineError.__init__(self, message)
