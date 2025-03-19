# dummy_validator.py
class DummyValidator:
    def is_valid(self, cleaned_data):
        return True if cleaned_data else False