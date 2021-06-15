import numpy as np
import pandas as pd 
import argparse
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument('--dir_path',default='../Esun_data/result/deepwalk/week_no_feature', help='Directory of the embedding file store')
parser.add_argument('--method', default="Deep_Walk", help='Model name')
parser.add_argument('--test', default='../Esun_data/data/test.txt', help='Test file path')
parser.add_argument('--recall_num', nargs='+', type=int, help='The list of recall')
parser.add_argument('--user_node', default=7, type=int, help='# of user node')
parser.add_argument('--user_start', default=800, type=int, help='user id start')
args = parser.parse_args()
print('\n',args)


def scores_then_recall(filename, test, recall_num, user_node, user_start, method = None):
    S = [0 for i in range(len(recall_num))]
    Prec = [0 for i in range(len(recall_num))]
    test = pd.read_csv(test,  delim_whitespace=True)
    for txt in filename:
        txt = os.path.join(dir_path,txt)
        with open(txt, 'r') as f:
            text = f.readlines()
        del text[0]    
        df1 = [[float(x) for x in e.split()] for e in text]
        df1 = pd.DataFrame(df1)
        df1.iloc[:,0] = pd.to_numeric(df1.iloc[:,0], downcast='integer')
        D = {}
        for i in range(len(df1[0])):
            D[df1[0][i]] = list(df1.iloc[i,1:])
            
        # user-item inner product
        items_users = list(df1[0])
        #print(items_users)
        items = [int(ele) for ele in items_users if int(ele) not in [user_start +j for j in range(user_node)]]
        scores = [[] for i in range(user_node)]

        for i in range(len(items)):
            for k in range(user_node):
                scores[k].append(sum([x*y for x,y in zip(D[k+user_start],D[items[i]])]))

        # get first 10 recommender items of each user based on the scores
        N = 10
        rec_list = [0 for i in range(user_node)]
        Max_scores = [0 for i in range(user_node)]
        for k in range(user_node):
            test_list = scores[k]
            res = sorted(range(len(test_list)), key = lambda sub: test_list[sub])[-N:]
            rec_list[k] = [items[i] for i in res]
            Max_scores[k] = [test_list[i] for i in res]
            
        items_users = list(df1[0])
        items = [ele for ele in items_users if ele not in [user_start +j for j in range(user_node)]]
        test_item = list((test['item_id']))

        rec_list = [rec_list[i][::-1] for i in range(len(rec_list))]


        for num in range(len(recall_num)):
            # Recall@num
            s = 0
            for i in range(len(test_item)):
                for idx in range(user_node):
                    if list(test['user_id'])[i]==idx and test_item[i] in rec_list[idx][0:recall_num[num]]:
                        s+=1
            S[num]+=s

            # Precision@num
            P = 0
            for idx in range(user_node):
                K = list(set(test[test['user_id']==idx]['item_id']) & set(rec_list[idx][0:recall_num[num]]))
                P+= len(K)/recall_num[num]
            Prec[num] = P/user_node



    if method != None :
        fw = open('../Esun_data/result/recall_save_file.txt', "a")
        fw.write(f'\n========= {method} =========')
        print(f'========= {method} =========')

    S = np.array(S)/len(test)/len(filename)
    for i in range(len(recall_num)):
        
        fw.write(f'\nAverage rec@{recall_num[i]} of {len(filename)} result : {S[i]}')
        fw.write(f'\nAverage prec@{recall_num[i]} of {len(filename)} result : {Prec[i]}')
        print(f'Average rec@{recall_num[i]} of {len(filename)} result :',S[i])
        print(f'Average prec@{recall_num[i]} of {len(filename)} result :',Prec[i])

start_time = time.time()
dir_path = args.dir_path
filename = os.listdir(dir_path)
scores_then_recall(filename, args.test, args.recall_num, args.user_node, args.user_start, args.method)
print("--- %s seconds ---" % (time.time() - start_time))


