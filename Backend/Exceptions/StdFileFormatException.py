class StdFileFormatException(Exception):
    def __init__(self, error_map):
        self.error_map = error_map

    def __str__(self):
        return repr(self.error_map)
