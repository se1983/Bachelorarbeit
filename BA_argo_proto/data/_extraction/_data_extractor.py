import os

from ._float import Float

class ExtractorFactory:
    def __init__(self, data_directory):
        """
        Factory for Argo Float data-extractors.
        
        :param data_directory: PATH to the Argo_Data directory.
        """
        self.data_directory = data_directory

    def get_data_sets(self):
        """
        The whole dataset of the argo-floats.
        
        :return: Generator-object holding Argo-Floats
        """
        for profile_directory in os.listdir(self.data_directory):
            yield Float(os.path.join(self.data_directory,
                                     profile_directory))
