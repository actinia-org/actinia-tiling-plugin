#!/usr/bin/env sh

# start valkey server
valkey-server &
sleep 1
valkey-cli ping

# # start webhook server
# webhook-server --host "0.0.0.0" --port "5005" &
# sleep 10

# run tests
echo $ACTINIA_CUSTOM_TEST_CFG
echo $DEFAULT_CONFIG_PATH

if [ "$1" = "dev" ]
then
  echo "Executing only 'dev' tests ..."
  pytest -m dev
elif [ "$1" = "integrationtest" ]
then
  pytest -m integrationtest
else
  pytest
fi

TEST_RES=$?

# stop valkey server
valkey-cli shutdown

return $TEST_RES
