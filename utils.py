from functools import wraps
import time
import psutil
import string


def reset_word_counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Assuming the decorated functions are instance methods of a class
        self = args[0]

        # Reset the word_counter dictionary
        self.word_counter = {}

        # Call the original function
        result = func(*args, **kwargs)

        return result

    return wrapper

def get_complete_words(chunk, remainder):
    """Extract complete words from a chunk and update the remainder."""
    # Combine the remainder from the previous chunk with the current chunk
    chunk = remainder + chunk

    # Find the last occurrence of a space character in the chunk
    last_space_index = chunk.rfind(' ')
    if last_space_index != -1:
        # Extract the complete words from the chunk
        complete_words = chunk[:last_space_index]
        # Set the remainder for the next iteration
        remainder = chunk[last_space_index + 1:]
    else:
        complete_words = chunk
        remainder = ''

    return complete_words, remainder


def read_file_chunks(file_path, chunk_size: int):
    """Read text file in chunks according to the chunk size, ensuring that chunks end on complete words."""
    with open(file_path, 'r') as file:
        remainder = ''
        while True:
            chunk = file.read(chunk_size).replace("\n", " ")
            if not chunk:
                break

            complete_words, remainder = get_complete_words(chunk, remainder)
            yield complete_words


def split_text_chunks(text, num_chunks):
    """Split string in chunks according to the chunk size, ensuring that chunks end on complete words."""
    chunk_size = len(text) // num_chunks
    remainder = ''
    index = 0

    for _ in range(num_chunks):
        chunk = text[index:index + chunk_size]
        index += chunk_size

        complete_words, remainder = get_complete_words(chunk, remainder)
        yield complete_words


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


class ExperimentRunner:
    def __init__(self):
        self.measure = []

    def measure_resource_utilization(self, start_time: float, process: psutil.Process):
        """Measure and log the resource utilization."""
        self.runtime = time.time() - start_time
        self.cpu_percent = process.cpu_percent()
        self.memory_usage = process.memory_info().rss
        self.measure = [self.runtime, self.cpu_percent, self.memory_usage / 1024 / 1024]
        print(f"Runtime: {self.runtime:.2f} seconds")
        print(f"CPU Utilization: {self.cpu_percent:.2f}%")
        print(f"Memory Usage: {self.memory_usage / 1024 / 1024:.2f} MB")

    def run_experiment(self, version_name: str, func, *args, **kwargs):
        """Run an experiment and log the results."""
        print(f"Running experiment: {version_name}")

        # Start time
        start_time = time.time()

        # Start resource monitoring
        process = psutil.Process()
        process.cpu_percent()
        process.memory_info()

        # Call the function
        result = func(*args, **kwargs)

        # Stop resource monitoring
        self.measure_resource_utilization(start_time, process)

        return result
