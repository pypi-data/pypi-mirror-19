"""
Parser module specific to the "Jones" sequence file format
"""

__author__ = "Felix Simkovic"
__date__ = "13 Sep 2016"
__version__ = 0.1

from conkit.core import Sequence
from conkit.core import SequenceFile
from conkit.io._ParserIO import _SequenceFileParser

import os
import re

SEQ_RECORD = re.compile(r'^([A-Z0-9~-]+)$')

class JonesIO(_SequenceFileParser):
    """Parser class for Jones sequence files

    Description
    -----------
    This format is a "new" definition of sequence-only records.

    It assumes that there are no comments, headers or any other
    data in the file.

    The only information present are sequences, whereby one sequence
    is represented in a single line!

    """
    def __init__(self):
        super(JonesIO, self).__init__()

    def read(self, f_handle, f_id='jones'):
        """Read a sequence file

        Parameters
        ----------
        f_handle
           Open file handle [read permissions]
        f_id : str, optional
           Unique sequence file identifier

        Returns
        -------
        :obj:`conkit.core.SequenceFile`

        """

        # Create a new sequence file instance
        hierarchy = SequenceFile(f_id)

        for i, line in enumerate(f_handle):

            if not line:
                continue

            if not SEQ_RECORD.match(line):
                raise ValueError('Unknown entry in line {0}: {1}'.format(i+1, line))

            sequence = SEQ_RECORD.match(line).group(1)
            sequence_entry = Sequence('seq_{i}'.format(i=i), sequence)

            hierarchy.add(sequence_entry)

        return hierarchy

    def write(self, f_handle, hierarchy):
        """Write a sequence file instance to to file

        Parameters
        ----------
        f_handle
           Open file handle [write permissions]
        hierarchy : :obj:`conkit.core.SequenceFile` or :obj:`conkit.core.Sequence`

        """
        # Double check the type of hierarchy and reconstruct if necessary
        sequence_file = self._reconstruct(hierarchy)

        for sequence_entry in sequence_file:
            f_handle.write(sequence_entry.seq + os.linesep)

        return
