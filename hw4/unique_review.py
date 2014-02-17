from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re

from language import *

WORD_RE = re.compile(r"[\w']+")


# One issue here is that at least some reviews are in German. There are a few ways I can think of to
# discriminate between English/German in a crude way:
# relative letter frequency: The frequency of the letter 'e' is 12.7% in Eng 
# and 17.4% in German FROM WIKIPEDIA
# Common words: The five most common words in English are 'the' 'be' 'to' 'of' 'and' FROM WIKIPEDIA
# The five most common words in written German are 'der' 'die' 'und' 'in' 'von' SOURCE: http://german.about.com/library/blwfreq_spk30.htm

class UniqueReview(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol
    
    def init_extract_words(self):
        self.lang=getLanguage(50,2); # No ned for nWords to be big here, the reviews we are looking for are long

    def extract_words(self, _, record):
        """Take in a record, yield <word, review_id>"""
        if record['type'] == 'review' and (self.lang.language(record['text']) in ['English']):
            for word in WORD_RE.findall(record['text']):
                # Key is a word in all lower case, value is the review ID
                yield(word.lower(), record['review_id'])
        
    def count_reviews(self, word, review_ids):
        """Count the number of reviews a word has appeared in.  If it is a
        unique word (ie it has only been used in 1 review), output that review
        and 1 (the number of words that were unique)."""
      
        unique_reviews = set(review_ids)  # set() uniques an iterator
        # If the word appears in only one review, yield the review_id as a key 
        # and 1 as value
        if len(unique_reviews)==1:
            yield(unique_reviews.pop(),1)

    def count_unique_words(self, review_id, unique_word_counts):
        """Output the number of unique words for a given review_id"""
        yield(review_id,sum(unique_word_counts))

    def aggregate_max(self, review_id, unique_word_count):
        """Group reviews/counts together by the MAX statistic."""
        yield("MAX",[unique_word_count,review_id])

    def select_max(self, stat, count_review_ids):
        """Given a list of pairs: [count, review_id], select on the pair with
        the maximum count, and output the result."""
        temp=max(count_review_ids)
        yield(temp[1],temp[0])
        ###
        # TODO: find the review with the highest count, yield the review_id and
        # the count. HINT: the max() function will compare pairs by the first
        # number
        #
        #/

    def steps(self):
        """TODO: Document what you expect each mapper and reducer to produce:
        mapper1: <line, record> => <key, value>
        reducer1: <key, [values]>
        mapper2: ...
        """
        return [
            self.mr(mapper_init=self.init_extract_words, mapper=self.extract_words, reducer=self.count_reviews),
            self.mr(reducer=self.count_unique_words),
            self.mr(self.aggregate_max, self.select_max),
        ]


if __name__ == '__main__':
    UniqueReview.run()
