# TRACE

TRACE is a tool that automates web scraping, analyzes data, and generates username-password pairs based on statistical and learning-based models.

## Dependencies

Install Steps:
-	Clone the repository or download the provided files.
-	Navigate to the project directory.
- Required Python libraries:
  - `beautifulsoup4`
  - `numpy`
  - `requests`
- Install dependencies by running the following command: 
```bash
pip install -r requirements.txt
```

## How To Run
1.	Prepare Input Files:
-	wordlist.txt: Contains sample words for training.
-	site_list.csv: Has a id and website.
2.	Run the Script:
-	Save the script and run the following command:
```bash
python md3.py
```
## MDP 
The script processes the CSV and wordlist to build state transitions and generates credentials based on MDPs, enhancing the quality of usernames and passwords.
-	Generated Usernames and Passwords: The script generates a list of usernames and passwords based on the MDP learning process.
-	The improved credentials are printed to the console.
Example: 
```bash
Username: skipe487, Password: Computerst%
```
