#!/usr/bin/env bash

if [ ! -d "./logs" ]; then
  mkdir ./logs
fi

nohup python ./REST.py 8888 >> ./logs/console.log &
