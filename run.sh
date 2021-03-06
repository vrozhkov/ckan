#!/usr/bin/env bash

docker run -d -it \
	--name ckan \
	-p 5000:5000 \
	-p 8983:8983 \
	-v $(pwd)/container/public:/home/user/ckan/lib/default/src/ckan/ckan/public \
	-v $(pwd)/container/templates:/home/user/ckan/lib/default/src/ckan/ckan/templates \
	-v $(pwd)/container/storage:/var/lib/ckan \
	-v $(pwd)/container/ckanext-slider:/home/user/ckan/lib/default/src/ckan/ckanext-slider \
	-v $(pwd)/container/ckanext-banner:/home/user/ckan/lib/default/src/ckan/ckanext-banner \
	-P ckan
