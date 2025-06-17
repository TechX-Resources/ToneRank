# The top-level class for the ToneRank application
# @author Rylan Ahmadi (Ry305)
# Last updated 06/16/2025

from gmailPipe import GmailPipe

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

if __name__ == '__main__':
    emails = GmailPipe.get_emails_last_24_hours() # get emails

    # split into their categories
    cat1_emails = []
    cat2_emails = []
    for e in emails:
        domain = e.sender.split("@")[1] # get the part of the sender data after the '@'
        if (domain[len(domain) - 1] == '>'):
            domain = domain[0:len(domain)-1] # remove the closing '>', if there is one
        if domain in public_email_domains: 
            cat2_emails.append(e) # If the email is a public domain
        else:
            cat1_emails.append(e) # If the email is NOT a public domain

    # TODO: remove this line
    # Print number of messages
    print(f"Found {len(emails)} messages from the past 24 hours ({len(cat1_emails)} from C1, {len(cat2_emails)} from C2).")

    # Use llm.py to get a Llama3 client
    from llm import GroqLlama
    llama3 = GroqLlama()

    flagged_emails = [] # Declare a list used to hold all Category 1 emails which could not be processed

    # TODO: Create separate prompt functions with different prompts for C1 and C2

    # Calculate urgency score for each email in category 1
    try:
        for e in cat1_emails:
            uscore = urgency_prompt_C1(e, llama3) # get the urgency score using helper method
            e.uscore = uscore # set uscore
        # Calculate urgency score for each email in category 2
        for e in cat2_emails:
            uscore = urgency_prompt_C2(e, llama3) # get the urgency score using helper method
            e.uscore = uscore # set uscore
    except Exception as ex:
        if ex == "Query failed.":
            flagged_emails.append(e) # if email failed to be processed
    
    # Create overall email ranking
    emails_ranked = sorted(cat1_emails) + sorted(cat2_emails)

    # TODO: possibly add manual processing by keyword for the flagged emails, just in case.

    # Print Priority Report

    print("\n=====================================")
    print("          PRIORITY REPORT            ")
    print("=====================================\n")

    print("Top 5 emails to read Right Now:")
    count = 1
    for i in range(5):
        print(f"{count}. {emails_ranked[i]}")
        count = count + 1
    print("")

    print("All emails by order of urgency:")
    count = 1
    for e in emails_ranked:
        print(f"{count}. {e}")
        count = count + 1
    print("")

    # If some emails could not be processed
    if len(flagged_emails) != 0:
        print("Emails which could not be processed by the system (urgency unknown):")
        count = 1
        for e in flagged_emails:
            print(f"{count}. {e}")
            count = count + 1
        print("")

