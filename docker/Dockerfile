FROM mundialis/actinia-core:latest

# pwgen is needed for the tests
RUN pip3 install pwgen

COPY docker/actinia.cfg /etc/default/actinia
COPY . /src/actinia-tiling-plugin/

RUN pip3 uninstall actinia-tiling-plugin.wsgi -y
# SETUPTOOLS_SCM_PRETEND_VERSION is only needed if in the plugin folder is no
# .git folder
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0
RUN (cd /src/actinia-tiling-plugin && pip3 install .)
