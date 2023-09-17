import os

# Define the path to the dataset
dataset_path = '/home/lupe/Phishing_Email/enron_dataset/maildir'

# List all user directories
users = os.listdir(dataset_path)

# Loop through each user and their subdirectories to read emails
emails = []
for user in users:
    user_path = os.path.join(dataset_path, user)
    for dirpath, dirnames, filenames in os.walk(user_path):
        for file in filenames:
            with open(os.path.join(dirpath, file), 'r', errors='ignore') as email_file:
                email_content = email_file.read()
                emails.append(email_content)  # This will store each email's content in a list

