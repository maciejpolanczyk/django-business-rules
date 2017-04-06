import os


class TestResourceProvider:

    @staticmethod
    def get_test_data_dir():
        return os.path.abspath(os.path.join(os.path.dirname(__file__)))
