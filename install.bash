#!/bin/env bash

echo "Going into the /tmp folder"
cd /tmp

rm -rf ./man-brother
git clone git@github.com:erotourtes/man-brother.git --depth=1
cd man-brother

./start.bash

cd ..
echo "Removing this mess..."
rm -rf ./man-brother
