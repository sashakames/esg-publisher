#!/bin/bash

touch /tmp/pub_flag
srcdir=`dirname $0`

cd $srcdir

running=`ps -fe | grep pub-workflow | wc -l`

#source ~/miniforge3/etc/profile.d/conda.sh
#mamba activate replica

if [ $running -gt 1 ]
then
  exit 0
else
  echo No publisher process detected, starting!
  thedate=`date +%y%m%d_%H%M` ; time nohup python3 pub-workflow.py  --config esg.prod.yaml --cmor-tables /usr/local/cmip6-cmor-tables/Tables --flag-file /tmp/pub_flag > /esg/log/publisher/main/replica-pub.$thedate.log
fi
