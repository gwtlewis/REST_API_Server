#!/usr/bin/env bash

if [ ! -d "./logs" ]; then
  mkdir ./logs
fi

pid=$(ps -ef | grep "REST" | grep -v grep | awk '{print $2}')

if [ -n "$pid" ]; then
    kill ${pid}
fi

nohup python ./REST.py 8888 >> ./logs/console.log &
