import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import csv
import random
import re
from io import StringIO
import sys

from src.modules.ai.credential_generator import Credential_Generator


class TestCredentialGenerator(unittest.TestCase):
    """Test cases for the Credential_Genertor class."""

    mock_data = "word1\nword2\nword3"

    @patch("src.modules.ai.credential_generator.CredentialMDP")
    @patch("src.modules.ai.credential_generator.os.path.exists")
    @patch("src.modules.ai.credential_generator.csv.DictReader")
    @patch("builtins.open", new_callable=mock_open, read_data=mock_data)
    def setUp(self, mock_file, mock_dict_reader, mock_exists, mock_credential_mdp):
        """Set up test environment before each test iteration."""
        mock_exists.return_value = True

        # Setup mock CSV reader with required fields
        mock_reader = MagicMock()
        mock_reader.fieldnames = ["id", "content", "url"]
        mock_dict_reader.return_value = mock_reader
        mock_reader.__iter__.return_value = [
            {"id": "1", "content": "Content1", "url": "http://example.com"},
            {"id": "2", "content": "Content2", "url": "http://example2.com"},
        ]

        # Return mocks when mdp is called
        self.mock_username_mdp = MagicMock()
        self.mock_password_mdp = MagicMock()
        mock_credential_mdp.side_effect = [
            self.mock_username_mdp,
            self.mock_password_mdp,
        ]

        self.generator = Credential_Generator("test.csv", "test_wordlist.txt")

        # Set properties directly after initialization
        self.generator.wordlists = ["test1", "test2", "test3"]
        self.generator.web_text = "sample text made for testing."

        # configure the mocks in MDP
        self.mock_username_mdp.calculate_username_quality.return_value = 0.8
        self.mock_password_mdp.calculate_password_strength.return_value = 0.8
        self.mock_username_mdp.choose_action.return_value = ("a", "b")
        self.mock_password_mdp.choose_action.return_value = ("c", "d")
        self.mock_username_mdp.initial_states = ["username_test"]
        self.mock_password_mdp.initial_states = ["password_test"]

    @patch("src.modules.ai.credential_generator.ollama.chat")
    def test_calculate_password_strength(self, mock_ollama_chat):
        """Test calculate_password_strength method."""

        # Arrange
        mock_ollama_chat.return_value = {
            "message": {"content": "secure - follows best practices"}
        }

        # Act
        result = self.generator.calculate_password_strength("TestPassword123!")

        # Assert
        self.assertEqual(result, "secure - follows best practices")
        mock_ollama_chat.asswer_called_once()

    def test_calculate_username_strength(self):
        """Test calculate_username_strength"""

        # Act
        result = self.generator.calculate_username_strength("testuser")

        # Assert
        self.assertEqual(result, 0.8)

    def test_get_ai_hyperparameters(self):
        """Test get_ai_hyperparameters"""

        # Act
        result = self.generator._get_ai_hyperparameters()

        # Assert
        self.assertIsInstance(result, list)

    def test_get_ai_wordlist(self):
        """Test get_ai_wordlist"""

        # Act
        result = self.generator.get_ai_wordlist()

        # Assert
        self.assertEqual(result, ["test1", "test2", "test3"])

    @patch("builtins.open", new_callable=mock_open)
    def test_process_ai_wordlist(self, mock_file):
        """Test process_ai_wordlist"""

        # Arrange
        mock_csv_writter = MagicMock()
        csv.DictWriter = MagicMock(return_value=mock_csv_writter)

        self.generator.calculate_password_strength = MagicMock(
            return_value="secure - good password"
        )

        credentials = [
            (
                "user1",
                "password1",
            ),
            ("user2", "pass2"),
        ]

        # Act
        self.generator.process_ai_wordlist(credentials)

        # Assert
        mock_file.assert_called_once_with(
            "processed_credentials.csv", "w", newline="", encoding="utf-8"
        )
        csv.DictWriter.assert_called_once()
        mock_csv_writter.writeheader.assert_called_once()
        self.assertEqual(mock_csv_writter.writerows.call_count, 1)

    def test_preprocess_text(self):
        """Text _preprocess_text"""

        # Act
        result = self.generator._preprocess_text("This is a test word123")

        # Assert
        self.assertIsInstance(result, list)
        self.assertIn("word123", result)
        self.assertIn("test", result)
        self.assertIn("this", result)
        self.assertNotIn("is", result)
        self.assertNotIn("a", result)

    def test_build_state_transitions(self):
        """Test _build_state_transitions"""
        # Arrange
        self.generator._preprocess_text = MagicMock(return_value=["testword"])

        # Act
        self.generator._build_state_transitions()

        # Assert
        self.assertTrue(True)

    @patch("random.randint")
    def test_generate_credential(self, mock_randint):
        """Test generate_credential"""
        # Arrange
        mock_randint.return_value = 123
        self.mock_username_mdp.get_reward.return_value = 0.5
        self.mock_password_mdp.get_reward.return_value = 0.5

        mock_password = "ImprovedPassword1!"

        # Act
        with patch.object(
            self.generator, "_improve_password", return_value=mock_password
        ):
            username, password = self.generator.generate_credential()

        # Assert
        self.assertIsInstance(username, str)
        self.assertIsInstance(password, str)
        self.assertEqual(password, mock_password)
        self.mock_username_mdp.choose_action.assert_called()
        self.mock_password_mdp.choose_action.assert_called()

    @patch.object(Credential_Generator, "generate_credential")
    def test_generate_credentials(self, mock_generate_credential):
        """Test generate_credentials"""
        # Arrange
        mock_user = "testuser"
        mock_pass = "testpassword"
        mock_generate_credential.return_value = (mock_user, mock_pass)

        # Act
        result = self.generator.generate_credentials(3)

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(
            result,
            [(mock_user, mock_pass), (mock_user, mock_pass), (mock_user, mock_pass)],
        )
        self.assertEqual(mock_generate_credential.call_count, 3)

    def test_improve_password(self):
        """Test _improve_password"""
        # Act
        password = self.generator._improve_password("testpassword")
        result_criteria = self.generator._get_password_status(password)
        self.assertEqual(result_criteria, 0b111)

        password = self.generator._improve_password("!@##")
        result_criteria = self.generator._get_password_status(password)
        self.assertEqual(result_criteria, 0b111)

        password = self.generator._improve_password("!@#$%^&*()<>?{},./")
        result_criteria = self.generator._get_password_status(password)

        self.generator.password_cap = False
        self.generator.password_special_chars = False
        password = self.generator._improve_password("testpassword")
        result_criteria = self.generator._get_password_status(password)
        self.assertEqual(result_criteria, 0b111)
        self.assertEqual(self.generator._get_password_status("testpassword"), 0b111)
        self.generator.password_cap = True
        self.generator.password_special_chars = True
        self.assertEqual(self.generator._get_password_status("testpassword"), 0b100)

    @patch("src.modules.ai.credential_generator.os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.DictReader")
    def test_load_web_text(self, mock_dict_reader, mock_file, mock_exists):
        """Test _load_web_test"""
        # Arrange
        mock_exists.return_value = True
        mock_reader = MagicMock()
        mock_reader.fieldnames = ["id", "content", "url"]
        mock_dict_reader.return_value = mock_reader
        mock_reader.__iter__.return_value = [
            {"content": "Content1"},
            {"content": "Content2"},
            {"content": ""},
        ]

        # Act
        result = self.generator._load_web_text("test_csv.csv")

        # Assert
        self.assertEqual(result, "content1 content2")
        mock_exists.assert_called_with("test_csv.csv")
        mock_file.assert_called_with("test_csv.csv", "r", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
