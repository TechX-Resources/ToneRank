# Utility class for handling I/O, specifically storing data in files
# @author Rylan Ahmadi (Ry305)
# Last updated 06/29/2025

import csv
import os
from typing import List

class ToneRank_IO:

    """ Used to manage I/O requests involved with running the ToneRank application. Primarily used
     for loading, accessing, and saving the lists of user-defined keywords and whitelisted emails. """

    KEYWORD_FILE_NAME = "keywords.txt" # the name of the file used to save keywords
    EMAIL_WHITELIST_FILE_NAME = "whitelist.txt" # the name of the file used to save whitelisted emails
    PRIORITY_REPORT_FILE_NAME = "report.txt"
    MAX_KEYWORDS = 100 # the maximum number of keywords which can be held in the system at a given time

    LEN_KW_ROWS = 2 # the length of a row in a csv file for keywords

    # Default settings for priority report
    MIN_TOP_EMAIL_SIZE = 1
    MAX_TOP_EMAIL_SIZE = 10
    DEFAULT_TOP_EMAIL_SIZE = 5
    MIN_TODO_SAMPLE_SIZE = 1
    MAX_TODO_SAMPLE_SIZE = 20
    DEFAULT_TODO_SAMPLE_SIZE = 10

    keywords: dict[str, float] = {} # Stores user-inputted keywords to be used in urgency calculation
    email_whitelist: List[str] = [] # Stores emails the user has whitelisted for Category 0
    top_email_size: int # The number of emails to be used in "Top X emails to read Right Now"
    todo_list_sample_size: int # The number of emails to be used when making a to-do list

    @staticmethod
    def initialize_files():
        """ Ensure required files exist before attempting to load """
        for filename in [ToneRank_IO.KEYWORD_FILE_NAME, ToneRank_IO.EMAIL_WHITELIST_FILE_NAME, 
                         ToneRank_IO.PRIORITY_REPORT_FILE_NAME]:
            if not os.path.exists(filename):
                try:
                    with open(filename, 'x'):
                        pass # just create the file
                except Exception as e:
                    print(f"File initialization error: {e}")
                    raise

    @staticmethod
    def add_keyword(keyword, weight):
        """ Adds a new keyword to the list if it is not a duplicate, and if the capacity has not
         been reached. """
        if len(ToneRank_IO.keywords) >= ToneRank_IO.MAX_KEYWORDS:
            print(f"Cannot add keyword. Maximum number of keywords ({ToneRank_IO.MAX_KEYWORDS}) reached.")
            return # exit
        keyword = keyword.strip().lower() # Normalize the keyword
        # Add the keyword (and its weight) to the list
        if keyword not in ToneRank_IO.keywords:
            ToneRank_IO.keywords[keyword] = weight
        else:
            print(f"Keyword \"{keyword}\" has already been added.")
    
    @staticmethod
    def remove_keyword(keyword):
        """ Removes a keyword from the list. """
        keyword = keyword.strip().lower() # Normalize the keyword
        if keyword in ToneRank_IO.keywords:
            del ToneRank_IO.keywords[keyword]
    
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
        """ Loads data saved to file from previous runs of the application. """
        try:
            # Initialize files
            ToneRank_IO.initialize_files()
            # Load keywords
            with open(ToneRank_IO.KEYWORD_FILE_NAME, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row and len(row) >= ToneRank_IO.LEN_KW_ROWS: # skip empty rows
                        keyword = row[0].strip().lower()
                        weight = float(row[1])
                        ToneRank_IO.keywords[keyword] = weight
            # Load whitelisted emails
            with open(ToneRank_IO.EMAIL_WHITELIST_FILE_NAME, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    if row: # skip empty rows
                        ToneRank_IO.email_whitelist.append(row[0])
            # Load priority report options
            with open(ToneRank_IO.PRIORITY_REPORT_FILE_NAME, 'r') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader) # Read all rows into a list
                if len(rows) == 0: # If this is the first run of the system 
                    ToneRank_IO.top_email_size = ToneRank_IO.DEFAULT_TOP_EMAIL_SIZE
                    ToneRank_IO.todo_list_sample_size = ToneRank_IO.DEFAULT_TODO_SAMPLE_SIZE
                else:
                    ToneRank_IO.top_email_size = int(rows[0][0]) # Load the Top X emails size                    
                    ToneRank_IO.todo_list_sample_size = int(rows[1][0]) # Load the todo list sample size
        except Exception as e:
            print(f"Error when loading files: {e}")
            raise

    @staticmethod
    def save_local_data():
        """ Save keywords and whitelisted emails to the file. """
        try:
            with open(ToneRank_IO.KEYWORD_FILE_NAME, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                for w, weight in ToneRank_IO.keywords.items():
                    csv_writer.writerow([w, weight]) # each item on its own row
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
        try:
            with open(ToneRank_IO.PRIORITY_REPORT_FILE_NAME, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([ToneRank_IO.top_email_size])
                csv_writer.writerow([ToneRank_IO.todo_list_sample_size])
        except Exception as e:
            print(f"Error when saving priority report customizations: {e}")
            raise


