rm -r dist build nicovideo_api_client.egg-info README.rst
pandoc --from markdown --to rst README.md -o README.rst
python setup.py sdist bdist_wheel