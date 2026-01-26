#!/bin/bash
set -e

# Configuration
GITLAB_PROJECT_ID="67960847"
GITLAB_URL="https://gitlab.com"
DIST_DIR="artifacts/dist"

# Check for GITLAB_TOKEN
if [ -z "$GITLAB_TOKEN" ]; then
  echo "Error: GITLAB_TOKEN environment variable is not set"
  exit 1
fi

# Check if dist directory exists
if [ ! -d "$DIST_DIR" ]; then
  echo "Error: Directory $DIST_DIR does not exist"
  exit 1
fi

# Check if there are any wheel files
if ! ls "$DIST_DIR"/*.whl 1>/dev/null 2>&1; then
  echo "Error: No wheel files found in $DIST_DIR"
  exit 1
fi

# Install twine if not available
if ! command -v twine &>/dev/null; then
  echo "Installing twine..."
  pip install twine
fi

# GitLab PyPI registry URL using project ID
REPOSITORY_URL="${GITLAB_URL}/api/v4/projects/${GITLAB_PROJECT_ID}/packages/pypi"

echo "Publishing wheels to GitLab PyPI registry..."
echo "Project ID: $GITLAB_PROJECT_ID"
echo "Repository URL: $REPOSITORY_URL"
echo "Wheels to publish:"
ls -lh "$DIST_DIR"/*.whl

# Publish using twine
twine upload \
  --repository-url "$REPOSITORY_URL" \
  --username gitlab-ci-token \
  --password "$GITLAB_TOKEN" \
  "$DIST_DIR"/*.whl

echo "Successfully published packages to GitLab PyPI registry!"
echo ""
echo "To install from this registry, users can run:"
echo "pip install --index-url https://__token__:YOUR_TOKEN@gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/packages/pypi/simple yurts-vllm"
