# Notes
- For Jodie and DGCF, suggest to use the original source code if you want to apply to another dataset, because I have modified the source code. If you want to change the train,validation and test in my code, you need to delete and add some codes, since the source code only support train proprotion <= 0.8, and since our data do not need validation, so I make validation data equal to test data, and train proportion = 0.9
- For node2vec and smore, actually they are easy to use, you can read the readme file in their source code, I have not changed anything of the source code, I only add a folder named Esun_data. In Esun_data folder, it contains recall,precision,MRR code and shell script which run the node2vec, deepwalk and hoprec 100 epochs, calculate recall,precision and MRR for each epoch, finally average them.

# Jodie: Predicting Dynamic Embedding Trajectory in Temporal Interaction Networks
- Temporal networks developed by Stanford University
- Copy and slightly modify from https://github.com/srijankr/jodie
-  Code setup and requirements
    - ```$ git clone https://github.com/udothemath/wl_Spring2021atEsun/tree/main/Project/jodie```
    - ```$ pip install -r requirements.txt```
    - To initialize the directories needed to store data and outputs, use the following command. This will create ```data/, saved_models/, and results/``` directories.
        - ```$ chmod +x initialize.sh```
        - ``` $ ./initialize.sh```
- I add a folder named **data** in the package, which contains (train+test) data according to time in one csv file
    - The data must be converted to the csv form with columns (user_id, item_id, timestamp, state_label, feature1, feature2)
    - Can refer to ```data/Esun_week.csv```
- Usage: (Example)
    - (1) Follow the step above
    - (2) ```$ python jodie.py --network Esun_week --model jodie --epochs 50``` (The model of each epoch will be saved in folder ```saved_models/```)
    - (3) ```$ ./evaluate_all_epochs.sh <network> interaction``` (MRR and recall@3 of each epoch will be save in folder ```results\```, and print best performance result)
- For more details, please visit the source code
- Note
    - The source code is written in python2, I modify it to python3 
    - Recall@10 in source code, I change it to recall@3
    - The original code use 0.8 for train, 0.1 for validation and 0.1 for train
    - I modify the code to 0.8 for train and 0.2 for test (just simply set validation = test)
    - Folder **data** contains 3 train data afer preprocessing
    - Folder **results** contains test result txt file 
    - Since the model size saved in ```saved_models/``` is large, so I do not upload it

# DGCF : Dynamic Graph Collaborative Filtering
- Copy and slightly modify from https://github.com/CRIPAC-DIG/DGCF
- ```$ git clone https://github.com/udothemath/wl_Spring2021atEsun/tree/main/Project/DGCF```
- To initialize the directories needed to store data and outputs, use the following command. This will create ```data/, saved_models/, and results/``` directories.
    - ``` $ ./initialize.sh```
- Usage : 
  - 1. The data must be converted to the csv form with columns (user_id, item_id, timestamp, state_label, feature1, feature2)
        - Can refer to DGCF/data/Esun_week.csv
        - We store train and test data in one csv. We can adjust the train proportion in the command line in next step.
  - 2. Apply command line to your train data : ```python DGCF.py --network <network> --model DGCF --epochs 50 --method attention --adj```
        - Example :   ```python3 DGCF.py --network Esun_week --model DGCF --epochs 50 --method attention --adj```  
        - After that, a folder of saved models will be generated (since the model size is large, so I do not upload it)
  - 3. To evaluate the result for test data, apply command line: Example ```python3 evaluate_all.py --network Esun_week --model DGCF --method attention --adj```
        - Every epoch in step b will generate a model, so after evaluate all, we have 50 test result in a txt file, saved in the folder **results**
- Note : 
  - The source code is written in python2, I modify it to python3 
  - The original code use 0.8 for train, 0.1 for validation and 0.1 for train
  - I modify the code to 0.8 for train and 0.2 for test (just simply set validation = test)
  - Folder **data** contains 3 train data afer preprocessing
  - Folder **results** contains test result txt file 

# Node2vec
- Graph embedding method developed by Stanford University
- Source: https://github.com/aditya-grover/node2vec
- I add a folder named **Esun_data** in the package, which apply Node2vec to Esun dataset 
- There are some subfolders and files contained in **Esun_data**:
    - **data**: Contained train and test csv after preprocess
    - **results**: contained embedding results and a txt file which save MRR and recall
- Usage: ```cd Esun_data/```, then ```sh node2vec_emb.sh ```
- Note: Please use python2

# Smore 
- Graph embedding package developed by NCCU and Academic Sinica
- Source: https://github.com/cnclabs/smore
- I add a folder named Esun_data in the package, which apply**DeepWalk** and **Hoprec** to Esun dataset 
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
- Note: The source code is written with C++
# Random Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get all items in train data
- For each row in test data, generate a random list of recommend items from train data with length 10
- Calculate the recall, precision and MRR of test data

# Top 10 Sales Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get top10 sales items for each user(peroid, eg in week, we have Monday top 10 sales list, .. , Sunday top 10 sales list) from train data
- Calculate the recall, precision and MRR of test data


