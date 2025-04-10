FROM mundialis/actinia-core:latest as actinia_test

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG /etc/default/actinia-tiling-plugin-test

# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH /etc/default/actinia-tiling-plugin-test

# install things only for tests
RUN apk add valkey valkey-cli
RUN pip3 install iniconfig colorlog pwgen pytest pytest-cov

# COPY docker/actinia-tiling-plugin-test/start.sh /src/start.sh

ENTRYPOINT ["/bin/sh"]
CMD ["/src/start.sh"]

# add data for tests
RUN wget --quiet https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_micro.zip && \
  unzip nc_spm_08_micro.zip && \
  rm -f nc_spm_08_micro.zip && \
  mv nc_spm_08_micro /actinia_core/grassdb/nc_spm_08
RUN grass -e -c 'EPSG:4326' /actinia_core/grassdb/latlong_wgs84


# copy needed files and configs for test
COPY docker/actinia-tiling-plugin-test/actinia-tiling-plugin-test.cfg /etc/default/actinia
COPY docker/actinia-tiling-plugin-test/actinia-tiling-plugin-test.cfg /etc/default/actinia-tiling-plugin-test
COPY . /src/actinia-tiling-plugin/

WORKDIR /src/actinia-tiling-plugin/

RUN chmod a+x tests_with_kvdb.sh
RUN make install

# RUN make test
