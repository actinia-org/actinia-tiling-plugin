FROM mundialis/actinia-core:3.0.0 as actinia_test

LABEL authors="Carmen Tawalika,Anika Weinmann"
LABEL maintainer="tawalika@mundialis.de,weinmann@mundialis.de"

ENV ACTINIA_CUSTOM_TEST_CFG /etc/default/actinia-tiling-plugin-test

# TODO do not set DEFAULT_CONFIG_PATH if this is fixed
ENV DEFAULT_CONFIG_PATH /etc/default/actinia-tiling-plugin-test

# install things only for tests
RUN apk add redis
RUN pip3 install iniconfig colorlog pwgen

# COPY docker/actinia-tiling-plugin-test/start.sh /src/start.sh

ENTRYPOINT ["/bin/sh"]
CMD ["/src/start.sh"]

# copy needed files and configs for test
COPY docker/actinia-tiling-plugin-test/actinia-tiling-plugin-test.cfg /etc/default/actinia
COPY docker/actinia-tiling-plugin-test/actinia-tiling-plugin-test.cfg /etc/default/actinia-tiling-plugin-test
COPY . /src/actinia-tiling-plugin/

WORKDIR /src/actinia-tiling-plugin/

RUN chmod a+x tests_with_redis.sh
RUN make install

# RUN make test
