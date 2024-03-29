# -*- coding: utf-8 -*
'''
This code evaluates the validation and test performance in an epoch of the model trained in DGCF.py.
The task is: interaction prediction, i.e., predicting which item will a user interact with? 

To calculate the performance for one epoch:
$ python evaluate_interaction_prediction.py --network reddit --model DGCF --epoch 49

To calculate the performance for all epochs, use the bash file, evaluate_all_epochs.sh, which calls this file once for every epoch.

Paper: Predicting Dynamic Embedding Trajectory in Temporal Interaction Networks. S. Kumar, X. Zhang, J. Leskovec. ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD), 2019. 
'''

# python3 -u  evaluate_interaction_prediction.py --network Esun_data --method attention --epoch 49 --adj

from library_data import *
from library_models import *
import datetime

# INITIALIZE PARAMETERS
parser = argparse.ArgumentParser()
parser.add_argument('--network', required=True, help='Network name')
parser.add_argument('--model', default='DGCF', help="Model name")
parser.add_argument('--adj', action='store_true', help='The second order relationship')
parser.add_argument('--no_zero', action='store_true', help='The zero order relationship')
parser.add_argument('--no_first', action='store_true', help='The first order relationship')
parser.add_argument('--l2u', type=float, default=1.0, help='regular coefficient of user')
parser.add_argument('--l2i', type=float, default=1.0, help='regular coefficient of item')
parser.add_argument('--method', default="mean", help='The way of aggregate adj')
parser.add_argument('--length', type=int, default=None, help='sample length')
parser.add_argument('--gpu', default=-1, type=int, help='ID of the gpu to run on. If set to -1 (default), the GPU with most free memory will be chosen.')
parser.add_argument('--epoch', default=50, type=int, help='Epoch id to load')
parser.add_argument('--embedding_dim', default=128, type=int, help='Number of dimensions')
parser.add_argument('--train_proportion', default=0.8, type=float, help='Proportion of training interactions')
parser.add_argument('--span_num', default=500, type=int, help='time span number')
parser.add_argument('--state_change', default=False, type=bool, help='True if training with state change of users in addition to the next interaction prediction. False otherwise. By default, set to True. MUST BE THE SAME AS THE ONE USED IN TRAINING.')
args = parser.parse_args()
print(args)
args.datapath = "data/%s.csv" % args.network
if args.train_proportion > 0.8:
    sys.exit('Training sequence proportion cannot be greater than 0.8.')
if args.network == "mooc":
    print("No interaction prediction for %s" % args.network)
    sys.exit(0)
    
# SET GPU
args.gpu = select_free_gpu()
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu

# CHECK IF THE OUTPUT OF THE EPOCH IS ALREADY PROCESSED. IF SO, MOVE ON.
if not args.length:
    dic = 'results/'
else:
    dic = 'results_%s/' % args.length

if args.adj:
    if args.l2u == 1.0 and args.l2i == 1.0:
        output_fname = dic + "interaction_prediction_%s.%s.%s.txt" % (args.network, args.method, 'adj')
    else:
        output_fname = dic + "interaction_prediction_%s.%s.user%.1f.item%.1f.%s.txt" % (args.network, args.method, args.l2u, args.l2i,'adj')
elif args.no_zero:
    if args.l2u == 1.0 and args.l2i == 1.0:
        output_fname = dic + "interaction_prediction_%s.%s.%s.txt" % (args.network, args.method, 'no_zero')
    else:
        output_fname = dic + "interaction_prediction_%s.%s.user%.1f.item%.1f.%s.txt" % (args.network, args.method, args.l2u, args.l2i,'no_zero')
elif args.no_first:
    if args.l2u == 1.0 and args.l2i == 1.0:
        output_fname = dic + "interaction_prediction_%s.%s.%s.txt" % (args.network, args.method, 'no_first')
    else:
        output_fname = dic + "interaction_prediction_%s.%s.user%.1f.item%.1f.%s.txt" % (args.network, args.method, args.l2u, args.l2i,'no_first')
else:
    if args.l2u == 1.0 and args.l2i == 1.0:
        output_fname = dic + "interaction_prediction_%s.%s.txt" % (args.network, args.method)
    else:
        output_fname = dic + "interaction_prediction_%s.%s.user%.1f.item%.1f.txt" % (args.network, args.method, args.l2u, args.l2i,)


if os.path.exists(output_fname):
    f = open(output_fname, "r")
    search_string = 'Test performance of epoch %d' % args.epoch
    for l in f:
        l = l.strip()
        if search_string in l:
            print("Output file already has results of epoch %d" % args.epoch)
            sys.exit(0)
    f.close()

# LOAD NETWORK
[user2id, user_sequence_id, user_timediffs_sequence, user_previous_itemid_sequence, \
 item2id, item_sequence_id, item_timediffs_sequence, \
 timestamp_sequence, \
 feature_sequence, \
 y_true] = load_network(args)
num_interactions = len(user_sequence_id)
num_features = len(list(feature_sequence[0]))
num_users = len(user2id)
num_items = len(item2id) + 1
true_labels_ratio = len(y_true)/(sum(y_true)+1)
print("*** Network statistics:\n  %d users\n  %d items\n  %d interactions\n  %d/%d true labels ***\n\n" % (num_users, num_items, num_interactions, sum(y_true), len(y_true)))

# SET TRAIN, VALIDATION, AND TEST BOUNDARIES
train_end_idx = validation_start_idx = test_start_idx = int(num_interactions * args.train_proportion)
#test_start_idx = int(num_interactions * (args.train_proportion + 0.1))
test_end_idx = int(num_interactions * (args.train_proportion + 0.2))

# SET BATCHING TIMESPAN
'''
Timespan indicates how frequently the model is run and updated. 
All interactions in one timespan are processed simultaneously. 
Longer timespans mean more interactions are processed and the training time is reduced, however it requires more GPU memory.
At the end of each timespan, the model is updated as well. So, longer timespan means less frequent model updates. 
'''
timespan = timestamp_sequence[-1] - timestamp_sequence[0]
tbatch_timespan = timespan / args.span_num

# INITIALIZE MODEL PARAMETERS
model = DGCF(args, num_features, num_users, num_items).cuda()
weight = torch.Tensor([1,true_labels_ratio]).cuda()
crossEntropyLoss = nn.CrossEntropyLoss(weight=weight)
MSELoss = nn.MSELoss()

# INITIALIZE MODEL
learning_rate = 1e-3
optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-5)

# LOAD THE MODEL
model, optimizer, user_embeddings_dystat, item_embeddings_dystat, user_adj, item_adj, \
user_embeddings_timeseries, item_embeddings_timeseries, train_end_idx_training = load_model(model, optimizer, args, args.epoch)
if train_end_idx != train_end_idx_training:
    sys.exit('Training proportion during training and testing are different. Aborting.')

# SET THE USER AND ITEM EMBEDDINGS TO THEIR STATE AT THE END OF THE TRAINING PERIOD
set_embeddings_training_end(user_embeddings_dystat, item_embeddings_dystat, user_embeddings_timeseries, item_embeddings_timeseries, user_sequence_id, item_sequence_id, train_end_idx) 

# LOAD THE EMBEDDINGS: DYNAMIC AND STATIC
item_embeddings = item_embeddings_dystat[:, :args.embedding_dim]
item_embeddings = item_embeddings.clone()
item_embeddings_static = item_embeddings_dystat[:, args.embedding_dim:]
item_embeddings_static = item_embeddings_static.clone()

user_embeddings = user_embeddings_dystat[:, :args.embedding_dim]
user_embeddings = user_embeddings.clone()
user_embeddings_static = user_embeddings_dystat[:, args.embedding_dim:]
user_embeddings_static = user_embeddings_static.clone()

# PERFORMANCE METRICS
validation_ranks = []
test_ranks = []

''' 
Here we use the trained model to make predictions for the validation and testing interactions.
The model does a forward pass from the start of validation till the end of testing.
For each interaction, the trained model is used to predict the embedding of the item it will interact with. 
This is used to calculate the rank of the true item the user actually interacts with.

After this prediction, the errors in the prediction are used to calculate the loss and update the model parameters. 
This simulates the real-time feedback about the predictions that the model gets when deployed in-the-wild. 
Please note that since each interaction in validation and test is only seen once during the forward pass, there is no data leakage. 
'''
import heapq

tbatch_start_time = None
loss = 0
# FORWARD PASS
print("*** Making interaction predictions by forward pass (no t-batching) ***")
#with trange(train_end_idx, test_end_idx) as progress_bar:
print('start time:', datetime.datetime.now())
for j in range(train_end_idx, test_end_idx):
    #progress_bar.set_description('%dth interaction for validation and testing' % j)

    # LOAD INTERACTION J
    userid = user_sequence_id[j]
    itemid = item_sequence_id[j]
    feature = list(feature_sequence[j])
    user_timediff = user_timediffs_sequence[j]
    item_timediff = item_timediffs_sequence[j]
    timestamp = timestamp_sequence[j]
    if not tbatch_start_time:
        tbatch_start_time = timestamp
    itemid_previous = user_previous_itemid_sequence[j]

    # LOAD USER AND ITEM EMBEDDING
    user_embedding_input = user_embeddings[torch.cuda.LongTensor([userid])]
    user_embedding_static_input = user_embeddings_static[torch.cuda.LongTensor([userid])]
    item_embedding_input = item_embeddings[torch.cuda.LongTensor([itemid])]
    item_embedding_static_input = item_embeddings_static[torch.cuda.LongTensor([itemid])]
    feature_tensor = Variable(torch.Tensor(feature).cuda()).unsqueeze(0)
    user_timediffs_tensor = Variable(torch.Tensor([user_timediff]).cuda()).unsqueeze(0)
    item_timediffs_tensor = Variable(torch.Tensor([item_timediff]).cuda()).unsqueeze(0)
    item_embedding_previous = item_embeddings[torch.cuda.LongTensor([itemid_previous])]

    # PROJECT USER EMBEDDING
    user_projected_embedding = model.forward(user_embedding_input, item_embedding_previous, timediffs=user_timediffs_tensor, features=feature_tensor, select='project')
    user_item_embedding = torch.cat([user_projected_embedding, item_embedding_previous, item_embeddings_static[torch.cuda.LongTensor([itemid_previous])], user_embedding_static_input], dim=1)

    # PREDICT ITEM EMBEDDING
    predicted_item_embedding = model.predict_item_embedding(user_item_embedding)

    # CALCULATE PREDICTION LOSS
    loss += MSELoss(predicted_item_embedding, torch.cat([item_embedding_input, item_embedding_static_input], dim=1).detach())

    # CALCULATE DISTANCE OF PREDICTED ITEM EMBEDDING TO ALL ITEMS
    euclidean_distances = nn.PairwiseDistance()(predicted_item_embedding.repeat(num_items, 1), torch.cat([item_embeddings, item_embeddings_static], dim=1)).squeeze(-1)

    # CALCULATE RANK OF THE TRUE ITEM AMONG ALL ITEMS
    true_item_distance = euclidean_distances[itemid]
    euclidean_distances_smaller = (euclidean_distances < true_item_distance).data.cpu().numpy()
    true_item_rank = np.sum(euclidean_distances_smaller) + 1
 
    #print(list(map(list(euclidean_distances).index, heapq.nsmallest(10, euclidean_distances))))
    #print(true_item_rank)
    #if j < test_start_idx:
    validation_ranks.append(true_item_rank)
    #else:
    test_ranks.append(true_item_rank)

    # UPDATE USER AND ITEM EMBEDDING
    # user_embedding_output = model.forward(user_embedding_input, item_embedding_input, timediffs=user_timediffs_tensor, features=feature_tensor, select='user_update')
    # item_embedding_output = model.forward(user_embedding_input, item_embedding_input, timediffs=item_timediffs_tensor, features=feature_tensor, select='item_update')
    if model.adj or model.no_zero or model.no_first:
        # user_adj_embedding = model.aggregate(item_embeddings, user_adj[userid], select='user_update', train=False)
        # item_adj_embedding = model.aggregate(user_embeddings, item_adj[itemid], select='item_update', train=False)
        if len(user_adj[userid]) == 0:
            user_adj_embedding = Variable(torch.zeros(1, model.embedding_dim).cuda())

        else:
            if not model.length:
                user_adj_, user_length_mask, user_max_length = adj_pad([user_adj[userid]])
                user_adj_em = item_embeddings[torch.LongTensor(user_adj_).cuda(), :]
            else:
                user_adj_, user_length_mask, user_max_length = adj_sample([user_adj[userid]], model.length)
                user_adj_em = item_embeddings[torch.LongTensor(user_adj_).cuda(), :]

            if model.method == 'attention':
                user_adj_embedding = model.aggregate_attention(user_adj_em, torch.LongTensor(user_length_mask),
                                                               user_max_length, user_embedding_input,
                                                               select='user_update')
            elif model.method == 'mean':
                user_adj_embedding = model.aggregate_mean(user_adj_em, torch.LongTensor(user_length_mask),
                                                              user_max_length, user_embedding_input, select='user_update')
            elif model.method == 'lstm':
                user_adj_embedding = model.aggregate_lstm(user_adj_em, torch.LongTensor(user_length_mask),
                                                          user_max_length, user_embedding_input,
                                                          select='user_update')
            elif model.method == 'gat':
                user_adj_embedding = model.aggregate_gat(user_adj_em, torch.LongTensor(user_length_mask),
                                                         user_max_length, user_embedding_input,
                                                         select='user_update')
        if len(item_adj[itemid]) == 0:
            item_adj_embedding = Variable(torch.zeros(1, model.embedding_dim).cuda())
        else:
            if not model.length:
                item_adj_, item_length_mask, item_max_length = adj_pad([item_adj[itemid]])
                item_adj_em = user_embeddings[torch.LongTensor(item_adj_).cuda(), :]
            else:
                item_adj_, item_length_mask, item_max_length = adj_sample([item_adj[itemid]],model.length)
                item_adj_em = user_embeddings[torch.LongTensor(item_adj_).cuda(), :]
            if model.method == 'attention':
                item_adj_embedding = model.aggregate_attention(item_adj_em, torch.LongTensor(item_length_mask),
                                                               item_max_length, item_embedding_input,
                                                               select='item_update')
            elif model.method == 'mean':
                item_adj_embedding = model.aggregate_mean(item_adj_em, torch.LongTensor(item_length_mask),
                                                                   item_max_length, item_embedding_input,
                                                                   select='item_update')
            elif model.method == 'lstm':
                item_adj_embedding = model.aggregate_lstm(item_adj_em, torch.LongTensor(item_length_mask),
                                     item_max_length, item_embedding_input,
                                     select='item_update')
            elif model.method == 'gat':
                item_adj_embedding = model.aggregate_gat(item_adj_em, torch.LongTensor(item_length_mask),
                                                         item_max_length, item_embedding_input,
                                                         select='item_update')
    else:
        user_adj_embedding = None
        item_adj_embedding = None
    user_embedding_output = model.forward(user_embedding_input, item_embedding_input,
                                          timediffs=user_timediffs_tensor, features=feature_tensor,
                                          adj_embeddings=user_adj_embedding, select='user_update')
    item_embedding_output = model.forward(user_embedding_input, item_embedding_input,
                                          timediffs=item_timediffs_tensor, features=feature_tensor,
                                          adj_embeddings=item_adj_embedding, select='item_update')

    # SAVE EMBEDDINGS
    item_embeddings[itemid,:] = item_embedding_output.squeeze(0)
    user_embeddings[userid,:] = user_embedding_output.squeeze(0)
    user_embeddings_timeseries[j, :] = user_embedding_output.squeeze(0)
    item_embeddings_timeseries[j, :] = item_embedding_output.squeeze(0)
    if model.adj or model.no_zero or model.no_first:
        # 计算user和item的邻居：
        if not model.length:
            user_adj[userid].add(itemid)  # 实时更新user和item的邻居 user_adj is dic, key is user_id ,value is item_id
            item_adj[itemid].add(userid)
        else:
            user_adj[userid].append(itemid)  # 实时更新user和item的邻居 user_adj is dic, key is user_id ,value is item_id
            item_adj[itemid].append(userid)

    # CALCULATE LOSS TO MAINTAIN TEMPORAL SMOOTHNESS
    loss += args.l2i*MSELoss(item_embedding_output, item_embedding_input.detach())
    loss += args.l2u*MSELoss(user_embedding_output, user_embedding_input.detach())

    # CALCULATE STATE CHANGE LOSS
    # if args.state_change:
    #     loss += calculate_state_prediction_loss(model, [j], user_embeddings_timeseries, y_true, crossEntropyLoss)

    # UPDATE THE MODEL IN REAL-TIME USING ERRORS MADE IN THE PAST PREDICTION
    if timestamp - tbatch_start_time > tbatch_timespan:
        tbatch_start_time = timestamp
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # RESET LOSS FOR NEXT T-BATCH
        loss = 0
        item_embeddings.detach_()
        user_embeddings.detach_()
        item_embeddings_timeseries.detach_()
        user_embeddings_timeseries.detach_()
            
# CALCULATE THE PERFORMANCE METRICS
performance_dict = dict()
ranks = validation_ranks
mrr = np.mean([1.0 / r for r in ranks])
rec10 = sum(np.array(ranks) <= 3)*1.0 / len(ranks)
performance_dict['validation'] = [mrr, rec10]

print(sum(np.array(ranks) <= 3)*1.0)
print(len(ranks))

ranks = test_ranks
mrr = np.mean([1.0 / r for r in ranks])
#print(ranks)
#print(len(ranks))
#print(np.array(ranks) <= 10)
rec10 = sum(np.array(ranks) <= 3)*1.0 / len(ranks)
performance_dict['test'] = [mrr, rec10]

print(sum(np.array(ranks) <= 3)*1.0)
print(len(ranks))

# PRINT AND SAVE THE PERFORMANCE METRICS
fw = open(output_fname, "a")
metrics = ['Mean Reciprocal Rank', 'Recall@3']
print( 'end time:', datetime.datetime.now())
print( '\n\n*** Validation performance of epoch %d ***' % args.epoch)
fw.write('\n\n*** Validation performance of epoch %d ***\n' % args.epoch)
for i in range(len(metrics)):
    print(metrics[i] + ': ' + str(performance_dict['validation'][i]))
    fw.write("Validation: " + metrics[i] + ': ' + str(performance_dict['validation'][i]) + "\n")
    
print( '\n\n*** Test performance of epoch %d ***' % args.epoch)
fw.write('\n\n*** Test performance of epoch %d ***\n' % args.epoch)
for i in range(len(metrics)):
    print(metrics[i] + ': ' + str(performance_dict['test'][i]))
    fw.write("Test: " + metrics[i] + ': ' + str(performance_dict['test'][i]) + "\n")

fw.flush()
fw.close()
