#!/usr/bin/env bash

# renew_data.sh
# sebsch 2018-03-06
# Script to automatically renew the Argo-Database


venv="/root/argo_venv"
argo_proto="/root/argo_proto"

_py="${venv}/bin/python"
_dumpfile="/tmp/argo_db.sql"

# Renew data
function renew_data(){
    printf " >> Downloading new data..."
    rsync -azh --delete vdmzrs.ifremer.fr::argo/aoml/ /root/aoml
    printf "\n\tdone.\n"

    ${_py} ${argo_proto}/manage.py rebuild_db

}

# Dump From TMPDB
function dump_tmpdb(){
    printf " >> Dumping tmpdb to ${_dumpfile} ..."
    PGPASSWORD=$TMPDBPASS pg_dump --no-acl --no-owner -U  argo_user -d argo_temp_db > ${_dumpfile}
    printf "\n\tdone. [`ls -ll ${_dumpfile}`]\n"
}

# Insert Dump into producton
function rewrite_production_data(){
    local DELETE_QUERY="DROP TABLE profiles, measurements, locations, argo_floats CASCADE;"
    printf " >> Renew production database ..."
    PGPASSWORD=$DBPASS psql -q -h localhost -d argo_db -U argo_user -c "${DELETE_QUERY}" > /dev/null
    PGPASSWORD=$DBPASS psql -q -h localhost -d argo_db -U argo_user -f ${_dumpfile}  > /dev/null
    printf "\n\tdone.\n"
}

# Renew cache
function renew_cache(){
    local URL="https://argo.geblubber.org/last_seen/${RENEW_TOKEN}"
    printf " >> Renew Argos cache..."
    curl ${URL} > /dev/null
    printf "\n\tdone.\n"
}


START=$(date +%s);
printf "(!) Starting renew process at `date`. \n"

renew_data
dump_tmpdb

s=$(date +%s)
rewrite_production_data
downtime="$(($(date +%s)-$s))"
renew_cache


printf "\nProcess finished.\n"
printf "This took  $(($(date +%s)-$START)) Seconds.\n"
printf "We had a downtime of ${downtime} Seconds.\n"
printf "So long and thanks for all the fish.\n\n\n\t\t\tEOS\n"

