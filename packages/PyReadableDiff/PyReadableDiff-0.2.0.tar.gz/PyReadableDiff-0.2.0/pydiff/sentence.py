import re

from .base import Diff


class SentenceDiff(Diff):

    _sentence_split_re = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.!?])(\s)')#re.compile(r'(\S.+?[.!?])(?=\s+|$)')

    def tokenize(self, string):
        ts = self._sentence_split_re.split(string)
        print ts
        return ts


_sentence_diff = SentenceDiff()


def diff_sentences(old_string, new_string):
    return _sentence_diff.diff(old_string, new_string)
