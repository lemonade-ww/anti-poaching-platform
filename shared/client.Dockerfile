FROM openapitools/openapi-generator-cli
RUN useradd -m client
USER client
