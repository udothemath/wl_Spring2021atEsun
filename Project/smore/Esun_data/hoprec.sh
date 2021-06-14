#set -x  # Print commands and their arguments as they are executed.
Threads=2
epoch=100

# Hop-Rec
for num in `seq 1 $epoch` # weektime without feature
do
    ../cli/hoprec -train ../Esun_data/data/week.txt -field ../Esun_data/data/week_vf.txt -save ../Esun_data/result/hoprec/week_no_feature/week_emb_$num.txt -dimensions 32 -sample_times 10 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # weektime without feature
do
    ../cli/hoprec -train ../Esun_data/data/time.txt -field ../Esun_data/data/time_vf.txt -save ../Esun_data/result/hoprec/time_no_feature/time_emb_$num.txt -dimensions 32 -sample_times 10 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # weektime without feature
do
    ../cli/hoprec -train ../Esun_data/data/weektime.txt -field ../Esun_data/data/weektime_vf.txt -save ../Esun_data/result/hoprec/weektime_no_feature/weektime_emb_$num.txt -dimensions 32 -sample_times 10 -alpha 0.025 -threads $Threads
done

########################
for num in `seq 1 $epoch` # weektime with feature
do
    ../cli/hoprec -train ../Esun_data/data/week_fea.txt -field ../Esun_data/data/week_vf.txt -save ../Esun_data/result/hoprec/week_feature/week_fea_emb_$num.txt -dimensions 32 -sample_times 10 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # weektime with feature
do
    ../cli/hoprec -train ../Esun_data/data/time_fea.txt -field ../Esun_data/data/time_vf.txt -save ../Esun_data/result/hoprec/time_feature/time_fea_emb_$num.txt -dimensions 32 -sample_times 10 -alpha 0.025 -threads $Threads
done

for num in `seq 1 $epoch` # weektime with feature
do
    ../cli/hoprec -train ../Esun_data/data/weektime_fea.txt -field ../Esun_data/data/weektime_vf.txt -save ../Esun_data/result/hoprec/weektime_feature/weektime_fea_emb_$num.txt -dimensions 32 -sample_times 10 -alpha 0.025 -threads $Threads
done

# python3 ../recall_count.py [embedding data path] [test data path] [recall number list] [# of user nodes] [method]
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/hoprec/week_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 7 --user_start 800 --method Hop_Rec_week_without_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/hoprec/time_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 6 --user_start 800 --method Hop_Rec_time_without_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/hoprec/weektime_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 42 --user_start 800 --method Hop_Rec_weektime_without_feature 

python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/hoprec/week_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 7 --user_start 800 --method Hop_Rec_week_with_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/hoprec/time_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 6 --user_start 800 --method Hop_Rec_time_with_feature 
python3 ../Esun_data/recall_count.py --dir_path ../Esun_data/result/hoprec/weektime_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 42 --user_start 800 --method Hop_Rec_weektime_with_feature