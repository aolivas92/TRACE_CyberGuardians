import csv
import os
import random
import re
import time
from typing import List, Tuple
import warnings

import ollama

from .credential_mdp import CredentialMDP


class Credential_Generator:
    """
    In charge of generating usernames and passwords using AI-based learning models.

    Attributes:
        No public attributes.

    Methods:
        calculate_password_strength(self, password: str) -> float:

        calculate_username_strenth(self, username: str) -> float:

        _get_ai_hyperparameters(self) -> list[str]:

        get_ai_wordlist(self) -> list[str]:

        process_ai_wordlist(self, credentials_list: list[str]) -> None:

    Notes:
        This class doesn't inherit from any superclass.
    """

    def __init__(
        self,
        csv_path: str | None = None,
        wordlist_path: str | None = None,
        min_username_length: int = 8,
        username_cap: bool = True,
        username_special_chars: bool = True,
        min_password_length: int = 12,
        password_cap: bool = True,
        password_special_chars: bool = True,
    ):
        """
        Initialize the Credential Generator.

        Args:
            csv_path (str, optional): Path to CSV with web text.
            wordlist_path (str, optional): Path to wordlist file.
        """
        try:
            if csv_path and os.path.exists(csv_path):
                self.web_text = self._load_web_text(csv_path)
            else:
                self.web_text = ""

            if wordlist_path and os.path.exists(wordlist_path):
                self.wordlists = self._load_wordlist(wordlist_path)
            else:
                self.wordlists = []

        except FileNotFoundError as e:
            print(f"Error loading input files in Credential_Generator: {e}")
            self.web_text = csv_path if csv_path else ""
            self.wordlists = wordlist_path if wordlist_path else []

        self.username_mdp = CredentialMDP(order=2)
        self.password_mdp = CredentialMDP(order=3)
        self.min_username_length = min_username_length
        self.username_cap = username_cap
        self.username_special_chars = username_special_chars
        self.min_password_length = min_password_length
        self.password_cap = password_cap
        self.password_special_chars = password_special_chars

    def calculate_password_strength(self, password: str) -> str:
        """
        Calculates the strength of a given password and evaluates it using MDP evaluator.

        Args:
            password (str): The password to evaluate. Must not be empty.

        Returns:
            str: Evaluation response from MDP Evaluator.

        Raises:
            ValueError: If the password is empty.
        """
        if not password:
            raise ValueError("Password cannot be empty")

        # Basic strength score to replace embeddings.
        score = self.password_mdp.calculate_password_strength(password)

        if score > 0.7:
            return "secure - meets best practices"
        else:
            return "not secure - does not meet all best practices."

    def _suggest_password(self, password: str, score: float) -> str:
        strengthened_password = ""
        good_practices_info = (
            "Good password practices include the following: "
            "1. Length: Passwords should be at least 12 characters long. "
            "2. Complexity: Passwords should include a mix of uppercase letters, lowercase letters, numbers, and special characters. "
            "3. Unpredictability: Avoid common words, phrases, or predictable patterns like '1234' or 'qwerty'. "
            "4. Uniqueness: Passwords should be unique for every account to prevent leaks. "
            "5. Avoid personal information: Avoid using easily guessable information, such as names or birthdays. "
            "6. Use of password managers: Consider using password managers for securely storing passwords."
        )
        query = (
            f"This is the password to review: '{password}.'"
            f"This password got the score of {score:.2f}.\n"
            f"Keep in mind the good best practice info:\n{good_practices_info}\n"
            f"It is your task to improve this password so it follows the best practices\n"
            f"while keeping the passwords concept, so for example if the password you'd get is 'Hello123', then you should return something along the lines of 'H31l0w@rLd20341'.\n"
            f"You should also avoid using escape characters like '\\n' or '\\t', but add any other alphanumeric string of around 5 characters. Take into account that it meets all good practices\n"
            f"Please only answer with your suggestion of the password, with no other text"
        )
        system_message = "You are a password security expert. Evaluate passwords carefully and provide the best suggestion you can come up with."
        message = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ]
        try:
            response = ollama.chat(model="gemma3:latest", messages=message)
            strengthened_password = response["message"]["content"]
            if self._get_password_status(strengthened_password) != 0b111:
                strengthened_password = self._improve_password(strengthened_password)
        except Exception as e:
            warnings.warn(
                f"Error calling Ollama due to : {e}\nDefaulting to improving password with default method"
            )
            strengthened_password = self._improve_password(password)
        return strengthened_password

    def calculate_username_strength(self, username: str) -> float:
        """
        Calculate the strength of a given username.

        Args:
            username (str): The username to evaluate. Must not be empty.

        Returns:
            float: A strength score between 0.0 and 1.0.

        Raises:
            ValueError: If the username is empty.
        """
        if not username:
            raise ValueError("Username cannot be empty")

        return self.username_mdp.calculate_username_quality(username)

    def _suggest_username(self, username: str, score: float) -> str:
        """
        Uses Ollama to suggest a more secure and unique version of a given username,
        while maintaining its original concept.

        Args:
            username (str): The username to evaluate and improve.
            score (float): The similarity or quality score of the original username.

        Returns:
            str: A new, AI-suggested secure username based on the original.
        """
        improved_username = ""
        username_practices = (
            "Good username practices include:\n"
            "1. Avoid using personal info (real name, birthday, etc.).\n"
            "2. Avoid common words (e.g., admin, test).\n"
            "3. Make it unique and unpredictable.\n"
            "4. Keep it at least 8 characters long.\n"
            "5. Use alphanumeric characters and (optionally) underscores or dots."
        )

        query = (
            f"Review this username: '{username}' (score: {score:.2f}).\n\n"
            f"{username_practices}\n\n"
            f"Suggest a stronger version that follows the practices while keeping the concept of the original (e.g., 'johndoe' → 'j0hnd03_dev87').\n"
            f"Only return the new username, no explanation, and avoid escape characters like '\\n'."
        )

        system_message = "You are a security advisor for usernames. Suggest a better version of a given username to follow best practices for uniqueness and anonymity."

        message = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ]

        try:
            response = ollama.chat(model="gemma3:latest", messages=message)
            improved_username = response["message"]["content"].strip().replace("\n", "")
            if len(improved_username) < self.min_username_length:
                improved_username += str(
                    random.randint(10, 99)
                )  # Ensure minimum length
        except Exception as e:
            warnings.warn(
                f"Error calling Ollama for username improvement: {e}\nUsing fallback method."
            )
        improved_username = f"user_{random.randint(1000, 9999)}"
        return improved_username

    def _get_ai_hyperparameters(self) -> List[str]:  # Unused
        """
        Retrieves the AI Hyperparameters for the ML model from the user.

        Args:
            None

        Returns:
            list[str]: the list of hyperparameters for the AI model.

        Raises:
            ValueError: If there are no hyperparameters.
        """
        # TODO: Update to receive from user when backend is set up.
        return [""]

    def get_ai_wordlist(self) -> List[str] | str:
        """
        Provides the results of the AI results as a word list.

        Args:
            None

        Returns:
            list[str]: the wordlist that has been generated.

        Raises:
            ValueError: if there is no wordlist that has been generated.
        """
        if not self.wordlists:
            raise ValueError("No wordlist has been generated or loaded")
        return self.wordlists

    def process_ai_wordlist(self, credentials_list: list[str]) -> None:
        """
        Processes the wordlist containing usernames and passwords along with the score of their confidence.

        Args:
            credentials_list (list[tuple[str, str]]): the wordlist that needs to be processed.

        Returns:
            None

        Raises:
            ValueError: if the credentials_list is empty.
        """
        if not credentials_list:
            raise ValueError("Credential list cannot be empty")

        # Process and score each credential
        processed_credentials = []
        for username, password in credentials_list:
            username_score = self.calculate_username_strength(username)
            password_response = self.calculate_password_strength(password)
            is_secure = "secure" in password_response.lower()

            processed_credentials.append(
                {
                    "username": username,
                    "username_score": username_score,
                    "password": password,
                    "is_secure": is_secure,
                    "password_evaluation": password_response,
                }
            )

        with open(
            "processed_credentials.csv", "w", newline="", encoding="utf-8"
        ) as outfile:
            fieldnames = [
                "username",
                "username_score",
                "password",
                "is_secure",
                "password_evaluation",
            ]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_credentials)

    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text data for training.

        Args:
            text (str): The text to preprocess.

        Returns:
            List[str]: List of words.
        """
        words = re.findall(r"\w+", text.lower())
        return [
            word for word in words if len(word) >= 4
        ]  # Filter out words shorter than 4 chars

    def _build_state_transitions(self):
        """
        Build state transitions for username and password generation.
        """
        username_date = set(self._preprocess_text(self.web_text) + self.wordlists)
        password_data = set(word for word in username_date if len(word) >= 8)

        for word in username_date:
            for i in range(len(word) - self.username_mdp.order):
                state = f"username_{word[i : i + self.username_mdp.order]}"
                action = word[i + self.username_mdp.order]
                next_char = word[i + self.username_mdp.order]
                self.username_mdp.state_transitions[state][action].add(next_char)
                if i == 0:
                    self.username_mdp.initial_states.append(state)

        for word in password_data:
            for i in range(len(word) - self.password_mdp.order):
                state = f"password_{word[i : i + self.password_mdp.order]}"
                action = word[i + self.password_mdp.order]
                next_char = word[i + self.password_mdp.order]
                self.password_mdp.state_transitions[state][action].add(next_char)
                if i == 0:
                    self.password_mdp.initial_states.append(state)

    def generate_credential(self) -> Tuple[str, str]:
        """
        Generate a username and password pair.

        Returns:
            tuple[str, str]: Generated username and password.
        """
        # -- Generate username --
        if not self.username_mdp.initial_states:
            state = f"username_{random.choice(self.wordlists)[:2] if self.wordlists else 'user'}"
        else:
            state = random.choice(self.username_mdp.initial_states)

        username = state[9:]
        while len(username) < self.min_username_length:
            action, next_char = self.username_mdp.choose_action(state)
            if not action or not next_char:
                break
            username += next_char
            next_state = f"username_{username[-self.username_mdp.order :]}"
            reward = self.username_mdp.get_reward(state, action, next_char)
            self.username_mdp.update_q_value(
                state, action, next_char, next_state, reward
            )
            state = next_state

        username_score = self.calculate_username_strength(username)
        username = self._suggest_username(username, username_score)
        if self._get_username_status(username) != 0b111:
            username = self._improve_username(username)
        self.username_mdp.used_usernames.add(username)

        # -- Generate password --
        if not self.password_mdp.initial_states:
            state = f"password_{random.choice(self.wordlists)[:3] if self.wordlists else 'pwd'}"
        else:
            state = random.choice(self.password_mdp.initial_states)

        password = state[9:]
        while len(password) < self.min_password_length:
            action, next_char = self.password_mdp.choose_action(state)
            if not action or not next_char:
                break
            password += next_char
            next_state = f"password_{password[-self.password_mdp.order :]}"
            reward = self.password_mdp.get_reward(state, action, next_char)
            self.password_mdp.update_q_value(
                state, action, next_char, next_state, reward
            )
            state = next_state

        password_score = self.password_mdp.calculate_password_strength(password)
        password = self._suggest_password(password, password_score)
        if self._get_password_status(password) != 0b111:
            password = self._improve_password(password)

        return username, password

    def generate_credentials(self, count: int = 10) -> List[Tuple[str, str]]:
        """
        Generate multiple credentials.

        Args:
            count (int): Number of credentials to generate.

        Returns:
            list[tuple[str, str]]: List of generated username and password pairs.
        """
        self._build_state_transitions()
        credentials = []
        for _ in range(count):
            username, password = self.generate_credential()
            credentials.append((username, password))
        return credentials

    def _get_password_status(self, password: str) -> int:
        """
        Evaluates a password and returns a status code as a binary flag integer.

        This function checks if the password meets various strength criteria and
        represents the results as a binary flag where:
        - 0b001 (1): Contains special characters
        - 0b010 (2): Contains capital letters
        - 0b100 (4): Meets minimum length requirement

        The flags are combined using bitwise OR operations, so a fully compliant
        password would return 0b111 (7).

        Args:
            password (str): The password string to evaluate

        Returns:
            int: Binary flag integer representing which criteria are met
                 - 0 if no criteria are met
                 - 1-7 depending on which combination of criteria are met

        Example:
            >>> get_password_status("a")
            0
            >>> get_password_status("Password1234")
            6  # Meets length and capitalization requirements (4+2)
            >>> get_password_status("Password!")
            7  # Meets all requirements (4+2+1)
        """
        status = 0b000 & 0b111  # Default to not having anything set
        if len(password) >= self.min_password_length:
            status |= 0b100
        if re.search(r"[A-Z]", password) or not self.password_cap:
            status |= 0b010
        if (
            re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', password)
            or not self.password_special_chars
        ):
            status |= 0b001
        return status

    def _update_capitalization(self, password: str) -> str:
        """
        Randomly capitalizes one lowercase letter in the password or adds a capital letter if none present.

        This function identifies all lowercase letters in the given password,
        randomly selects one, and converts it to uppercase. If the password
        contains no lowercase letters, it adds a capital letter 'A' to the end
        of the password.

        Args:
            password (str): The password string to modify

        Returns:
            str: A new password string with either one randomly capitalized letter,
                 or the original password with an added capital letter if no lowercase
                 letters were present

        Examples:
            >>> _update_capitalization("hello123")
            "hEllo123"  # The 'e' was randomly selected to be capitalized

            >>> _update_capitalization("12345")
            "12345A"    # No lowercase letters to capitalize, so 'A' was added
        """

        lowercase_indices = [
            i for i, char in enumerate(password) if re.match(r"[a-z]", char)
        ]
        if lowercase_indices:
            random_capitalize = random.choice(lowercase_indices)
            char = password[random_capitalize]
            password = (
                password[:random_capitalize]
                + char.upper()
                + password[random_capitalize + 1 :]
            )
        else:
            password += "A"
        return password

    def _add_length_to_password(self, password: str) -> str:
        """
        Extends a password to meet the minimum required length.

        This function calculates how many additional characters are needed
        to reach the minimum password length, then generates a random string
        of that length using a diverse character set (including lowercase letters,
        numbers, and special characters) and appends it to the original password.

        Args:
            password (str): The original password to extend

        Returns:
            str: The extended password that meets the minimum length requirement

        Note:
            The function uses `self.min_password_length` to determine the
            required minimum length.

        Example:
            If min_password_length is 8:
            >>> _add_length_to_password("abc")
            "abc1x!p4"  # Random 5 characters added to reach length 8
        """
        # Additional 5 characters to increase complexity of password
        length_to_add = self.min_password_length - len(password) + 5
        character_set = "abcdefghijklmnopqrstuvwxyz0123456789"
        salt = "".join(random.choice(character_set) for _ in range(length_to_add))
        password += salt
        return password

    def _improve_password(self, password: str) -> str:
        """
        Enhance the generated password with additional complexity, depending on the
        parameters set by:
        - self.min_password_length
        - self.password_cap
        - self. password_special_chars

        Args:
            password (str): The password to enhance.

        Returns:
            str: Enhanced password.
        """
        required_flags = 0b100  # Length is always required
        if self.password_cap:
            required_flags |= 0b010
        if self.password_special_chars:
            required_flags |= 0b001
        password_status = self._get_password_status(password)
        missing_flags = required_flags & ~password_status

        special_chars = "!@#$%^&*()_+-=[]{}|;:,./<>"
        enhanced = password

        if (missing_flags & 0b100) == 0b100:  # Missing Length
            enhanced = self._add_length_to_password(enhanced)
        if (missing_flags & 0b010) == 0b010:  # Missing capitalization
            for _ in range(3):
                enhanced = self._update_capitalization(enhanced)
        if (missing_flags & 0b001) == 0b001:
            for _ in range(3):  # Add 3 random special chars
                enhanced += random.choice(special_chars)

        return enhanced

    def _improve_username(self, username: str) -> str:
        """
        Improve the username by adding uniqueness, random digits, and optionally
        modifying characters to enhance security.

        Args:
            username (str): The original username to improve.

        Returns:
            str: A more secure and unique version of the username.
        """
        substitutions = {
            "a": ["@", "4"],
            "e": ["3"],
            "i": ["1", "!"],
            "o": ["0"],
            "s": ["$", "5"],
            "l": ["1"],
            "t": ["7"],
        }

        improved_username = ""
        for char in username:
            if char.lower() in substitutions and random.random() < 0.3:
                improved_username += random.choice(substitutions[char.lower()])
            else:
                improved_username += char

        suffix = random.randint(100, 9999)  # Add a random suffix
        improved_username += str(suffix)

        # Ensure minimum length
        if len(improved_username) < self.min_username_length:
            pad_length = self.min_username_length - len(improved_username)
            improved_username += "".join(
                random.choices("abcdefghijklmnopqrstuvwxyz", k=pad_length)
            )
        return improved_username

    def _get_username_status(self, username: str) -> int:
        """
        Evaluates a username and returns a status code as a binary flag integer.

        Flags:
        - 0b001 (1): Meets minimum length
        - 0b010 (2): Does not contain common personal patterns (e.g., names, years, admin)
        - 0b100 (4): Contains non-dictionary-like elements (e.g., numbers, symbols)

        Returns:
         int: A combined status flag from 0 to 7
        """
        status = 0b000

        # Rule 1: Length
        if len(username) >= self.min_username_length:
            status |= 0b001

        # Rule 2: No common personal info or patterns
        banned_patterns = ["admin", "user", "test", "root", "guest", "name"]
        if not any(pattern in username.lower() for pattern in banned_patterns):
            status |= 0b010

        # Rule 3: Has symbols/numbers/randomness
        if re.search(r"[0-9@._-]", username):
            status |= 0b100

        return status

    def _load_web_text(self, csv_path: str) -> str:
        """
        Load web text from a CSV file.

        Args:
            csv_path (str): Path to the CSV file.

        Returns:
            str: Concatenated content from the CSV.

        Raises:
            FileNotFoundError: If the CSV file doesn't exist.
            ValueError: If the CSV doesn't have the required columns.
        """
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        try:
            with open(csv_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if not {"id", "content", "url"}.issubset(set(reader.fieldnames or [])):
                    raise ValueError("CSV must contain columns: id, content, url")
                contents = []
                for row in reader:
                    if row["content"]:
                        contents.append(row["content"].lower())
            return " ".join(contents)
        except csv.Error as e:
            raise ValueError(f"Error reading CSV file: {e}")

    def _load_wordlist(self, file_path: str) -> List[str]:
        """
        Load wordlist from a file.

        Args:
            file_path (str): Path to the wordlist file.

        Returns:
            List[str]: List of words from the file.

        Raises:
            FileNotFoundError: If the wordlist file doesn't exist.
            ValueError: If there's an error reading the file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Wordlist file not found: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                words = [line.strip().lower() for line in file if line.strip()]
                return words
        # TODO: updated to have a more specific catch
        except Exception as e:
            raise ValueError(f"Error reading wordlist file: {e}")


if __name__ == "__main__":
    cdg = Credential_Generator()
    password = "frick"
    score = cdg.password_mdp.calculate_password_strength(password)
    cdg._suggest_password(password, score)
