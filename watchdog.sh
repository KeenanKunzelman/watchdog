# ./watchdog /path/to/monitor weekly 

#!/bin/bash

if [ $1=="hourly" ]
then
    mv execute.sh /etc/cron.hourly/
elif [ $1=="daily" ]
then
    mv execute.sh /etc/cron.daily/

elif [ $1=="weekly" ]
then
    mv execute.sh /etc/cron.weekly/

elif [ $1=="monthly"]
then
    mv execute.sh /etc/cron.monthly/
fi