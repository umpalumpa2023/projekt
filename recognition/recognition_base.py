# recognition/recognition_base.py

class RecognitionSoftware:
    def detect_person(self, frame):
        """Detects the person in a frame and returns the COM (center of mass) coordinates.
        This function should be implemented by each specific recognition software class."""
        raise NotImplementedError("This method should be implemented by the recognition software.")
