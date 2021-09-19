rm -r `dirname $0`/../dist
rm -r `dirname $0`/../build
rm -r `dirname $0`/../nicovideo_api_client.egg-info
rm `dirname $0`/../README.rst
rm `dirname $0`/../requirements.txt
source `dirname $0`/../.venv/bin/activate
pip freeze -l > requirements.txt
sh `dirname $0`/make-docs.sh
pandoc --from markdown --to rst README.md -o README.rst
python setup.py sdist bdist_wheel