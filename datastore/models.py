import base64
import os
import re

from . import constants
from .exceptions import CanNotExtractMoreEmails, CanNotOpenRawFile


def extracts_words_frequencies_for(text):
    if "=?utf-" in text.lower():
        return ["=?utf-"]
    text = " {} ".format(text.lower())
    words = set(re.findall('[a-zA-Z0-9]+[.,:?!]* ', text))
    return [str(word.strip()) for word in list(words) if word.strip() != '']


class EmailsDataStore:
    """
    This model stores the data from the emails
    """

    OUTPUT_DIR = constants.OUTPUT_RESULTS_DIR
    RAW_DIR = constants.RAW_DATA_DIR
    EXTENSION = constants.RAW_EXTENSION

    def __init__(self, index=1, max=constants.MAXIMUM_EMAILS):
        self.index = index
        self.max = max
        self.emails = {
            constants.SPAM_TYPE: [],
            constants.NO_SPAM_TYPE: []
        }

    def populate(self):
        for key_type, emails in self.emails.items():
            file = self.file_for_type(key_type)
            emails += RawEmailsStore(file).get_raw_emails()

        # Let's insure we have the same number of spam and no spam emails:
        self.max = min([len(val) for typ, val in self.emails.items()])
        for type in self.emails:
            self.emails[type] = self.emails[type][0:self.max]

    def file_for_type(self, type):
        return os.path.join(self.RAW_DIR, "{}-{}.{}".format(type, self.index, self.EXTENSION))

    def extract(self, start=0, count=1):
        if start + count >= self.max:
            raise CanNotExtractMoreEmails
        return {
            constants.SPAM_TYPE: self.emails[constants.SPAM_TYPE][start:start+count],
            constants.NO_SPAM_TYPE: self.emails[constants.NO_SPAM_TYPE][start:start+count],
        }


class RawEmailsStore:
    """
    Stores and parses the raw emails from a mbox file
    """

    def __init__(self, file):
        self.file = file
        self.content = ""
        self.emails = []

    def get_content(self):
        with open(self.file, 'r') as f:
            return f.readlines()
        raise CanNotOpenRawFile("Could not open the file {}".format(self.file))

    def get_raw_emails(self, max=constants.MAXIMUM_EMAILS):
        """
        Reads its mbox File and returns a list of RawEmailParser objects
        """
        content_file = self.get_content()
        current_email = []
        index = 0
        for line in content_file:
            if index > max:
                return self.emails
            if line.startswith("From "):
                index += 1
                if current_email and index > 0:
                    self.emails.append(Email(current_email))
                current_email = [line.strip('\n')]
            else:
                current_email.append(line.strip('\n'))

        if current_email:
            self.emails.append(Email(current_email))
        return self.emails


class Email:
    """
    This stores the email data
    """

    def __init__(self, raw_content=''):
        self.raw = raw_content
        self.headers = {'Subject': ''}
        self.content = ''
        self.content_starts_index = 0

        # Let's populate the email attributes:
        self.parse_raw()

    @property
    def subject(self):
        return  self.headers['Subject']

    def parse_raw(self):
        self.populate_headers()
        self.populate_content()

    def populate_headers(self):
        for index, line in enumerate(self.raw[1:]):
            if line == '\r':
                self.content_starts_index = index + 2
                return
            header_parts = line.split(': ')
            if len(header_parts) < 2:
                continue
            header_key = header_parts[0]
            header_content = ": ".join(header_parts[1:])
            self.headers[header_key] = header_content.strip('\r')

    def populate_content(self):
        content = "\n".join(self.raw[self.content_starts_index:])
        try:
            content = base64.b64decode(content).decode('UTF-8')
        except UnicodeDecodeError:
            pass
        except TypeError:
            content = ''
        self.content = content

    def extract_classifier_words(self):
        return extracts_words_frequencies_for(self.subject)

