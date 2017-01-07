class CanNotOpenRawFile(Exception):
    """
    Can not open the email raw file
    """


class CanNotExtractMoreEmails(Exception):
    """
    Can not extract more emails than it exists on the raw data
    """
