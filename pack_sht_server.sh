#!/bin/bash

rm ./sht_server/__pycache__/ -rf
rm ./sht_server/sht.log* -f
rm ./sht_server/server.log* -f

tar czvf sht_server.tar.gz sht_server
