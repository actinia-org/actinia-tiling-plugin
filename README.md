# actinia-tiling-plugin

This is an example plugin for actinia-core which adds a "Hello World" endpoint to actinia-core.

You can run actinia-tiling-plugin as actinia-core plugin.

## Installation
Use docker-compose for installation:
```bash
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up -d
```

### Installation hints
* If you get an error like: `ERROR: for docker_kvdb_1  Cannot start service valkey: network xxx not found` you can try the following:
```bash
docker-compose -f docker/docker-compose.yml down
# remove all custom networks not used by a container
docker network prune
docker-compose -f docker/docker-compose.yml up -d
```

## DEV setup
For a DEV setup you can use the docker/docker-compose.yml:
```bash
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml run --rm --service-ports --entrypoint sh actinia

# install the plugin
(cd /src/actinia-tiling-plugin && pip3 install .)
# start actinia-core with your plugin
gunicorn -b 0.0.0.0:8088 -w 1 --access-logfile=- -k gthread actinia_core.main:flask_app
```

### Hints

* If you have no `.git` folder in the plugin folder, you need to set the
`SETUPTOOLS_SCM_PRETEND_VERSION` before installing the plugin:
```bash
export SETUPTOOLS_SCM_PRETEND_VERSION=0.0
```
Otherwise you will get an error like this
`LookupError: setuptools-scm was unable to detect version for '/src/actinia-tiling-plugin'.`.

* If you make changes in code and nothing changes you can try to uninstall the plugin:
```bash
pip3 uninstall actinia-tiling-plugin.wsgi -y
rm -rf /usr/lib/python3.8/site-packages/actinia_tiling_plugin.wsgi-*.egg
```

### Running tests
You can run the tests in the actinia docker:
```bash
docker build -f docker/actinia-tiling-plugin-test/Dockerfile -t actinia-tiling-plugin-test .

docker run -it actinia-tiling-plugin-test -i

cd /src/actinia-tiling-plugin/

# run all tests
make test
```

For debugging the test this might be helpful when a `waitAsyncStatusAssertHTTP` fails:
```python
from flask.json import loads as json_loads
resp_data = json_loads(rv.data)
rv_user_id = resp_data["user_id"]
rv_resource_id = resp_data["resource_id"]
rv2 = self.server.get(URL_PREFIX + "/resources/%s/%s" % (rv_user_id, rv_resource_id), headers=self.user_auth_header)
resp_data2 = json_loads(rv2.data)
```

## Small Example
```python
actinia_base_url=http://localhost:8088/api/v3
mapset_url=${actinia_base_url}/projects/loc_25832/mapsets/tiling_usermapset
auth="actinia-gdi:actinia-gdi"
```

### Grid Tiling Example
```bash
# grid tiling
# the region should be set correctly
json_reg=test_postbodies/set_region_for_epsg25832.json
curl -u ${auth} -X POST ${mapset_url}/processing_async -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json_reg} | jq
curl -u ${auth} -X GET ${mapset_url}/info | jq

# create tiling grid
curl -u ${auth} -X GET ${mapset_url}/vector_layers | jq
json=test_postbodies/grid_tiling_pb.json
curl -u ${auth} -X POST ${mapset_url}/tiling_processes/grid -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json} | jq
curl -u ${auth} -X GET ${mapset_url}/vector_layers | jq

# request tiling_processes
curl -u ${auth} -X GET ${mapset_url}/tiling_processes | jq
curl -u ${auth} -X GET ${mapset_url}/tiling_processes/grid | jq
```

### Processing Example as preparation for the merge
```bash
# process - tile 1
json=test_postbodies/grid_1_calulation.json
curl -u ${auth} -X POST ${mapset_url}_tmp1/processing_async -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json} | jq
curl -u ${auth} -X GET  "http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-..." | jq
curl -u ${auth} -X GET ${mapset_url}_tmp1/vector_layers | jq
curl -u ${auth} -X GET ${mapset_url}_tmp1/raster_layers | jq
curl -u ${auth} -X GET ${mapset_url}_tmp1/strds | jq

# process - tile 2
json=test_postbodies/grid_2_calulation.json
curl -u ${auth} -X POST ${mapset_url}_tmp2/processing_async -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json} | jq
curl -u ${auth} -X GET  "http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-..." | jq

# process - tile 3
json=test_postbodies/grid_3_calulation.json
curl -u ${auth} -X POST ${mapset_url}_tmp3/processing_async -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json} | jq
curl -u ${auth} -X GET  "http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-..." | jq
```

### Patch merge Example
```bash
json=test_postbodies/patch_merge_no_mapset_deletion.json
json=test_postbodies/patch_merge.json
curl -u ${auth} -X POST ${mapset_url}/merge_processes/patch -H 'accept: application/json' -H 'Content-Type: application/json' -d @${json} | jq
curl -u ${auth} -X GET ${mapset_url}/vector_layers | jq
curl -u ${auth} -X GET ${mapset_url}/raster_layers | jq
curl -u ${auth} -X GET ${mapset_url}/strds | jq

curl -u ${auth} -X GET ${actinia_base_url}/projects/loc_25832/mapsets | jq
```



## TODO
* Region statt Vector speichern (wie res setzen?)
