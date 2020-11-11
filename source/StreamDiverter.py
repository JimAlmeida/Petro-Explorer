import sys
from io import StringIO

class StreamDiverter:
    def __init__(self):
        self.old_Output = sys.stdout
        self.address = StringIO()
        sys.stdout = self.address

    def __del__(self):
        sys.stdout = self.old_Output

    def srcExtractor(self):
        return str(self.address.getvalue()).rsplit("\"")[7]