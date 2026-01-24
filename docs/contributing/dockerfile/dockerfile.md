# Dockerfile

We provide a <gh-file:docker/Dockerfile> to construct the image for running an OpenAI compatible server with vLLM.
More information about deploying with Docker can be found [here](../../deployment/docker.md).

Below is a visual representation of the multi-stage Dockerfile. The build graph contains the following nodes:

- All build stages
- The default build target (highlighted in grey)
- External images (with dashed borders)

The edges of the build graph represent:

- `FROM ...` dependencies (with a solid line and a full arrow head)

- `COPY --from=...` dependencies (with a dashed line and an empty arrow head)

- `RUN --mount=(.\*)from=...` dependencies (with a dotted line and an empty diamond arrow head)

  > <figure markdown="span">
  >   ![](../../assets/contributing/dockerfile-stages-dependency.png){ align="center" alt="query" width="100%" }
  > </figure>
  >
  > Made using: <https://github.com/patrickhoefler/dockerfilegraph>
  >
  > Commands to regenerate the build graph (make sure to run it **from the \`root\` directory of the vLLM repository** where the dockerfile is present):
  >
  > ```bash
  > dockerfilegraph \
  >   -o png \
  >   --legend \
  >   --dpi 200 \
  >   --max-label-length 50 \
  >   --filename docker/Dockerfile
  > ```
  >
  > or in case you want to run it directly with the docker image:
  >
  > ```bash
  > docker run \
  >    --rm \
  >    --user "$(id -u):$(id -g)" \
  >    --workdir /workspace \
  >    --volume "$(pwd)":/workspace \
  >    ghcr.io/patrickhoefler/dockerfilegraph:alpine \
  >    --output png \
  >    --dpi 200 \
  >    --max-label-length 50 \
  >    --filename docker/Dockerfile \
  >    --legend
  > ```
  >
  > (To run it for a different file, you can pass in a different argument to the flag `--filename`.)

## Build Arguments

The Dockerfile supports several build arguments for customization, particularly for hermetic builds and mirror configurations.

### Python Installation

vLLM uses [python-build-standalone](https://github.com/indygreg/python-build-standalone) for Python installation, which provides hermetic builds and better control over Python versions.

The following build arguments control Python installation:

- `PYTHON_BUILD_STANDALONE_MIRROR_URL`: Mirror URL for python-build-standalone releases (default: `https://github.com/astral-sh/python-build-standalone/releases/download`)
- `PYTHON_BUILD_STANDALONE_VERSION`: Release date of python-build-standalone (default: `20260114`)
- `PYTHON_INSTALL_DIR`: Installation directory for Python (default: `/opt/python`)

**Note**: Currently only Python 3.12.12 is supported (hardcoded).

#### Examples

Use a custom mirror (e.g., for air-gapped environments):

```bash
docker build \
  --build-arg PYTHON_BUILD_STANDALONE_MIRROR_URL="https://internal-mirror.example.com/python" \
  -f docker/Dockerfile .
```

Use a different python-build-standalone release:

```bash
docker build \
  --build-arg PYTHON_BUILD_STANDALONE_VERSION=20250120 \
  -f docker/Dockerfile .
```

Use a custom installation directory:

```bash
docker build \
  --build-arg PYTHON_INSTALL_DIR=/usr/local/python \
  -f docker/Dockerfile .
```

### Other Build Arguments

See the Dockerfile for additional build arguments related to PyTorch indexes, pip configuration, and CUDA settings.
