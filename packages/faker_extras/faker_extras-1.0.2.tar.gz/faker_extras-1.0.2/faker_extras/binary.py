"""Faker data providers for binary data."""

from random import choice

from faker.providers import BaseProvider

from . import utils


class BinaryProvider(BaseProvider):
    """Provide binary data."""

    byte_formats_binary = {
        'KiB': 'kibibyte',
        'MiB': 'mebibyte',
        'GiB': 'gibibyte',
        'TiB': 'tebibyte',
        'PiB': 'pebibyte',
        'EiB': 'exbibyte',
        'ZiB': 'zebibyte',
        'YiB': 'yobibyte',
    }

    byte_formats_decimal = {
        'kB': 'kilobyte',
        'MB': 'megabyte',
        'GB': 'gigabyte',
        'TB': 'terabyte',
        'PB': 'petabyte',
        'EB': 'exabyte',
        'ZB': 'zettabyte',
        'YB': 'yottabyte',
    }

    def binary_byte_str(self, code=False):
        """Return a multiple of a byte, in its binary string form."""
        bf = self.byte_formats_binary
        return choice(bf.keys() if code else bf.values())

    def decimal_byte_str(self, code=False):
        """Return a multiple of a byte, in its typical decimal form."""
        bf = self.byte_formats_decimal
        return choice(bf.keys() if code else bf.values())

    def nibble(self):
        """Return a nibble.

        >>> nibble()
        >>> 0101
        """
        return utils._choice_str([0, 1], 4)

    def octet(self):
        """Return an octet.

        >>> octet()
        >>> 01011010
        """
        return utils._choice_str([0, 1], 8)

    def byte(self):
        """Return a byte.

        >>> octet()
        >>> 01011010
        """
        return utils._choice_str([0, 1], 8)

    def word(self):
        """Return a 'word'.

        >>> word()
        >>> 0010101111101011
        """
        return utils._choice_str([0, 1], 16)
