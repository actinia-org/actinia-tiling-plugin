FROM mundialis/actinia-core:g79-latest-alpine

# pwgen is needed for the tests
RUN pip3 install pwgen

COPY docker/actinia.cfg /etc/default/actinia
COPY src /src/actinia-tiling-plugin/src/
COPY setup.cfg /src/actinia-tiling-plugin/
COPY setup.py /src/actinia-tiling-plugin/
COPY requirements.txt /src/actinia-tiling-plugin/

RUN pip3 install -r /src/actinia-tiling-plugin/requirements.txt
RUN pip3 uninstall actinia-tiling-plugin.wsgi -y
# SETUPTOOLS_SCM_PRETEND_VERSION is only needed if in the plugin folder is no
# .git folder
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0
RUN (cd /src/actinia-tiling-plugin && python3 setup.py install)
