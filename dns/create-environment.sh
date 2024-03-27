#!/bin/bash

echo "-------------- Creating Environment --------------"
python3 -m venv dns_env
source dns_env/bin/activate
echo "-------------- Installing requirements --------------"
pip install -r requirements.txt
