import email
from config import filters

# Returns an array containing the names of all available mailboxes on the
# selected imap server
def get_mailboxes(imap):
    # An array that will hold the names of all available mailboxes
    mailboxes = []

    # Fetch all folders from the imap server
    response_code, folders = imap.list()

    # Loop through all the folders, extract their names and dump them
    # into @mailboxes
    for folder_details_raw in folders:
        folder_details = folder_details_raw.decode().split()
        mailboxes.append(folder_details[-1].replace('"',''))

    # return the array of available mailboxes
    return mailboxes

# Returns the sender of the given message
def extract_sender(imap, message_number):
    # Fetch the given message based on the number
    _, msg = imap.fetch(message_number, '(RFC822)')

    # Parse the data bytes
    mail = email.message_from_bytes(msg[0][1])

    # Return the sender field
    return mail["from"]

# Analyzes the emails in the given mailbox.
# It returns a dictionary containing the address of the sender
# as the key, and the number of emails received from them as the
# value.
def analyze_mailbox(imap, mailbox):
    # Select the given mailbox as to only analyze it
    imap.select(mailbox)

    # A dictionary that will contain pairs in this format:
    # { "sender_address@provider.whatever": number_of_emails_received_from_them }
    senders = {}

    # Fetch all message numbers in the given mailbox
    _, message_numbers_raw = imap.search(None, 'ALL')

    # Loop through all available emails
    for message_number in message_numbers_raw[0].split():
        # Extract the email sender
        sender = extract_sender(imap, message_number)

        # If the doesn't exist in the dictionary, add it with a value of 1
        # Otherwise, increment the associated number
        if sender not in senders:
            senders[sender] = 1
        else:
            senders[sender] += 1

    return senders