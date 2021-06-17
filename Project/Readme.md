# Node2vec
- Graph embedding method developed by Stanford University
- Source: https://github.com/aditya-grover/node2vec
- I add a folder named Esun_data in the package, which apply Node2vec to Esun dataset 
- There are some subfolders and files contained in **Esun_data**:
    - **data**: Contained train and test csv after preprocess

# Smore 
- Graph embedding package developed by NCCU and Academic Sinica
- Source: https://github.com/cnclabs/smore
- I add a folder named Esun_data in the package, which apply DeepWalk and Hoprec to Esun dataset 
- Compilation : 
    ```
    $ git clone https://github.com/udothemath/wl_Spring2021atEsun/tree/main/Project/smore
    $ cd smore
    $ make
    ```
- There are some subfolders and files contained in **Esun_data**:
    - **data**: Contained train and test csv after preprocess
    - **result**: Contained embedding results, and a txt file which save precision@K and recall@K
    - **deepwalk.sh**: Run this command ```sh deepwalk.sh``` to get the embeddings and results of deepwalk
    - **hoprec.sh**: Run this command ```sh hoprec.sh``` to get the embeddings and results of hoprec
    - **recall_count.py**: Calculate the inner product of embeddings to get the recommendation list, then calculate the precision@K and recall@K
- Usage example (After compilation) :
    - ```cd Esun_data/```, then ```sh deepwalk.sh```


# DGCF : Dynamic Graph Collaborative Filtering
- Copy and slightly modify from https://github.com/CRIPAC-DIG/DGCF
- ```$ git clone https://github.com/udothemath/wl_Spring2021atEsun/tree/main/Project/DGCF```
- Usage : 
  - 1. The data must be converted to the csv form with columns (user_id, item_id, timestamp, state_label, feature1, feature2)
        - Can refer to DGCF/data/Esun_week.csv
        - We store train and test data in one csv. We can adjust the train proportion in the command line in next step.
  - 2. Apply command line to your train data : ```python DGCF.py --network <network> --model DGCF --epochs 50 --method attention --adj```
        - Example :   ```python3 DGCF.py --network Esun_week --model DGCF --epochs 50 --method attention --adj```  
        - After that, a folder of models will be generated (since the model size is large, so I do not upload it)
  - 3. To evaluate the result for test data, apply command line: Example ```python3 evaluate_all.py --network Esun_week --model DGCF --method attention --adj```
        - Every epoch in step2 will generate a model, so after evaluate all, we have 50 test result in a txt file, saved in the folder **results**
- Note : 
  - The original code use 0.8 for train, 0.1 for validation and 0.1 for train
  - I modify the code to 0.8 for train and 0.2 for test
  - Folder **data** contains 3 train data afer preprocessing
  - Folder **results** contains test result txt file 

# Random Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get all items in train data, remove duplicates.
- For each row in test data, generate a random list of recommend items with length 10
- Calculate the recall

# Top 10 Sales Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get top10 sales items for each user(peroid, eg in week, we have Monday top 10 sales list, .. , Sunday top 10 sales list) in train data
- Calculate the recall for test data


