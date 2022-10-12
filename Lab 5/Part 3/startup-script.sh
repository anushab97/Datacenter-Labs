#Script for downloading vm2 files
#!/bin/bash

sudo apt-get update 
sudo apt-get install -y python3 python3-pip git
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

curl http://metadata/computeMetadata/v1/instance/attributes/vm2-startup-script -H "Metadata-Flavor: Google" > vm2-startup-script.sh 
curl http://metadata/computeMetadata/v1/instance/attributes/service-credentials -H "Metadata-Flavor: Google" > service-credentials.json
curl http://metadata/computeMetadata/v1/instance/attributes/vm1-launch-vm2-code -H "Metadata-Flavor: Google" > vm1-launch-vm2-code.py

python3 ./vm1-launch-vm2-code.py --project "avian-compiler-324721" --bucket_name "datacenterbucket1" --zone "us-west1-b" --name "vm02"