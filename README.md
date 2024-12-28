# TRACE

TRACE is a tool that automates web scraping, analyzes data, and generates username-password pairs based on statistical and learning-based models.

## Dependencies

To run TRACE, ensure you have the following dependencies installed:

- Python
- Required Python libraries:
  - `beautifulsoup4`
  - `numpy`
  - `requests`

## How to Run
Prepare the input files:
- A wordlist.txt file containing a list of words for generating credentials.
Run the MDP:
```bash
python md3.py
```
MDP: The script processes the CSV and wordlist to build state transitions and generates credentials based on MDPs, enhancing the quality of usernames and passwords.

Run the Markov Chain:
```bash
python markovChain.py
```
Markov Chain: The script scrapes text from URLs, generates a web_text.csv file, and uses a wordlist to train Markov models for credential generation.
