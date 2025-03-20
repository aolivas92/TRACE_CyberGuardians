from .credential_generator import Credential_Generator

# Initialize Credential Generator (wordlist & csv optional)
generator = Credential_Generator(csv_path="data.csv", wordlist_path="wordlist.txt")

# Generate 10 credentials
credentials = generator.generate_credentials(count=10)

# Print the generated credentials
for i, (username, password) in enumerate(credentials, 1):
    print(f"{i}. Username: {username}, Password: {password}")
