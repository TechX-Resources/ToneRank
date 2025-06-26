# Utility class for handling I/O, specifically storing data in files
# @author Rylan Ahmadi (Ry305)
# Last updated 06/26/2025

import csv
import os
from typing import List

class ToneRank_IO:

    """ Used to manage I/O requests involved with running the ToneRank application. Primarily used
     for loading, accessing, and saving the lists of user-defined keywords and whitelisted emails. """

    KEYWORD_FILE_NAME = "keywords.txt" # the name of the file used to save keywords
    EMAIL_WHITELIST_FILE_NAME = "whitelist.txt" # the name of the file used to save whitelisted emails
    MAX_KEYWORDS = 100 # the maximum number of keywords which can be held in the system at a given time

    keywords: List[str] = [] # Stores user-inputted keywords to be used in urgency calculation
    email_whitelist: List[str] = [] # Stores emails the user has whitelisted for Category 0

    @staticmethod
    def initialize_files():
        """ Ensure required files exist before attempting to load """
        for filename in [ToneRank_IO.KEYWORD_FILE_NAME, ToneRank_IO.EMAIL_WHITELIST_FILE_NAME]:
            if not os.path.exists(filename):
                try:
                    with open(filename, 'x'):
                        pass # just create the file
                except Exception as e:
                    print(f"File initialization error: {e}")
                    raise

    @staticmethod
    def add_keyword(keyword):
        """ Adds a new keyword to the list if it is not a duplicate, and if the capacity has not
         been reached. """
        if len(ToneRank_IO.keywords) >= ToneRank_IO.MAX_KEYWORDS:
            print(f"Cannot add keyword. Maximum number of keywords ({ToneRank_IO.MAX_KEYWORDS}) reached.")
            return # exit
        keyword = keyword.strip().lower() # Normalize the keyword
        if keyword not in ToneRank_IO.keywords:
            ToneRank_IO.keywords.append(keyword)
        else:
            print(f"Keyword \"{keyword}\" has already been added.")
    
    @staticmethod
    def remove_keyword(keyword):
        """ Removes a keyword from the list. """
        keyword = keyword.strip().lower() # Normalize the keyword
        if keyword in ToneRank_IO.keywords:
            ToneRank_IO.keywords.remove(keyword)
    
    @staticmethod
    def add_email_to_whitelist(email):
        """ Add an email to the whitelist if it is not already present. """
        email = email.strip().lower() # Normalize email
        if email not in ToneRank_IO.email_whitelist:
            ToneRank_IO.email_whitelist.append(email)
        else:
            print(f"Email \"{email}\" has already been added.")

    @staticmethod
    def remove_email(email):
        """ Removes an email from the whitelist. """
        email = email.strip().lower() # Normalize the keyword
        if email in ToneRank_IO.email_whitelist:
            ToneRank_IO.email_whitelist.remove(email)
    
    @staticmethod
    def load_remote_data():
        try:
            # Initialize files
            ToneRank_IO.initialize_files()
            # Load keywords
            with open(ToneRank_IO.KEYWORD_FILE_NAME, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row: # skip empty rows
                        ToneRank_IO.keywords.append(row[0])
            # Load whitelisted emails
            with open(ToneRank_IO.EMAIL_WHITELIST_FILE_NAME, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row: # skip empty rows
                        ToneRank_IO.email_whitelist.append(row[0])
        except Exception as e:
            print(f"Error when loading files: {e}")
            raise

    @staticmethod
    def save_local_data():
        """ Save keywords and whitelisted emails to the file. """
        try:
            with open(ToneRank_IO.KEYWORD_FILE_NAME, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                for w in ToneRank_IO.keywords:
                    csv_writer.writerow([w]) # each item on its own row
        except Exception as e:
            print(f"Error when saving keywords: {e}")
            raise
        try:  
            with open(ToneRank_IO.EMAIL_WHITELIST_FILE_NAME, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                for e in ToneRank_IO.email_whitelist:
                    csv_writer.writerow([e])
        except Exception as e:
            print(f"Error when saving email whitelist: {e}")
            raise


if __name__ == '__main__':
    ToneRank_IO.load_remote_data()
    print(ToneRank_IO.get_keyword_string())