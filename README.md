# Factors Influencing the Performance of an Application for Searching Most Popular Words
## Introduction
This study is to explore and analyze the factors that may affect the performance of an application, such as:

- Input data scale (dataset size)
- Code Efficiency (data structure and algorithms)
- System resources utilization (CPU and Memory)

The runtime, CPU, and RAM utilization were tacked as metrics for application performance evaluation.
The main challenge of processing a large dataset is the limited system resources, such as data size (16 GB) over the available memory space. To combat the CPU and memory limitations, the following strategies are employed:

- **Data Chunking**: divide the file into smaller, manageable chunks. Each chunk is subsequently processed one at a time.
- **Multi-threading**: divide the file into N equal portions and assign them to N threads for simultaneous processing on a single core. 
- **Multi-processing**: divide the file into equal portions and then distribute to several CPU cores processing.

The computed individual results are aggregated for each approach to obtain the final results.

## Data Preparation
To run the experiment for this analysis, text files in English with sizes in different orders of magnitude can be used. 
Before the experiments,  the following reparations will be performed:
- Words tokenizing
- Remove English Stop Words
- Remove punctuations

## How to run experiments:
1. Save the testing dataset in the data folder
2. Add the respect file names to the files list
3. Run the Jupyter notebook of result_analysis.ipynb for different defined cases

   - For basesline case
   ```
    k_most = KMostPopularWords(file_path, "heap_sort")
    result = experiment_runner.run_experiment("Baseline"+file_path, k_most.get_top_k_words_baseline, k)
   ```
   - For Chunking case
   ```
    k_most = KMostPopularWords(file_path)
    result = experiment_runner.run_experiment("Chunking-Tim" + file_path, k_most.get_top_k_words_chunk, k, chunk_size)
   ```
   - For Multi-Threads Cases
   ```
    k_most = KMostPopularWords(file_path)
    result = experiment_runner.run_experiment("multi-thread" + file_path, k_most.get_top_k_words_chunk_mt, k, num_thread, chunk_size)
   ```
   - For Multi-Process Cases
   ```
    k_most = KMostPopularWords(file_path)
    result = experiment_runner.run_experiment("multi-thread" + file_path, k_most.get_top_k_words_chunk_mp, k, num_process, chunk_size)

   ```
5. View the results in the Summary section.
