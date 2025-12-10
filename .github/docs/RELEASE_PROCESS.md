# Release Process

1. Ensure `develop` is stable and all PRs merged.
2. Create a release branch: `git checkout develop && git pull && git checkout -b release/vX.Y.Z`
3. Run tests & bump version in code (if applicable).
4. Merge `release/vX.Y.Z` into `main` via PR (include changelog).
5. Tag the release:
6. Deploy from `main`.
7. Merge `main` back into `develop`.
