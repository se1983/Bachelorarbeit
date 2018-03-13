import os

from ._float import Float


class ExtractorFactory:
    def __init__(self, data_directory):
        """
        Interface to get a extractor-generator-object.

        :param data_directory: Directory to the data of all ArgoFloats.
        """
        self.extractor_generator = (
            Float(os.path.join(data_directory,
                               profile_directory))
            for profile_directory in os.listdir(data_directory))

        self.__sum_floats = sum([os.path.isdir(os.path.join(data_directory, d)) for d in os.listdir(data_directory)])

    def get_data_sets(self):
        """
        Getting data.

        :return: generator - LazyLoading Graph of all Datasets of all ArgoFloats.
        """
        return self.extractor_generator

    def float_count(self):
        """
        Counting the ArgoFloats.

        :return: int - Number of directories in the Data-folder
        """
        return self.__sum_floats
