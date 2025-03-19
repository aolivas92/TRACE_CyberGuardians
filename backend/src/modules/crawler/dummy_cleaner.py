# dummy_cleaner.py
class DummyCleaner:
    def clean(self, parsed_data):
        parsed_data["cleaned"] = True
        return parsed_data