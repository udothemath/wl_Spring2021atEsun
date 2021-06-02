# Random Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get all items in train data, remove duplicates.
- For each row in test data, generate a random list of recommend items with length 10
- Calculate the recall

# Top 10 Sales Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get top10 sales items for each user(peroid, eg in week, we have Monday top 10 sales list, .. , Sunday top 10 sales list) in train data
- Calculate the recall for test data

# DGCF : Dynamic Graph Collaborative Filtering
- Copy and slightly modify from https://github.com/CRIPAC-DIG/DGCF
- Usage : 
  - 1. The data must be converted to the csv form with column (user_id, item_id, timestamp, state_label, feature1, feature2)
        - Can refer to DGCF/data/Esun_week.csv
        - We store train and test data in one csv. We can adjust the train proportion in the command line in next step.
  - 2. Apply command line for your train data : ```python DGCF.py --network <network> --model DGCF --epochs 50 --method attention --adj```
        - Example :   ```python3 DGCF.py --network Esun_week --model DGCF --epochs 50 --method attention --adj```  
        - After that, a folder that contains models will be generated (since the model size is large, so I do not upload it)
  - 3. To evaluate the result for test data, apply command line: Example ```python3 evaluate_all.py --network Esun_week --model DGCF --method attention --adj```
        - Every epoch in step2 will generate a model, so after evaluate all, we have 50 test result in a txt file, saved in the folder ```results```  
