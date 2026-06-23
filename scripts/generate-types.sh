#!/bin/bash
set -e

echo "Generating TypeScript types from OpenAPI specs..."

# Install openapi-typescript if not present
if ! command -v openapi-typescript &> /dev/null; then
    npm install -g openapi-typescript
fi

# Generate types for each service
for spec in shared/openapi/*.yaml; do
    service=$(basename "$spec" .yaml)
    echo "  Generating types for $service..."
    openapi-typescript "$spec" -o "shared/types/${service}.d.ts"
done

echo "Done!"

chmod +x scripts/generate-types.sh