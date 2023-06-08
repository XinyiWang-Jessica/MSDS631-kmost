import string
from typing import Dict, Generator, List, Tuple
import os
import psutil
from threading import Thread, Lock
from utils import reset_word_counter, read_file_chunks, split_text_chunks, remove_punctuation
from multiprocessing import Pool
import heapq


class KMostPopularWords:
    def __init__(self, file_path: str, sorting_method="default"):
        # Path of the file to read from
        self.file_path = file_path

        # Use hash map to keep track of word counts
        self.word_counter = {}

        # Lock for thread-safe access to variables
        self.lock = None

        # Load stopwords
        with open('data/stopwords.txt', 'r') as f:
            # Use set for fast lookup in constant time
            self.stopwords = set([line.strip("\n") for line in f.readlines()])

        if sorting_method not in ["default", "heap_sort"]:
            raise ValueError("Unknown sorting method")
        self.sorting_method = sorting_method

    def count_words(self, text) -> None:
        text = remove_punctuation(text)
        for word in text.split():
            # Convert to lowercase
            word_lower = word.lower()
            # Check whether a word is a stop word
            if not word_lower in self.stopwords:
                if self.lock:
                    with self.lock:
                        self.word_counter[word_lower] = self.word_counter.get(
                            word_lower, 0) + 1
                else:
                    self.word_counter[word_lower] = self.word_counter.get(
                        word_lower, 0) + 1

    def is_file_size_safe(self) -> bool:
        """Check if the file size is within a safe limit to be loaded into memory"""
        file_size = os.path.getsize(self.file_path)
        memory_usage = psutil.virtual_memory()
        available_memory = memory_usage.available
        return file_size < available_memory

    @reset_word_counter
    def get_top_k_words_baseline(self, k: int) -> List[Tuple[str, int]]:
        """Naive approach to load the full text into memory and count words"""
        # Check whether the text can fit into memory
        if not self.is_file_size_safe():
            raise ValueError(
                "File size is too large to be loaded into memory.")

        with open(self.file_path, 'r') as file:
            text = file.read().replace('\n', ' ')
            self.count_words(text)
        if self.sorting_method == "heap_sort":
            return heapq.nlargest(k, self.word_counter.items(), key=lambda x: x[1])
        return sorted(self.word_counter.items(), key=lambda x: x[1], reverse=True)[:k]

    @reset_word_counter
    def get_top_k_words_chunk(self, k: int, chunk_size: int) -> List[Tuple[str, int]]:
        """Split text into smaller chunks and count words in each chunk iteratively"""
        # Iterate over chunks of the text
        for chunk in read_file_chunks(self.file_path, chunk_size):
            # Iterate over words of a chunk
            self.count_words(chunk)

        if self.sorting_method == "heap_sort":
            return heapq.nlargest(k, self.word_counter.items(), key=lambda x: x[1])
        return sorted(self.word_counter.items(), key=lambda x: x[1], reverse=True)[:k]

    @reset_word_counter
    def get_top_k_words_chunk_mt(self, k: int, num_threads: int, chunk_size: int) -> List[Tuple[str, int]]:
        """Apply multithreading to each chunk"""
        # Lock for thread-safe access to word_counter to ensure that only 1 thread can access the word_counter at a time, preventing potential race conditions
        self.lock = Lock()

        for chunk in read_file_chunks(self.file_path, chunk_size):
            # Further split the chunk into sub-chunks to be distributed across multiple threads
            sub_chunks = split_text_chunks(chunk, num_threads)
            # Create threads
            threads = []
            for _, sub_chunk in zip(range(num_threads), sub_chunks):
                t = Thread(target=self.count_words, args=(sub_chunk,))
                t.start()
                threads.append(t)

            # Wait for all threads to finish
            for t in threads:
                t.join()

        # Clean up lock
        self.lock = None

        if self.sorting_method == "heap_sort":
            return heapq.nlargest(k, self.word_counter.items(), key=lambda x: x[1])
        return sorted(self.word_counter.items(), key=lambda x: x[1], reverse=True)[:k]

    def count_words_mp(self, text):
        """Count word function for multiprocessing"""
        text = remove_punctuation(text)
        word_counter = {}
        for word in text.split():
            # Convert to lowercase
            word_lower = word.lower()
            # Check whether a word is a stop word
            if not word_lower in self.stopwords:
                word_counter[word_lower] = word_counter.get(word_lower, 0) + 1
        return word_counter

    @reset_word_counter
    def get_top_k_words_chunk_mp(self, k: int, num_processes: int, chunk_size: int) -> List[Tuple[str, int]]:
        """Apply multiprocessing to each chunk"""

        for chunk in read_file_chunks(self.file_path, chunk_size):
            # Further split the chunk into sub-chunks to be distributed across multiple threads
            sub_chunks = list(split_text_chunks(chunk, num_processes))
            # Create a multiprocessing Pool with the specified number of processes
            pool = Pool(processes=num_processes)

            # Map the count_words function to process each chunk in parallel
            results = pool.map(self.count_words_mp, sub_chunks)

            pool.close()
            # Wait for all processes to complete
            pool.join()

            # Merge the results from all processes
            for result in results:
                for word, count in result.items():
                    self.word_counter[word] = self.word_counter.get(
                        word, 0) + count

        if self.sorting_method == "heap_sort":
            return heapq.nlargest(k, self.word_counter.items(), key=lambda x: x[1])
        return sorted(self.word_counter.items(), key=lambda x: x[1], reverse=True)[:k]
