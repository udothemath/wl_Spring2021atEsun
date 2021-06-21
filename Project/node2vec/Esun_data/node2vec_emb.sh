epoch=100

for num in `seq 1 $epoch` # week without feature
do
    python ../src/main.py --input ../Esun_data/data/week_train_0.txt --output ../Esun_data/result/week_no_feature/week_res_$num.txt --dimensions 32 --walk-length 20 --num-walks 10 --window-size 5
done

for num in `seq 1 $epoch` # time without feature
do
    python ../src/main.py --input ../Esun_data/data/time_train_0.txt --output ../Esun_data/result/time_no_feature/time_res_$num.txt --dimensions 32 --walk-length 20 --num-walks 10 --window-size 5
done

for num in `seq 1 $epoch` # weektime without feature
do
    python ../src/main.py --input ../Esun_data/data/weektime_train_0.txt --output ../Esun_data/result/weektime_no_feature/weektime_res_$num.txt --dimensions 32 --walk-length 20 --num-walks 10 --window-size 5
done

for num in `seq 1 $epoch` # week with feature
do
    python ../src/main.py --input ../Esun_data/data/week_fea.txt --output ../Esun_data/result/week_feature/week_fres_$num.txt --dimensions 32 --walk-length 20 --num-walks 10 --window-size 5 --weighted
done

for num in `seq 1 $epoch` # time with feature
do
    python ../src/main.py --input ../Esun_data/data/time_fea.txt --output ../Esun_data/result/time_feature/time_fres_$num.txt --dimensions 32 --walk-length 20 --num-walks 10 --window-size 5 --weighted
done

for num in `seq 1 $epoch` # weektime with feature
do
    python ../src/main.py --input ../Esun_data/data/weektime_fea.txt --output ../Esun_data/result/weektime_feature/weektime_fres_$num.txt --dimensions 32 --walk-length 20 --num-walks 10 --window-size 5 --weighted
done

python ../Esun_data/recall_count.py --dir_path ../Esun_data/result/week_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 7 --user_start 800 --method Node2vec_week_without_feature 
python ../Esun_data/recall_count.py --dir_path ../Esun_data/result/time_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 6 --user_start 800 --method Node2vec_time_without_feature 
python ../Esun_data/recall_count.py --dir_path ../Esun_data/result/weektime_no_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 42 --user_start 800 --method Node2vec_weektime_without_feature 

python ../Esun_data/recall_count.py --dir_path ../Esun_data/result/week_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 7 --user_start 800 --method Node2vec_week_with_feature 
python ../Esun_data/recall_count.py --dir_path ../Esun_data/result/time_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 6 --user_start 800 --method Node2vec_time_with_feature 
python ../Esun_data/recall_count.py --dir_path ../Esun_data/result/weektime_feature --test ../Esun_data/data/test.txt --recall_num 3 5 10 --user_node 42 --user_start 800 --method Node2vec_weektime_with_feature 


