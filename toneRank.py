# The top-level class for the ToneRank application
# @author Rylan Ahmadi (Ry305)
# Last updated 06/06/2025

from gmailPipe import GmailPipe

# A list of the top 100 public domain email addresses, accounting for approx. 75.83% of active emails
# This list was derived from https://email-verify.my-addr.com/list-of-most-popular-email-domains.php
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

if __name__ == '__main__':
    emails = GmailPipe.get_emails_last_24_hours() # get emails
    print(f"Found {len(emails)} messages from the past 24 hours.") # Print number of messages

    # split into their categories
    cat1_emails = []
    cat2_emails = []
    for e in emails:
        domain = e.sender.split("@")[1] # get the part of the sender data after the '@'
        domain = domain[0:len(domain)-1] # remove the closing '>'
        if domain in public_email_domains: 
            cat2_emails.append(e) # If the email is a public domain
        else:
            cat1_emails.append(e) # If the email is NOT a public domain

    # TODO: calculate urgency score for each email

    # TODO: rank each category by urgency

    # TODO: merge categories back together