#!/bin/bash

if [ -d ./venv ]; then
    sudo rm -rf ./venv
fi

echo "Generating venv"
sudo python3.7 -m venv ./venv
source ./venv/bin/activate

echo "Upgrading pip"
sudo ./venv/bin/python3.7 -m pip install --upgrade pip
echo "Instaling requirements"
sudo ./venv/bin/python3.7 -m pip install -r ./requirements.txt

echo "Done!"
