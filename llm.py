# The top-level class for the ToneRank application
# @author Rylan Ahmadi (Ry305)
# Last updated 06/12/2025

from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path
import logging
from functools import wraps
import time
from functools import lru_cache

# Constants
MAX_RETRIES = 3 # the maximum number of retries allowed if a failure occurs
MAX_PROMPT_LEN = 100 # the max length of a prompt delivered to the model
MAX_CACHE_SIZE = 1000 # the max length of the cache size
TEMP = 0.0 # the temperature of the model

class GroqLlama:

    """ Provides methods through which Groq's API can be used to access the Llama3 LLM  """

    def __init__(self):
        """ Creates a new GroqLlama object. """
        self.client = self.setup_groq()
        self.logger = self.get_logger()

    # Load the model
    def setup_groq(self):
        """ Sets up the Groq API for use. """
        load_dotenv(Path(".gitignore/.env"))
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        return client

    # Configure logging
    def get_logger(self):
        """ Creates and configures a logger called 'llm_operations.log' which will be used to track
        the interactions with Llama3 """
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
            handlers=[logging.FileHandler('llm_operations.log'), logging.StreamHandler()]
            )
        logger = logging.getLogger(__name__)
        return logger

    # Retry decorator function
    def retry_on_fail( self, max_retries=MAX_RETRIES, delay=1 ):
        """ A decorator which marks a function as repeating upon its failure, for a maximum number of times equal to
        the MAX_RETRIES constant. Takes one user-inputted parameter, which is the logger returned from the get_logger() 
        method """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries - 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_retries - 1:
                            self.logger.error(f"Failed after {max_retries} attempts: {e}")
                            raise
                        self.logger.warning(f"Attempt {attempt + 1} failed {e}")
                        time.sleep(delay * (attempt + 1))
                return None
            return wrapper
        return decorator
    
    # Query Llama 3.2 (without caching the response)
    def get_llama_response( self, prompt, max_retries=MAX_RETRIES, delay=1 ):
        """ Query Llama3 with retry logic. """
        for attempt in range(max_retries - 1):
            try:
                return self.prompt_llama(prompt)
            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed after {max_retries} attempts: {e}")
                    raise
                self.logger.warning(f"Attempt {attempt + 1} failed {e}")
                time.sleep(delay * (attempt + 1))

    # Makes a single Llama 3.2 query with no protection or failsafes (not to be used externally)
    def prompt_llama( self, prompt ):
        """ Queries Llama3 for a response to the specified prompt. """
        try:
            chat_completion = self.client.chat.completions.create( 
                    messages=[ { "role": "user", "content": prompt, } ],
                model="llama3-8b-8192",
                max_tokens = MAX_PROMPT_LEN,
                temperature=TEMP)
            return chat_completion.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error in prompt_llama: {e}")
            raise

    # Query Llama 3.2 (with caching the response)
    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def get_cached_llama_response(self, prompt):
        """ Queries Llama3 for a response to the specified prompt. Caches the response. """
        return self.get_llama_response( prompt ) # call the uncached get_llama_response function
