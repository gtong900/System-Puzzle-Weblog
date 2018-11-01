#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER --dbname $POSTGRES_DB <<-EOSQL
        CREATE TABLE  weblogs (
               day    date,
               status varchar(3),
               source varchar(6)
               );
EOSQL
