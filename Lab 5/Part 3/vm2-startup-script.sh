
sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git clone https://github.com/cu-csci-4253-datacenter/flask-tutorial
cd /flask-tutorial
sudo python3 /flask-tutorial/setup.py install
sudo pip3 install -e /flask-tutorial


export FLASK_APP=/flask-tutorial/flaskr
cat $FLASK_APP >> output
flask init-db
nohup flask run -h 0.0.0.0 &