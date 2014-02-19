from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

from language import getLanguage

WORD_RE = re.compile(r"[\w']+")


class ReviewLanguageCount(MRJob):
    """Counts the number of reviews in each language German, Spanish, English, French. Some reviews
       are ambiguous and these are assigned to 'Unknown'"""
    INPUT_PROTOCOL = JSONValueProtocol
    
    def init_check_language(self):
        """This initializes the language identification object on each node"""
        self.lang=getLanguage(500,2); # getLanguage(nWords, confidence)
        
    def check_language(self, _, record):
        """Extract words using a regular expression.  Normalize the text to
        ignore capitalization. Yield <language,1> for each word"""
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
