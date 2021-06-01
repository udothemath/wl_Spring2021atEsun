# Random Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get all items in train data, remove duplicates.
- For each row in test data, generate a random list of recommend items with length 10
- Calculate the recall

# Top 10 Sales Recommendation
- Contains 4 ways: week as user, time as user, week&time as user, whole train data as user
- For each way, get top10 sales items for each user(peroid, eg in week, we have Monday top 10 sales list, .. , Sunday top 10 sales list) in train data
- Calculate the recall for test data
