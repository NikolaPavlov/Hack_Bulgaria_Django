#!/bin/bash
# remove postgre database and create new one with the same name

DATABASE_NAME="myproject"
DATABASE_USER="myprojectuser"

if [[ -z "$DATABASE_NAME" ]]
then
  echo "No database name set. Using $1"
  DATABASE_NAME="$1"
fi

if [[ -z "$DATABASE_USER" ]]
then
  echo "No database user set. Using $2"
  DATABASE_USER="$2"
fi

echo "Using database $DATABASE_NAME with user $DATABASE_USER"

sudo -u postgres dropdb --if-exists "$DATABASE_NAME"
sudo -u postgres createdb -O "$DATABASE_USER" "$DATABASE_NAME"

python manage.py migrate




