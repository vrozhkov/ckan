#!/usr/bin/env bash


if [ -f /home/user/postgres_installed ];
then
    echo "Postgres already installed."
    exit
fi


echo "Create users: $POSTGRES_WRITE_USER, $POSTGRES_READ_USER"
sudo -u postgres createuser -S -D -R -l $POSTGRES_WRITE_USER
sudo -u postgres createuser -S -D -R -l $POSTGRES_READ_USER

echo "Change user passwords: $POSTGRES_WRITE_PASSWORD, $POSTGRES_READ_PASSWORD"
sudo -u postgres psql -c "ALTER USER $POSTGRES_WRITE_USER WITH PASSWORD '$POSTGRES_WRITE_PASSWORD';"
sudo -u postgres psql -c "ALTER USER $POSTGRES_READ_USER WITH PASSWORD '$POSTGRES_READ_PASSWORD';"

echo "Create DB: $POSTGRES_CKAN_DB, $POSTGRES_DS_DB"
sudo -u postgres createdb -O $POSTGRES_WRITE_USER $POSTGRES_CKAN_DB
sudo -u postgres createdb -O $POSTGRES_WRITE_USER $POSTGRES_DS_DB

#pg_dump --format=custom -d ckan_default > ckan_default.dump
#pg_dump --format=custom -d datastore_default > datastore_default.dump
#pg_restore --clean --if-exists -d ckan_default < ckan_default.dump
#pg_restore --clean --if-exists -d datastore_default < datastore_default.dump


touch /home/user/postgres_installed


echo 'Postgres successful installed.'
