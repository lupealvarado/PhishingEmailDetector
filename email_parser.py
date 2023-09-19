import os
import email
import pandas as pd

# Define the path to the dataset
dataset_path = '/home/lupe/Phishing_Email/enron_dataset/maildir'

# List all user directories
users = os.listdir(dataset_path)

# Define a function to parse emails
def parse_email(email_content):
    msg = email.message_from_string(email_content)
    
    # Extract metadata
    subject = msg['subject']
    from_address = msg['from']
    to_address = msg['to']
    
    # Extract email body
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            if 'attachment' not in content_disposition and 'text/plain' in content_type:
                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    
    return from_address, to_address, subject, body

# Loop through each user and their subdirectories to read emails
parsed_emails = []

for user in users:
    user_path = os.path.join(dataset_path, user)
    for dirpath, dirnames, filenames in os.walk(user_path):
        for file in filenames:
            with open(os.path.join(dirpath, file), 'r', errors='ignore') as email_file:
                email_content = email_file.read()
                from_address, to_address, subject, body = parse_email(email_content)
                parsed_emails.append([from_address, to_address, subject, body])

# Convert the parsed emails into a pandas DataFrame
df_emails = pd.DataFrame(parsed_emails, columns=['From', 'To', 'Subject', 'Body'])

# Save the DataFrame to a CSV file
df_emails.to_csv('parsed_emails.csv', index=False)


