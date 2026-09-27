# meridian-pay-pipeline

Minimal Flask app with a CI/CD pipeline demonstrating: unit testing, container
build, vulnerability scanning, SBOM generation, and image signing.

## Local development

```bash
pip install -r requirements-dev.txt
pytest
python wsgi.py
```

## Docker

```bash
docker build -t meridian-pay:local .
docker run -p 8000:8000 meridian-pay:local
```

## Pipeline (`.github/workflows/ci-cd.yml`)

On every push/PR to `main`:

1. **test** — installs deps and runs `pytest` with coverage.
2. **build-scan-sign** (after tests pass):
   - Builds the Docker image with Buildx.
   - Scans the image with [Trivy](https://github.com/aquasecurity/trivy) and
     fails the build on unfixed CRITICAL/HIGH vulnerabilities.
   - Generates an SPDX SBOM with [Syft](https://github.com/anchore/syft) and
     uploads it as a workflow artifact.
   - On pushes to `main`: pushes the image to GHCR, signs it keylessly with
     [Cosign](https://github.com/sigstore/cosign) via GitHub's OIDC identity,
     and attests the SBOM to the image.

### Verifying a signed image

`<sha>` must be the **full** 40-character commit SHA (that's the tag the
pipeline pushes) — `git rev-parse HEAD`, not the short SHA shown in the
Actions UI.

Bash/macOS/Linux:

```bash
cosign verify \
  --certificate-identity-regexp "https://github.com/<owner>/<repo>/.github/workflows/ci-cd.yml@.*" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/<owner>/<repo>:<sha>
```

PowerShell:

```powershell
cosign verify `
  --certificate-identity-regexp "https://github.com/<owner>/<repo>/.github/workflows/ci-cd.yml@.*" `
  --certificate-oidc-issuer https://token.actions.githubusercontent.com `
  ghcr.io/<owner>/<repo>:<sha>
```
