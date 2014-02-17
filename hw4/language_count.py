from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

from language import getLanguage

WORD_RE = re.compile(r"[\w']+")


class ReviewLanguageCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    
    def init_check_language(self):
        self.lang=getLanguage(500,2); 
        
    def check_language(self, _, record):
        """Extract words using a regular expression.  Normalize the text to
        ignore capitalization."""
        if record['type'] == 'review':
            yield [self.lang.language(record['text']), 1]

    def count_languages(self, language, counts):
        """Summarize all the counts by taking the sum."""
        yield [language, sum(counts)]

    def steps(self):
        """Counts the number of words in all reviews
        extract_words: <line, record> => <word, count>
        count_words: <word, counts> => <word, total>
        """
        return [
            self.mr(mapper_init=self.init_check_language,mapper=self.check_language,
                    combiner=self.count_languages,reducer=self.count_languages),
        ]


if __name__ == '__main__':
    ReviewLanguageCount.run()
