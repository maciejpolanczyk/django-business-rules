#!/usr/bin/env bash
set -e

rm -rf build
mkdir build
cp -r plugin_setup/* build/
cp LICENSE.md build/
cp -r dbr/django_business_rules build/
cd build
python setup.py sdist
cd ..

docker build -t maciejpolanczyk/dbr-e2e-2 -f conf/e2e/python2/Dockerfile .
docker run maciejpolanczyk/dbr-e2e-2 python manage.py test

docker build -t maciejpolanczyk/dbr-e2e-3 -f conf/e2e/python3/Dockerfile .
docker run maciejpolanczyk/dbr-e2e-3 python3 manage.py test
