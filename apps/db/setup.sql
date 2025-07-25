CREATE DATABASE player_stats_db;

\c player_stats_db

rsync -avz --exclude-from='.rsyncignore' \
-e "ssh -i ~/.ssh/prayush-india-macbook.pem" \
. ubuntu@ec2-3-27-187-238.ap-southeast-2.compute.amazonaws.com:~/app
