from typing import Tuple


class CredentialMDP:
    """
    This class is responsbile for managing the Markov Decision Process for generating credentials

    Attributes:
        - `self.order`
        - `self.gamma`
        - `self.q_values: Dict[str, Dict[Tuple[str, str], float]]`
        - `self.state_transitions: Dict[str, Dict[str, Set[str]]]`
        - `self.used_usernames: Set[str]`
        - `self.epsilon: float`
        - `self.learning_rate: float`
        - `self.initial_states: List[str]`
    """

    def calculate_password_strength(self, password: str) -> float:
        """
        Calculate the strength of a password based on various criteria.

        The strength score ranges from 0.0 to 1.0, with higher scores indicating stronger passwords.
        The following criteria contribute to the password strength:
        - Length (≥ 12 characters): +0.3
        - Contains uppercase letter: +0.2
        - Contains digit: +0.2
        - Contains special character (!@#$%^&*): +0.2
        - Has at least 8 unique characters: +0.1

        Args:
            password (str): The password string to evaluate

        Returns:
            float: A score between 0.0 and 1.0 indicating password strength
        """
        pass

    def calculate_username_quality(self, username: str) -> float:
        """
        Calculate the quality score for a username based on multiple criteria.

        The quality score ranges from 0.0 to 1.0, with higher scores indicating better usernames.
        The following criteria contribute to the username quality:
        - Length (≥ 6 characters): +0.3
        - Uniqueness (not in used_usernames): +0.4
        - Starts with lowercase letter: +0.2
        - Contains no whitespace: +0.1

        Args:
            username (str): The username string to evaluate

        Returns:
            float: A score between 0.0 and 1.0 indicating username quality
        """
        pass

    def update_q_value(
        self, state: str, actino: str, next_char: str, reward: float
    ) -> None:
        """
        Update the Q-value for a state-action-result tuple using the Q-learning algorithm.

        This method implements the Q-learning update formula:
        Q(s,a,r) ← Q(s,a,r) + α * [reward + γ * max Q(s',a',r') - Q(s,a,r)]

        The function calculates the maximum Q-value for all possible actions in the next state,
        then uses this to update the Q-value of the current state-action-result combination.

        Args:
            state (str): The current state
            action (str): The action taken in the current state
            next_char (str): The result/observation after taking the action
            next_state (str): The resulting state after taking the action
            reward (float): The reward received for this transition

        Returns:
            None: The method updates the internal q_values dictionary directly

        Notes:
            - Uses the class attributes learning_rate (α) and gamma (γ) for calculations
            - If the next state has no possible actions, the max_next_q defaults to 0
        """
        pass

    def choose_action(self, state: str) -> Tuple[str, str]:
        """
        Select an action to take from the current state using an epsilon-greedy policy.

        This method implements exploration vs. exploitation using the epsilon-greedy approach:
        - With probability epsilon: Choose a random action (exploration)
        - With probability (1-epsilon): Choose the action with the highest Q-value (exploitation)

        For the exploitation case, the method selects the action with the highest expected
        Q-value among all possible next characters resulting from that action.

        Args:
            state (str): The current state for which to choose an action

        Returns:
            Tuple[str, str]: A tuple containing (selected_action, expected_next_character)
            If no actions are possible, returns ("", "")

        Notes:
            - Uses the class attribute epsilon to control exploration/exploitation balance
            - If the best action has multiple possible next characters, one is chosen randomly
            - Falls back to random selection if no Q-values are available for valid actions
        """
        pass
