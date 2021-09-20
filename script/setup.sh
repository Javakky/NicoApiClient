python3 -m venv .venv
source `dirname $0`/../.venv/bin/activate
pip install -r requirements.txt
pip install wheel
python3 -m pip install --upgrade pip
sh `dirname $0`/../script/build.sh