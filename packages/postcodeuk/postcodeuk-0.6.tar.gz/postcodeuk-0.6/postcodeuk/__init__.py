"""
Write a library that supports validating and formatting post codes for UK.
The details of which post codes are valid and which are the parts they consist of can be
found at https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting.
The API that this library provides is your choice.
"""
import re
from rstr import xeger


class PostCodeUk:
    N = '[0-9]'
    A1 = '[A-PR-UWYZ]'
    A2 = '[A-HK-Y]'
    A3 = '[ABCDEFGHJKPSTUW]'
    A4 = '[ABEHMNPRVWXY]'

    OUTWARD_PATTERNS = {
        'AN': A1+N,
        'ANN': A1+(N*2),
        'AAN': A1+A2+N,
        'ANA': A1+N+A3,
        'AANN': A1+A2+(N*2),
        'AANA': A1+A2+N+A4
    }
    INWARD_PATTERN = '[0-9][ABD-HJLNP-UW-Z]{2}'
    OUTWARD_PATTERN = '|'.join(list(OUTWARD_PATTERNS.values()))
    VALID_POSTCODE_PATTERN = r"^("+OUTWARD_PATTERN+")[ ]*("+INWARD_PATTERN+"$)"
    POSTCODE_PATTERN_IN_TEXT = r"("+OUTWARD_PATTERN+") ("+INWARD_PATTERN+")"

    def __init__(self, post_code):
        if not isinstance(post_code, str):
            raise TypeError(
                'postcode should be instance of "str" but received a "{}"'.format(
                    type(post_code).__name__
                )
            )
        self.post_code = post_code
        self._is_valid = self._valid()

    @classmethod
    def _validate(cls, post_code):
        regex_postcode = re.match(cls.VALID_POSTCODE_PATTERN, post_code)
        return regex_postcode if regex_postcode else None

    def _valid(self):
        if not self.post_code:
            return False

        code = self._validate(self.post_code)
        if not code:
            return False

        self._outward, self._inward = code.groups()
        return True

    def is_valid(self):
        return self._is_valid

    def get_outward(self):
        return self._outward if self._is_valid else None

    def get_inward(self):
        return self._inward if self._is_valid else None

    @classmethod
    def random_postcode(cls):
        pattern = r"^("+cls.OUTWARD_PATTERN+")[ ]("+cls.INWARD_PATTERN+"$)"
        return xeger(pattern)

    @classmethod
    def find_all_in_text(cls, text, post_codes=[]):
        if post_codes and not isinstance(post_codes, list):
            raise TypeError(
                'postcode should be instance of "list" but received a "{}"'.format(
                    type(post_codes).__name__
                )
            )
        pattern = cls.POSTCODE_PATTERN_IN_TEXT

        if post_codes:
            if not all(
                    cls._validate(code) if isinstance(code, str) else None
                    for code in post_codes):
                return "all postcodes should be valid"
            pattern = '|'.join(post_codes)

        matches = re.finditer(pattern, text)
        return [m.group() for m in matches] if matches else None
