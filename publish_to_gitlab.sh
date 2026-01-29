#!/bin/bash

set -e -o pipefail

# Configuration
GITLAB_PROJECT_ID="67960847"
GITLAB_URL="https://gitlab.com"
DIST_DIR="artifacts/dist"

REPOSITORY_URL="${GITLAB_URL}/api/v4/projects/${GITLAB_PROJECT_ID}/packages/pypi"

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
  echo "Error: twine not installed..."
  exit 1
fi

echo "Publishing most recent wheel to GitLab PyPI registry..."

echo "Project ID: $GITLAB_PROJECT_ID"
echo "Repository URL: $REPOSITORY_URL"

for whl in "$DIST_DIR"/*.whl; do
  echo "Wheel to publish: $whl"
  # Publish using twine
  twine upload \
    --repository-url "$REPOSITORY_URL" \
    --username gitlab-ci-token \
    --password "$GITLAB_TOKEN" \
    "$whl"
  break
done

echo "Successfully published packages to GitLab PyPI registry!"
