FROM alpine:3.6

RUN apk --no-cache update && \
    apk --no-cache add python py-pip py-setuptools ca-certificates groff less && \
    pip --no-cache-dir install awscli && \
    pip install --upgrade pip && \
    rm -rf /var/cache/apk/*


# WORKDIR /data
CMD ["/bin/bash"]