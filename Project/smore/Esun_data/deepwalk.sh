#set -x  # Print commands and their arguments as they are executed.
Threads=2
epoch=100

# Deep_Walk
for num in `seq 1 $epoch` # week without feature
do
    ../cli/deepwalk -train ../Esun_data/data/week.txt -save ../Esun_data/result/deepwalk/week_no_feature/week_emb_nof_$num.txt -undirected 1 -dimensions 32 -walk_times 10 -walk_steps 20 -window_size 5 -negative_samples 5 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # time without feature
do
    ../cli/deepwalk -train ../Esun_data/data/time.txt -save ../Esun_data/result/deepwalk/time_no_feature/time_emb_nof_$num.txt -undirected 1 -dimensions 32 -walk_times 10 -walk_steps 20 -window_size 5 -negative_samples 5 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # weektime without feature
do
    ../cli/deepwalk -train ../Esun_data/data/weektime.txt -save ../Esun_data/result/deepwalk/weektime_no_feature/weektime_emb_nof_$num.txt -undirected 1 -dimensions 32 -walk_times 10 -walk_steps 20 -window_size 5 -negative_samples 5 -alpha 0.025 -threads $Threads
done
##################
##################
for num in `seq 1 $epoch` # week with feature
do
    ../cli/deepwalk -train ../Esun_data/data/week_fea.txt -save ../Esun_data/result/deepwalk/week_feature/week_emb_$num.txt -undirected 1 -dimensions 32 -walk_times 10 -walk_steps 20 -window_size 5 -negative_samples 5 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # time with feature
do
    ../cli/deepwalk -train ../Esun_data/data/time_fea.txt -save ../Esun_data/result/deepwalk/time_feature/time_emb_$num.txt -undirected 1 -dimensions 32 -walk_times 10 -walk_steps 20 -window_size 5 -negative_samples 5 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # weektime with feature
do
    ../cli/deepwalk -train ../Esun_data/data/weektime_fea.txt -save ../Esun_data/result/deepwalk/weektime_feature/weektime_emb_$num.txt -undirected 1 -dimensions 32 -walk_times 10 -walk_steps 20 -window_size 5 -negative_samples 5 -alpha 0.025 -threads $Threads
done

# python3 ../recall_count.py [embedding data path] [test data path] [recall number list] [# of user nodes] [method]
# Without feature
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/deepwalk/week_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 7 --user_start 800 --method Deep_Walk_week_without_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/deepwalk/time_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 6 --user_start 800 --method Deep_Walk_time_without_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/deepwalk/weektime_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 42 --user_start 800 --method Deep_Walk_weektime_without_feature 

# With fea
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/deepwalk/week_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 7 --user_start 800 --method Deep_Walk_week_with_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/deepwalk/time_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 6 --user_start 800 --method Deep_Walk_time_with_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/deepwalk/weektime_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 42 --user_start 800 --method Deep_Walk_weektime_with_feature 