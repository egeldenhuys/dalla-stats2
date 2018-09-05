#!/bin/bash

set -e

log_dir="/var/local/dalla-stats"
date_string=`date -I"seconds"`
container_id=`docker container ls --filter volume=dalla_stats_data --format "{{.ID}}"`

mkdir -p $log_dir

file_path="$log_dir/dalla-stats-$date_string.sql"

docker exec $container_id /usr/bin/mysqldump -u root dalla_stats > $file_path

echo "Dalla Stats database has been exported to $file_path"

