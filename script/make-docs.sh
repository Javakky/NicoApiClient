cd `dirname $0`/../
cd docs
ls -a | grep -v -E '^\.$|^\.\.$|^conf.py$|^index.rst$|^make.bat$|^Makefile$|^_static$' | xargs rm -rf

cd ../
sphinx-apidoc -f -e -o ./docs ./nicovideo_api_client
cd docs
make html