
import string
from typing import Dict, Generator, List, Tuple
import nltk
from nltk.stem.porter import *
from collections import Counter
import heapq


class KMostSingle:
    def __init__(self, file_path: str):
        # Path of the file to read from
        self.file_path = file_path

        # Use hash map to keep track of word counts
        self.word_counter = {}

        # get the text
        with open(self.file_path,'r') as f:
            self.text = f.read()

        # Load stopwordsk
        with open('data/stopwords.txt', 'r') as f:
            # Use set for fast lookup in constant time
            self.stopwords = set([line.strip("\n") for line in f.readlines()])

    def count_words(self):
        """
        Tokenize text and return a non-unique list of tokenized words
        found in the text. Normalize to lowercase, strip punctuation,
        remove stop words, drop words of length < 3, strip digits.
        Time complexity O(n)  ()
        Get the count of each word
        Time complexity O(n)
        """
        self.text = re.sub('[' + string.punctuation + '0-9\\r\\t\\n]', ' ', self.text)
        self.text = self.text.lower()
        tokens = nltk.word_tokenize(self.text)
        tokens = [w for w in tokens if len(w) > 2 and w not in self.stopwords]  # ignore a, an, to, at, be, ...
        self.word_counter = Counter(tokens)
        del tokens
        return self.word_counter

    def heap_sort(self, k : int):
        """
        Sort the words count using python heapq
        return the k most popular words
        Time complexity O(nlogk)
        """
        self.count_words()
        return heapq.nlargest(k, self.word_counter.keys(), key = self.word_counter.get)

    def tim_sort(self, k : int):
        """
        Sorted the words count using python sorted 
        (Timsort: merge and insertion sort) 
        Time complexity O(nlogn)
        Get the k most popular words (slicing)
        Time complexity O(k)
        """ 
        self.count_words()
        return sorted(self.word_counter, key = lambda k : self.word_counter[k], reverse = True)[:k]