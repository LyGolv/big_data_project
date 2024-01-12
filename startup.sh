#!/bin/bash
# startup.sh

# Start the services
start-dfs.sh
start-yarn.sh

# Create a list of users
users=("spark" "lygolv")

# Create a directory for each user in HDFS and change its owner accordingly
for user in "${users[@]}"
do
    hadoop fs -mkdir /user/${user}
    hadoop fs -chown ${user}:hadoop /user/${user}
done

# Keep the container running
tail -f /dev/null