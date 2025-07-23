# The top-level class for the ToneRank application
# @author Rylan Ahmadi (Ry305)
# Last updated 07/16/2025
# TODO: add email chain context
# TODO: possibly add manual processing by keyword for the flagged emails, just in case.

from gmailPipe import GmailPipe
from llm import GroqLlama
from toneRank_io import ToneRank_IO
import re
from termcolor import colored
import json

# Number constants for the main menu options
OPTION_1 = 1
OPTION_2 = 2
OPTION_3 = 3
OPTION_4 = 4
OPTION_5 = 5
OPTION_6 = 6
OPTION_7 = 7
OPTION_8 = 8
OPTION_9 = 9
OPTION_10 = 10

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


def urgency_prompt_C1(email, client, prompt_data):
    """ Uses the GroqLlama class to prompt Llama3 to calculate an urgency score for a specific Category 1 email. """

    prompt3 = prompt_data['prompts']['uscore_prompt_one']['prompt'] + "Email subject: " + email.subject + "\n" + "Email body: " + email.body + "\n"
    
    # Attempt to query Llama3, and let the calling method know if this fails
    try:
        response = GroqLlama.get_cached_llama_response(client, prompt3)
        return float(response) # Return uscore
    except Exception as e:
        raise Exception(f"Query failed: {e}.")

def urgency_prompt_C2(email, client, prompt_data):
    """ Uses the GroqLlama class to prompt Llama3 to calculate an urgency score for a specific Category 2 email. """

    # Prompt with examples (potential bias)
    prompt = prompt_data['prompts']['uscore_prompt_two']['prompt'] + "Email subject: " + email.subject + "\n" + "Email body: " + email.body + "\n"
    
    # Attempt to query Llama3, and let the calling method know if this fails
    try:
        response = GroqLlama.get_cached_llama_response(client, prompt)
    except Exception as e:
        raise Exception("Query failed.")
    return float(response) # Return uscore

def generate_todo_list(top_ten_email_list, client, prompt_data):

    """ Generates a to-do list for the user using a string representing emails and a client. """

    prompt = prompt_data['prompts']['todo_prompt']['prompt'] + top_ten_email_list 

    # Attempt to query Llama3, and let the calling method know if this fails
    try:
        response = GroqLlama.get_cached_llama_response(client, prompt)
    except Exception as e:
        raise Exception("Query failed.")
    return response # Return list of tasks

def get_keyword_modifier(email):

    """ Utilizes the list of user-specified keywords to generate a modifier for the urgency score. For each keyword
     present, a specific weight will be added (by default, 1) """
    
    uscore_modifier = 0.0

    subject = email.subject.lower()
    body = email.body.lower()

    for word in ToneRank_IO.keywords.keys():
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.findall(pattern, subject) or word in re.findall(pattern, body):
            uscore_modifier = uscore_modifier + ToneRank_IO.keywords[word]

    return uscore_modifier


####################################################################################################################


def whitelist_emails():
    """ Adds user-specified emails to a whitelist which composes Category 0. """

    emails = input("Enter emails in a space-separated list (e.g. \"johndoe@gmail.com janedoe@yahoo.com\"):\n")
    email_list = emails.split()
    # For each email
    for e in email_list:
        if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", e) is None: # If email is invalid
            print(colored(f"Invalid email: {e}", "red"))
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
        while True:
            try: # Prompt user for weight, break loop on failure
                weight = float(input(f"Enter the weight of the keyword \"{w}\" (default 1): "))
                break
            except: # Error message
                print( colored("Please enter an decimal number.", "red") )
        ToneRank_IO.add_keyword(w, weight) # Add the word to the keywords list
    print() # Add newline

def remove_keywords():
    """ Removes keywords from your list. """

    keywords = input("Enter keywords in a space-separated list (e.g. \"urgent ToneRank now\"):\n")
    keyword_list = keywords.split()
    # For each keyword
    for w in keyword_list: 
        ToneRank_IO.remove_keyword(w) # Add the word to the keywords list
    print() # Add newline

def update_priority_report():
    """ Update various parts of the priority report. """

    while True:
        try:
            top_email_size = int(input("\nThe priority report includes a shortlist of the most urgent emails.\n" \
                                "How many emails do you want in this list (default 5)? "))
            if (top_email_size < ToneRank_IO.MIN_TOP_EMAIL_SIZE or top_email_size > ToneRank_IO.MAX_TOP_EMAIL_SIZE):
                raise ValueError
            ToneRank_IO.top_email_size = top_email_size
            break
        except Exception as e:
            print(colored(f"\nPlease enter an integer number from {ToneRank_IO.MIN_TOP_EMAIL_SIZE} to {ToneRank_IO.MAX_TOP_EMAIL_SIZE} (inclusive)", "red"))
    while True:
        try:
            todo_sample_size = int(input("\nThe priority report includes a todo list made from top emails.\n" \
                                "How many emails do you want to be used when making this list (default 10)? "))
            if (todo_sample_size < ToneRank_IO.MIN_TODO_SAMPLE_SIZE or todo_sample_size > ToneRank_IO.MAX_TODO_SAMPLE_SIZE):
                raise ValueError
            ToneRank_IO.todo_list_sample_size = todo_sample_size
            print() # For the newline
            break
        except Exception as e:
            print(colored(f"\nPlease enter an integer number from {ToneRank_IO.MIN_TODO_SAMPLE_SIZE} to {ToneRank_IO.MAX_TODO_SAMPLE_SIZE} (inclusive)", "red"))


####################################################################################################################


def toneRank_main():
    """ Handles the main flow, from email retrieval to priority report. """

    emails = GmailPipe.get_emails_last_24_hours() # get emails

    # If there were no emails to rank
    if len(emails) == 0:
        print(colored("No emails found from the past 24 hours.\n"))
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

    # Open prompts.json
    with open('prompts.json', 'r') as f:
        prompt_data = json.load(f)

    flagged_emails = [] # Declare a list used to hold all Category 1 emails which could not be processed
    cat0_key_emails = [] # Declare a list to hold Category 0 emails which include keywords
    cat1_key_emails = [] # Declare a list to hold Category 1 emails which include keywords
    cat2_key_emails = [] # Declare a list to hold Category 2 emails which include keywords

    # Calculate urgency score for each email in category 1
    for e in cat0_emails:
        try:
            uscore = urgency_prompt_C1(e, llama3, prompt_data) # get the base urgency score using helper method
            uscore_modifier = get_keyword_modifier(e) # use helper method to get a modifier for the uscore
            
            if uscore_modifier > 0.0: # If keywords were found
                e.subject = e.subject + " ☆" # Add a star to indicate keyword presence
                cat0_emails.remove(e) # Remove from main list
                cat0_key_emails.append(e) # Move to keyword sub-list

            uscore = uscore + uscore_modifier
            e.uscore = uscore # set uscore
        except Exception:
            flagged_emails.append(e) # if email failed to be processed
    for e in cat1_emails:
        try:
            uscore = urgency_prompt_C1(e, llama3, prompt_data) # get the base urgency score using helper method
            uscore_modifier = get_keyword_modifier(e) # use helper method to get a modifier for the uscore
            
            if uscore_modifier > 0.0: # If keywords were found
                e.subject = e.subject + " ☆" # Add a star to indicate keyword presence
                cat1_emails.remove(e) # Remove from main list
                cat1_key_emails.append(e) # Move to keyword sub-list

            uscore = uscore + uscore_modifier
            e.uscore = uscore # set uscore
        except Exception:
            flagged_emails.append(e) # if email failed to be processed
    # Calculate urgency score for each email in category 2
    for e in cat2_emails:
        try:
            uscore = urgency_prompt_C2(e, llama3, prompt_data) # get the base urgency score using helper method
            uscore_modifier = get_keyword_modifier(e) # use helper method to get a modifier for the uscore
            
            if uscore_modifier > 0.0: # If keywords were found
                e.subject = e.subject + " ☆" # Add a star to indicate keyword presence
                cat2_emails.remove(e) # Remove from main list
                cat2_key_emails.append(e) # Move to keyword sub-list

            uscore = uscore + uscore_modifier
            e.uscore = uscore # set uscore
        except Exception:
            flagged_emails.append(e) # if email failed to be processed

    # Create overall email ranking
    emails_ranked = sorted(cat0_key_emails) + sorted(cat0_emails) + sorted(cat1_key_emails) + \
        sorted(cat1_emails) + sorted(cat2_key_emails) + sorted(cat2_emails)
    
    # Generate a to-do list from top-priority emails

    todo_list_sample_emails = ""
    for i in range(ToneRank_IO.todo_list_sample_size): # For up to the first 10 emails
        if len(emails_ranked) > i:
            # Make a string representing the email's contents
            todo_list_sample_emails = todo_list_sample_emails + f"Subject #{i+1}: " + \
                emails_ranked[i].subject + f"\nBody #{i+1}: " + emails_ranked[i].body + "\n"
    tasks = generate_todo_list(todo_list_sample_emails, llama3, prompt_data) # generate the tasks

    # Print Priority Report

    print(colored("\n=====================================", attrs=["bold"]))
    print(colored("          PRIORITY REPORT            ", attrs=["bold"]))
    print(colored("=====================================\n", attrs=["bold"]))

    # Print to-do list
    print(colored("To-Do List:", attrs=["bold", "underline"]))
    print(colored(tasks + "\n"))

    # Print top 5 most urgent emails (if there were more than 5 total)
    if len(emails_ranked) >= ToneRank_IO.top_email_size:
        print(colored(f"Top {ToneRank_IO.top_email_size} emails to read Right Now:", attrs=["bold", "underline"]))
        count = 1
        for i in range(ToneRank_IO.top_email_size):
            print(f"{count}. {emails_ranked[i]}")
            count = count + 1
        print("")

    # Print total email ranking
    print(colored("All emails by order of urgency:", attrs=["bold", "underline"]))
    count = 1
    for e in emails_ranked:
        print(f"{count}. {e}")
        count = count + 1
    print("")

    # If some emails could not be processed, print them
    if len(flagged_emails) > 0:
        print(colored("Emails which could not be processed by the system (urgency unknown):", attrs=["bold", "underline"]))
        count = 1
        for e in flagged_emails:
            print(f"{count}. {e}")
            count = count + 1
        print("")

if __name__ == '__main__':
    print("\n")
    print(colored("@@@@@@@@@    @@@@@@@    @@@   @@@   @@@@@@@@@      @@@@@@@@     @@@@@@@    @@@   @@@   @@@   @@@", "red"))
    print(colored("   @@@      @@@   @@@   @@@@  @@@   @@@            @@@   @@@   @@@   @@@   @@@@  @@@   @@@  @@@ ", "red"))
    print(colored("   @@@      @@@   @@@   @@@ @ @@@   @@@            @@@   @@@   @@@   @@@   @@@ @ @@@   @@@ @@@  ", "red"))
    print(colored("   @@@      @@@   @@@   @@@  @@@@   @@@@@@@@@      @@@@@@@@    @@@@@@@@@   @@@  @@@@   @@@@@@   ", "red"))
    print(colored("   @@@      @@@   @@@   @@@   @@@   @@@            @@@ @@@     @@@   @@@   @@@   @@@   @@@ @@@  ", "red"))
    print(colored("   @@@      @@@   @@@   @@@   @@@   @@@            @@@  @@@    @@@   @@@   @@@   @@@   @@@  @@@ ", "red"))
    print(colored("   @@@       @@@@@@@    @@@   @@@   @@@@@@@@@      @@@   @@@   @@@   @@@   @@@   @@@   @@@   @@@", "red"))
    print("\n")

    print(colored("\n=====================================", attrs=["bold"]))
    print(colored("            MAIN MENU                ", attrs=["bold"]))
    print(colored("=====================================\n", attrs=["bold"]))

    try:
        ToneRank_IO.load_remote_data() # Load data from file
    except Exception as e:
        print(f"Error while user preferences from the file: {e}")

    while( True ):

        print(colored("1.  Add emails to high-priority list\n2.  Add keywords of special interest\n3.  Remove emails from high-priority" \
              " list\n4.  Remove keywords from list\n5.  List your high-priority emails\n6.  List your keywords\n" \
              "7.  List priority report settings" "\n8.  Customise priority report \n9.  Run ToneRank\n10. Quit\n"))

        response = input(colored("Select an option: ", attrs=["bold"])) # get user selection
        try:
            responseNum = int(response) # Parse to an integer
            if responseNum < OPTION_1 or responseNum > OPTION_10: # If integer is out of bounds
                raise ValueError
        except: # If the input was invalid
            print(colored("Please enter a number from 1-10\n", "red"))
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
            print(colored(f"Emails you have marked as high-priority:\n{ToneRank_IO.email_whitelist}\n"))
        elif responseNum == OPTION_6:
            keystr = ""
            for key in ToneRank_IO.keywords.keys():
                keystr = keystr + f"{key} ({ToneRank_IO.keywords[key]}), "
            print(f"Keywords you have marked as high-priority:\n{keystr}\n")
        elif responseNum == OPTION_7:
            print(colored(f"Priority report will highlight the top {ToneRank_IO.top_email_size} emails, and " \
              f"makes a to-do list from the top {ToneRank_IO.todo_list_sample_size} emails\n"))
        elif responseNum == OPTION_8: 
            update_priority_report()
        elif responseNum == OPTION_9: 
            toneRank_main()
            break
        elif responseNum == OPTION_10:
            break
    try:
        ToneRank_IO.save_local_data()
    except Exception as e:
        print(f"Error while saving user preferences to the file: {e}")
