import re
import os.path
import sys

#from django.utils.encoding import smart_str # This is needed to print unicode strings for debugging

class getLanguage: 
    """This class provides rough functionality to determine what language a text 
        string is written it. The techniques do not work well on short strings"""
    
    WORD_RE = re.compile(r"[\w']+")
    
    def __init__ (self,nWords,confidence):
        """nWords selects the number of most frequent words to use in analysis.
           confidence requires that the number of words in one language be at least
            confidence*(the number of words in any other language)"""
        self.nWords=nWords
        self.confidence=confidence        

        top_eng_words=[]
        # This ordered list of most frequent English words is from Google
        # https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt       
        with open(os.path.join(sys.path[0],'frequentDicts/google-10000-english.txt') ) as inputFile:
            for line in inputFile.readlines():        
                for word in getLanguage.WORD_RE.findall(line):        
                    top_eng_words.append(word.lower())    

        # http://wortschatz.uni-leipzig.de/html/wliste.html
        top_germ_words=[] 
        with open(os.path.join(sys.path[0],'frequentDicts/top10000de.txt')) as inputFile:
            for line in inputFile.readlines():        
                for word in getLanguage.WORD_RE.findall(line):        
                    top_germ_words.append(word.lower())   
                    
        # http://wortschatz.uni-leipzig.de/html/wliste.html
        top_fren_words=[] 
        with open(os.path.join(sys.path[0],'frequentDicts/top10000fr.txt')) as inputFile:
            for line in inputFile.readlines():        
                for word in getLanguage.WORD_RE.findall(line):        
                    top_fren_words.append(word.lower())   
                    
        # http://yong321.freeshell.org/misc/WordFrequency.html
        # Slightly different format here
        top_span_words=[] 
        with open(os.path.join(sys.path[0],'frequentDicts/SpanishWordFrequencyG.txt')) as inputFile:
            for line in inputFile.readlines():        
               top_span_words.append( getLanguage.WORD_RE.findall(line)[0] )       
        #consider using http://corpus.rae.es/lfrecuencias.html instead if this doesnt work
               
        # Use the nWords most frequent words from each languae
        # Make sure we aren't trying to use more words than are in the dictionaries
        top_eng_words=top_eng_words[0:min(nWords-1,len(top_eng_words))]             
        top_germ_words=top_germ_words[0:min(nWords-1,len(top_germ_words))]             
        top_fren_words=top_fren_words[0:min(nWords-1,len(top_fren_words))]          
        top_span_words=top_span_words[0:min(nWords-1,len(top_span_words))]

        # Remove all words that are in both sets    
        self.top_eng_word_set=set(top_eng_words)-set(top_germ_words)-set(top_fren_words)-set(top_span_words)
        self.top_germ_word_set=set(top_germ_words)-set(top_fren_words)-set(top_eng_words)-set(top_span_words)
        self.top_fren_word_set=set(top_fren_words)-set(top_germ_words)-set(top_eng_words)-set(top_span_words)                
        self.top_span_word_set=set(top_span_words)-set(top_fren_words)-set(top_eng_words)-set(top_germ_words)
    
        # These are some really popular words in Yelp reviews, improves classification, especially of short reviews
        self.top_eng_word_set=self.top_eng_word_set|set(['fast','good','great','best','awesome','fantastic','delicious','excellent','yum','yummy','amazing','disgusting','closed'])

    def printTopEng(self):
        """Prints the most common English words used in this object"""
        print(self.top_eng_word_set)
        print("\n")
    
    def printTopGerm(self):
        """Prints the most common German words used in this object"""
        print(self.top_germ_word_set)
        print("\n")
        
    def printTopFren(self):
        """Prints the most common French words used in this object"""
        print(self.top_fren_word_set)
        print("\n")
        
    def printTopSpan(self):
        """Prints the most common Spanish words used in this object"""
        print(self.top_span_word_set)
        print("\n")
        

    def language(self, string):
        """Extract words using a regular expression.  Normalize the text to
        ignore capitalization."""            
        
        # Initialize word counts to zero
        top_eng_count=0
        top_germ_count=0
        top_fren_count=0
        top_span_count=0    
        
        # Loop overtext and increment counters when a word appers in a language's dictionary
        for word in getLanguage.WORD_RE.findall(string):
            if word.lower() in self.top_eng_word_set:
                top_eng_count+=1
            elif word.lower() in self.top_germ_word_set:
                top_germ_count+=1
            elif word.lower() in self.top_fren_word_set:
                top_fren_count+=1
            elif word.lower() in self.top_span_word_set:
                top_span_count+=1
            # This should break once the text has a preponderance of one language, at a minimum
            # of 10 matching words
            #if abs(top_eng_count-top_germ_count) > 10*min([top_eng_count,top_germ_count]):
                # break
        
        # Return the language with the at least confidence times as many words as any other language
        # If none satisfy this condition, return 'Unknown'
        if top_germ_count>self.confidence*top_eng_count \
            and top_germ_count>self.confidence*top_span_count and top_germ_count>self.confidence*top_fren_count:
            return('German')
        elif top_eng_count>self.confidence*top_germ_count \
             and top_eng_count>self.confidence*top_fren_count and top_eng_count>self.confidence*top_span_count:
            return('English')
        elif top_fren_count>self.confidence*top_eng_count \
            and top_fren_count>self.confidence*top_span_count and top_fren_count>self.confidence*top_germ_count:           
            return('French')
        elif top_span_count>self.confidence*top_germ_count \
            and top_span_count>self.confidence*top_eng_count and top_span_count>self.confidence*top_fren_count:
            return('Spanish')
        else: 
            return('Unknown')