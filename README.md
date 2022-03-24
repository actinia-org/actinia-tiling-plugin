# actinia-tiling-plugin

This is an example plugin for actinia-core which adds a "Hello World" endpoint to actinia-core.

You can run actinia-tiling-plugin as actinia-core plugin.

## Installation
Use docker-compose for installation:
```
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up -d
```

### Installation hints
* If you get an error like: `ERROR: for docker_redis_1  Cannot start service redis: network xxx not found` you can try the following:
```
docker-compose -f docker/docker-compose.yml down
# remove all custom networks not used by a container
docker network prune
docker-compose -f docker/docker-compose.yml up -d
```

### Requesting helloworld endpoint
You can test the plugin and request the `/helloworld` endpoint, e.g. with:
```
curl -u actinia-gdi:actinia-gdi -X GET http://localhost:8088/api/v2/helloworld | jq

curl -u actinia-gdi:actinia-gdi -H 'accept: application/json' -H 'Content-Type: application/json' -X POST http://localhost:8088/api/v2/helloworld -d '{"name": "test"}' | jq
```

## DEV setup
For a DEV setup you can use the docker/docker-compose.yml:
```
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml run --rm --service-ports --entrypoint sh actinia

# install the plugin
(cd /src/actinia-tiling-plugin && python3 setup.py install)
# start actinia-core with your plugin
gunicorn -b 0.0.0.0:8088 -w 1 --access-logfile=- -k gthread actinia_core.main:flask_app
```

### Hints

* If you have no `.git` folder in the plugin folder, you need to set the
`SETUPTOOLS_SCM_PRETEND_VERSION` before installing the plugin:
```
export SETUPTOOLS_SCM_PRETEND_VERSION=0.0
```
Otherwise you will get an error like this
`LookupError: setuptools-scm was unable to detect version for '/src/actinia-tiling-plugin'.`.

* If you make changes in code and nothing changes you can try to uninstall the plugin:
```
pip3 uninstall actinia-tiling-plugin.wsgi -y
rm -rf /usr/lib/python3.8/site-packages/actinia_tiling_plugin.wsgi-*.egg
```

### Running tests
You can run the tests in the actinia docker:
```
docker build -f docker/actinia-tiling-plugin-test/Dockerfile -t actinia-tiling-plugin-test .

docker run -it actinia-tiling-plugin-test -i

cd /src/actinia-tiling-plugin/

# run all tests
make test
```

## Tiling Example
```
actinia_base_url=http://localhost:8088/api/v2
mapset_url=${actinia_base_url}/locations/loc_25832/mapsets/hpda_tiling_user
auth="actinia-gdi:actinia-gdi"

curl -u ${auth} -X POST ${mapset_url} -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json} | jq
curl -u ${auth} -X GET ${mapset_url}/info | jq

# grid tiling
# the region should be set correctly
json_reg=test_postbodies/set_region_for_epsg25832.json
curl -u ${auth} -X POST ${mapset_url}/processing_async -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json_reg} | jq

json=test_postbodies/grid_tiling_pb.json
curl -u ${auth} -X POST ${mapset_url}/tiling_processes/grid -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json} | jq


curl -u ${auth} -X GET ${mapset_url}/tiling_processes/grid | jq

```
