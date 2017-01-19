#!/usr/bin/env bash


DIR=/home/user

LIB=$DIR/ckan/lib
ETC=$DIR/ckan/etc
TMP=$DIR/tmp
BIN=$LIB/default/bin


if [ -f $DIR/ckan_installed ];
then
    echo "CKAN already installed."
    exit
fi


# Ckan config
echo "Ckan config"
INI=$ETC/default/development.ini
mkdir -p $ETC/default
cp $TMP/development.ini $ETC/default/development.ini

# Config solr
echo "Config solr"
mv /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.bak
ln -s $LIB/default/src/ckan/ckan/config/solr/schema.xml /etc/solr/conf/schema.xml
service jetty8 restart

# Install slider
echo "Install slider"
cd $LIB/default/src/ckan/ckanext-slider
$BIN/python setup.py develop

# Install banner
echo "Install banner"
cd $LIB/default/src/ckan/ckanext-banner
$BIN/python setup.py develop

# Config DB
echo 'Config DB'
cd $LIB/default/src/ckan
$BIN/paster db init -c $INI
$BIN/paster --plugin=ckan datastore set-permissions -c $INI

# Config who.ini
ln -s $LIB/default/src/ckan/who.ini $ETC/default/who.ini


touch $DIR/ckan_installed


echo 'CKAN successful installed.'
