# The top-level class for the ToneRank application
# @author Rylan Ahmadi (Ry305)
# Last updated 06/26/2025
# TODO: make keyword weight customizable
# TODO: make the Top Five function customizable (top 3, top 10, top 1, etc.)
# TODO: add email chain context
# TODO: possibly add manual processing by keyword for the flagged emails, just in case.

from gmailPipe import GmailPipe
from llm import GroqLlama
from toneRank_io import ToneRank_IO
import re

# Number constants for the main menu options
OPTION_1 = 1
OPTION_2 = 2
OPTION_3 = 3
OPTION_4 = 4
OPTION_5 = 5
OPTION_6 = 6
OPTION_7 = 7
OPTION_8 = 8

# The default weight assigned to a user-specified keyword
DEFAULT_WEIGHT = 0.1

# A list of the top 100 public domain email addresses, accounting for approx. 75.83% of active emails
# Source: email-verify.my-addr.com/list-of-most-popular-email-domains.php
public_email_domains = {
    "gmail.com", "yahoo.com", "hotmail.com", "aol.com", "hotmail.co.uk", "hotmail.fr", 
    "msn.com", "yahoo.fr", "wanadoo.fr", "orange.fr", "comcast.net", "yahoo.co.uk", 
    "yahoo.com.br", "yahoo.co.in", "live.com", "rediffmail.com", "free.fr", "gmx.de", 
    "web.de", "yandex.ru", "ymail.com", "libero.it", "outlook.com", "uol.com.br", "bol.com.br", 
    "mail.ru", "cox.net", "hotmail.it", "sbcglobal.net", "sfr.fr", "live.fr", "verizon.net", 
    "live.co.uk", "googlemail.com", "yahoo.es", "ig.com.br", "live.nl", "bigpond.com", 
    "terra.com.br", "yahoo.it", "neuf.fr", "yahoo.de", "alice.it", "rocketmail.com", 
    "att.net", "laposte.net", "facebook.com", "bellsouth.net", "yahoo.in", "hotmail.es", 
    "charter.net", "yahoo.ca", "yahoo.com.au", "rambler.ru", "hotmail.de", "tiscali.it", 
    "shaw.ca", "yahoo.co.jp", "sky.com", "earthlink.net", "optonline.net", "freenet.de", 
    "t-online.de", "aliceadsl.fr", "virgilio.it", "home.nl", "qq.com", "telenet.be", "me.com", 
    "yahoo.com.ar", "tiscali.co.uk", "yahoo.com.mx", "voila.fr", "gmx.net", "mail.com", 
    "planet.nl", "tin.it", "live.it", "ntlworld.com", "arcor.de", "yahoo.co.id", "frontiernet.net", 
    "hetnet.nl", "live.com.au", "yahoo.com.sg", "zonnet.nl", "club-internet.fr", "juno.com", 
    "optusnet.com.au", "blueyonder.co.uk", "bluewin.ch", "skynet.be", "sympatico.ca", 
    "windstream.net", "mac.com", "centurytel.net", "chello.nl", "live.ca", "aim.com", 
    "bigpond.net.au"
}


####################################################################################################################


def urgency_prompt_C1(email, client):
    """ Uses the GroqLlama class to prompt Llama3 to calculate an urgency score for a specific Category 1 email. """

    # Prompt with examples (potential bias)
    prompt1 = "You are a personal assistant to an overworked government official. It is of vital importance " \
    "that his most urgent emails are prioritized, because he might not be able to respond to all of them. " \
    "He is now going to give you an email, and wants you to assign an Urgency Score from 0 to 10 (inclusive) " \
    "to it, with 0 corresponding to an email which might not ever require a response, and 10 being an email " \
    "which must be addressed immediately. Possible indicators of urgency could include: using all caps, an angry " \
    "or frustrated tone, and words or phrases such as 'ASAP', 'as soon as possible', 'vital', 'action required', " \
    "'immediately', 'cannot wait', and so on. " \
    "Your response should contain NO text except an integer number which is no less than 0 and no more than 10.\n\n" \
    "Email subject: " + email.subject + "\n" \
    "Email body: " + email.body + "\n"

    # Prompt without examples (no bias)
    prompt2 = "You are a personal assistant to an overworked government official. It is of vital importance " \
    "that his most urgent emails are prioritized, because he might not be able to respond to all of them. " \
    "He is now going to give you an email, and wants you to assign an Urgency Score from 0 to 10 (inclusive) " \
    "to it, with 0 corresponding to an email which might not ever require a response, and 10 being an email " \
    "which must be addressed immediately. " \
    "Your response should contain NO text except an integer number which is no less than 0 and no more than 10.\n\n" \
    "Email subject: " + email.subject + "\n" \
    "Email body: " + email.body + "\n"

    # Same with prompt1, but it asks for a decimal
    prompt3 = "You are a personal assistant to an overworked government official. It is of vital importance " \
    "that his most urgent emails are prioritized, because he might not be able to respond to all of them. " \
    "He is now going to give you an email, and wants you to assign an Urgency Score from 0 to 10 (inclusive) " \
    "to it, with 0 corresponding to an email which might not ever require a response, and 10 being an email " \
    "which must be addressed immediately. Possible indicators of urgency could include: using all caps, an angry " \
    "or frustrated tone, and words or phrases such as 'ASAP', 'as soon as possible', 'vital', 'action required', " \
    "'immediately', 'cannot wait', and so on. " \
    "Your response should contain NO text except an decimal number of the format X.X which is no less than 0.0 " \
    "and no more than 10.0.\n\n" \
    "Email subject: " + email.subject + "\n" \
    "Email body: " + email.body + "\n"

    # The same as prompt2, but it asks for a decimal
    prompt4 = "You are a personal assistant to an overworked government official. It is of vital importance " \
    "that his most urgent emails are prioritized, because he might not be able to respond to all of them. " \
    "He is now going to give you an email, and wants you to assign an Urgency Score from 0 to 10 (inclusive) " \
    "to it, with 0 corresponding to an email which might not ever require a response, and 10 being an email " \
    "which must be addressed immediately. " \
    "Your response should contain NO text except an decimal number of the format X.X which is no less than 0.0 " \
    "and no more than 10.0.\n\n" \
    "Email subject: " + email.subject + "\n" \
    "Email body: " + email.body + "\n"
    
    # Attempt to query Llama3, and let the calling method know if this fails
    try:
        response = GroqLlama.get_cached_llama_response(client, prompt3)
    except Exception as e:
        raise Exception("Query failed.")
    return float(response) # Return uscore

def urgency_prompt_C2(email, client):
    """ Uses the GroqLlama class to prompt Llama3 to calculate an urgency score for a specific Category 2 email. """

    # Prompt with examples (potential bias)
    prompt = "You are a personal assistant to a counselor and family man. He is very busy, but wants to keep up " \
    "with the most urgent of his emails from family and friends, because he might not be able to respond to all of them. " \
    "He is now going to give you an email, and wants you to assign an Urgency Score from 0 to 10 (inclusive) " \
    "to it, with 0 corresponding to an email which might not ever require a response, and 10 being an email " \
    "which must be addressed immediately. Possible indicators of urgency could include: using all caps, an angry " \
    "or frustrated tone, and words or phrases such as 'ASAP', 'as soon as possible', 'important', 'cannot wait', " \
    "'immediately', 'I need your help', 'need help', and so on. " \
    "Your response should contain NO text except an decimal number of the format X.X which is no less than 0.0 " \
    "and no more than 10.0.\n\n" \
    "Email subject: " + email.subject + "\n" \
    "Email body: " + email.body + "\n"
    
    # Attempt to query Llama3, and let the calling method know if this fails
    try:
        response = GroqLlama.get_cached_llama_response(client, prompt)
    except Exception as e:
        raise Exception("Query failed.")
    return float(response) # Return uscore

def generate_todo_list(top_ten_email_list, client):

    """ Generates a to-do list for the user using a string representing emails and a client. """

    prompt = "You are a secretary to an important leader. They do not have time to answer their emails, but need to do " \
    "all of the tasks requested of them by email. Below will be a list of up to ten emails, each with a subject line and " \
    "body. Extract a list of tasks your boss must do. Your response should include nothing except the list (no title should" \
    "be included).\n" + top_ten_email_list 

    # Attempt to query Llama3, and let the calling method know if this fails
    try:
        response = GroqLlama.get_cached_llama_response(client, prompt)
    except Exception as e:
        raise Exception("Query failed.")
    return response # Return list of tasks

def get_keyword_modifier(email):

    """ Utilizes the list of user-specified keywords to generate a modifier for the urgency score. For each keyword
     present, a specific weight will be added (by default, 0.1) """
    
    uscore_modifier = 0.0

    subject = email.subject.lower()
    body = email.body.lower()

    for word in ToneRank_IO.keywords:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.findall(pattern, subject) or word in re.findall(pattern, body):
            uscore_modifier = uscore_modifier + DEFAULT_WEIGHT

    return uscore_modifier


####################################################################################################################


def whitelist_emails():
    """ Adds user-specified emails to a whitelist which composes Category 0. """

    emails = input("Enter emails in a space-separated list (e.g. \"johndoe@gmail.com janedoe@yahoo.com\"):\n")
    email_list = emails.split()
    # For each email
    for e in email_list:
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", e) is None: # If email is invalid
            print(f"Invalid email: {e}")
        else: # If email is valid
            ToneRank_IO.add_email_to_whitelist(e) # Add the email to the whitelist
    print() # Add newline

def remove_whitelisted_emails():
    """ Removes emails from the whitelist which composes Category 0. """
    emails = input("Enter emails in a space-separated list (e.g. \"johndoe@gmail.com janedoe@yahoo.com\"):\n")
    email_list = emails.split()
    # For each email
    for e in email_list:
        ToneRank_IO.remove_email(e) # Add the email to the whitelist
    print() # Add newline

def add_keywords():
    """ Adds user-specified keywords to a list used in calculation of email urgency. """

    keywords = input("Enter keywords in a space-separated list (e.g. \"urgent ToneRank now\"):\n")
    keyword_list = keywords.split()
    # For each keyword
    for w in keyword_list:
        ToneRank_IO.add_keyword(w) # Add the word to the keywords list
    print() # Add newline

def remove_keywords():
    """ Removes keywords from your list. """

    keywords = input("Enter keywords in a space-separated list (e.g. \"urgent ToneRank now\"):\n")
    keyword_list = keywords.split()
    # For each keyword
    for w in keyword_list: 
        ToneRank_IO.remove_keyword(w) # Add the word to the keywords list
    print() # Add newline

def toneRank_main():
    """ Handles the main flow, from email retrieval to priority report. """

    emails = GmailPipe.get_emails_last_24_hours() # get emails

    # If there were no emails to rank
    if len(emails) == 0:
        print("No emails found from the past 24 hours.\n")
        return

    # split into their categories
    cat0_emails = []
    cat1_emails = []
    cat2_emails = []
    for e in emails:

        e_split = e.sender.split("<") # extract the email address
        email_address = e_split[len(e_split) - 1]
        if (email_address[len(email_address) - 1] == '>'):
            email_address = email_address[0:len(email_address)-1] # remove the closing '>', if there is one
        domain = email_address.split("@")[1] # get the part of the sender data after the '@'

        if email_address in ToneRank_IO.email_whitelist:
            cat0_emails.append(e) # If the email is whitelisted
        elif domain in public_email_domains: 
            cat2_emails.append(e) # If the email is a public domain
        else:
            cat1_emails.append(e) # If the email is NOT a public domain

    # Print number of messages
    # print(f"Found {len(emails)} messages from the past 24 hours ({len(cat0_emails)} from C0, {len(cat1_emails)} from C1, {len(cat2_emails)} from C2).")

    # Use llm.py to get a Llama3 client
    llama3 = GroqLlama()

    flagged_emails = [] # Declare a list used to hold all Category 1 emails which could not be processed

    # Calculate urgency score for each email in category 1
    for e in cat0_emails:
        try:
            uscore = urgency_prompt_C1(e, llama3) # get the base urgency score using helper method
            uscore_modifier = get_keyword_modifier(e) # use helper method to get a modifier for the uscore
            uscore = uscore + uscore_modifier
            e.uscore = uscore # set uscore
        except Exception as ex:
            if ex == "Query failed.":
                flagged_emails.append(e) # if email failed to be processed
    for e in cat1_emails:
        try:
            uscore = urgency_prompt_C1(e, llama3) # get the base urgency score using helper method
            uscore_modifier = get_keyword_modifier(e) # use helper method to get a modifier for the uscore
            uscore = uscore + uscore_modifier
            e.uscore = uscore # set uscore
        except Exception as ex:
            if ex == "Query failed.":
                flagged_emails.append(e) # if email failed to be processed
    # Calculate urgency score for each email in category 2
    for e in cat2_emails:
        try:
            uscore = urgency_prompt_C2(e, llama3) # get the base urgency score using helper method
            uscore_modifier = get_keyword_modifier(e) # use helper method to get a modifier for the uscore
            uscore = uscore + uscore_modifier
            e.uscore = uscore # set uscore
        except Exception as ex:
            if ex == "Query failed.":
                flagged_emails.append(e) # if email failed to be processed
    
    # Create overall email ranking
    emails_ranked = sorted(cat0_emails) + sorted(cat1_emails) + sorted(cat2_emails)

    # Generate a to-do list from top-priority emails

    top_ten_emails_text = ""
    for i in range(10): # For up to the first 10 emails
        if len(emails_ranked) > i:
            # Make a string representing the email's contents
            top_ten_emails_text = top_ten_emails_text + \
            f"Subject #{i+1}: " + emails_ranked[i].subject + f"\nBody #{i+1}: " + emails_ranked[i].body + "\n"

    tasks = generate_todo_list(top_ten_emails_text, llama3) # generate the tasks

    # Print Priority Report

    print("\n=====================================")
    print("          PRIORITY REPORT            ")
    print("=====================================\n")

    # Print to-do list
    print("To-Do List:\n" + tasks + "\n")

    # Print top 5 most urgent emails (if there were more than 5 total)
    if len(emails_ranked) >= 5:
        print("Top 5 emails to read Right Now:")
        count = 1
        for i in range(5):
            print(f"{count}. {emails_ranked[i]}")
            count = count + 1
        print("")

    # Print total email ranking
    print("All emails by order of urgency:")
    count = 1
    for e in emails_ranked:
        print(f"{count}. {e}")
        count = count + 1
    print("")

    # If some emails could not be processed, print them
    if len(flagged_emails) != 0:
        print("Emails which could not be processed by the system (urgency unknown):")
        count = 1
        for e in flagged_emails:
            print(f"{count}. {e}")
            count = count + 1
        print("")

if __name__ == '__main__':
    print("\n")
    print("@@@@@@@@@    @@@@@@@    @@@   @@@   @@@@@@@@@      @@@@@@@@     @@@@@@@    @@@   @@@   @@@   @@@")
    print("   @@@      @@@   @@@   @@@@  @@@   @@@            @@@   @@@   @@@   @@@   @@@@  @@@   @@@  @@@ ")
    print("   @@@      @@@   @@@   @@@ @ @@@   @@@            @@@   @@@   @@@   @@@   @@@ @ @@@   @@@ @@@  ")
    print("   @@@      @@@   @@@   @@@  @@@@   @@@@@@@@@      @@@@@@@@    @@@@@@@@@   @@@  @@@@   @@@@@@   ")
    print("   @@@      @@@   @@@   @@@   @@@   @@@            @@@ @@@     @@@   @@@   @@@   @@@   @@@ @@@  ")
    print("   @@@      @@@   @@@   @@@   @@@   @@@            @@@  @@@    @@@   @@@   @@@   @@@   @@@  @@@ ")
    print("   @@@       @@@@@@@    @@@   @@@   @@@@@@@@@      @@@   @@@   @@@   @@@   @@@   @@@   @@@   @@@")
    print("\n")

    print("\n=====================================")
    print("            MAIN MENU                ")
    print("=====================================\n")

    try:
        ToneRank_IO.load_remote_data() # Load data from file
    except Exception as e:
        print(f"Error while loading keywords and email whitelist from the file: {e}")

    while( True ):

        print("1. Add emails to high-priority list\n2. Add keywords of special interest\n3. Remove emails from high-priority" \
              " list\n4. Remove keywords from list\n5. List your high-priority emails\n6. List your keywords\n7. Run ToneRank" \
              "\n8. Quit\n")

        response = input("Select an option: ") # get user selection
        try:
            responseNum = int(response) # Parse to an integer
            if responseNum < OPTION_1 or responseNum > OPTION_8: # If integer is out of bounds
                raise ValueError
        except: # If the input was invalid
            print("Please enter a number from 1-4\n")
            continue

        if responseNum == OPTION_1: # If user entered option 1
            whitelist_emails()
        elif responseNum == OPTION_2: # If user entered option 2
            add_keywords()
        elif responseNum == OPTION_3:
            remove_whitelisted_emails()
        elif responseNum == OPTION_4:
            remove_keywords()
        elif responseNum == OPTION_5:
            print(f"Emails you have marked as high-priority:\n{ToneRank_IO.email_whitelist}\n")
        elif responseNum == OPTION_6:
            print(f"Keywords you have marked as high-priority:\n{ToneRank_IO.keywords}\n")
        elif responseNum == OPTION_7:
            toneRank_main()
            break
        elif responseNum == OPTION_8: 
            break
    try:
        ToneRank_IO.save_local_data()
    except Exception as e:
        print(f"Error while saving keywords and email whitelist to the file: {e}")
