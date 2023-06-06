from functools import wraps
import time
import psutil
import string
import tracemalloc


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
        pass

    def log_performance_and_resource(self, wall_time: float, cpu_time: float, peak_memory_usage: int):
        """Log performance adn resource utilization."""
        self.wall_time = wall_time
        self.cpu_time = cpu_time
        self.peak_memory_usage = peak_memory_usage
        print(f"Wall Time: {self.wall_time:.2f} seconds")
        print(f"CPU Time: {self.cpu_time:.2f} seconds")
        print(
            f"Peak Memory Usage: {self.peak_memory_usage / 1024 / 1024:.2f} MB")

    def measure_peak_memory_usage(self, func, *args, **kwargs):
        """Measure peak memory usage of a function."""
        # Start memory monitoring
        tracemalloc.start()
        # Call the function
        func(*args, **kwargs)
        # Stop memory monitoring
        cur_mem_usage, peak_mem_usage = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak_mem_usage
    
    def measure_time(self, func, *args, **kwargs):
        """Measure wall & CPU time of a function."""
        # Start time monitoring
        wall_start_time = time.time()
        cpu_start_time = time.process_time()
        # Call the function
        result = func(*args, **kwargs)
        # Stop time monitoring and measure elapsed time
        wall_time = time.time() - wall_start_time
        cpu_time = time.process_time() - cpu_start_time
        
        return wall_time, cpu_time, result
    
    def run_experiment(self, version_name: str, func, *args, **kwargs):
        """Run an experiment and log the results."""
        print(f"Running experiment: {version_name}")

        peak_mem_usage = self.measure_peak_memory_usage(func, *args, **kwargs)
        
        # Measure speed without tracking memory usage since it introduces a lot of overhead
        wall_time, cpu_time, result = self.measure_time(func, *args, **kwargs)
        
        self.log_performance_and_resource(
            wall_time, cpu_time, peak_mem_usage)

        return result
