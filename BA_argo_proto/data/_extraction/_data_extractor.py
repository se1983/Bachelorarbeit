import os

from ._float import Float

class ExtractorFactory:
    def __init__(self, data_directory):
        self.data_directory = data_directory

        self.extractor_generator = (  # Comprehension with () is a generator.
            Float(os.path.join(self.data_directory, profile_directory)) for
            profile_directory in os.listdir(self.data_directory)
        )

    def get_data_sets(self):
        return self.extractor_generator
