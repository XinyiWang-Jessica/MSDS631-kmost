# MSDS631-kmost

This study is to explore and analyze the factors that may affect the performance of an application, such as:
- Input data scale (dataset size)
- Code Efficiency (data structure and algorithms)
- System resources utilization (CPU and Memory)

How to run experiments:
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
4. View the results in the Summary section.