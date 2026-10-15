# Backup and recovery

After each milestone commit, run:

```powershell
powershell -NoProfile -File scripts/backup.ps1 -Destination F:\ReckonME_Backups
```

The script requires a clean tracked and untracked working tree, creates a dated
directory outside the project, archives HEAD, bundles all Git refs, verifies the
bundle, checks ZIP entries against tracked files and records SHA-256 hashes.
Ignored files (including scan data and credentials) are deliberately excluded.
Review staged content for secrets before every commit. This is a local archive;
copy it to independent storage for protection against disk or machine loss.

Recovery: `git clone <archive-directory>\history.bundle <new-directory>`.
Alternatively extract source.zip for committed files without Git history.
Compare file hashes with SHA256.txt before recovery. Never restore over existing
work. Re-run tests in the recovered directory.

## Private GitHub remote (owner setup)

GitHub CLI is unavailable in the inspected environment. In GitHub's website,
create a **private** empty repository named ReckonME (no initial README or license).
Then authenticate Git using Git Credential Manager or an SSH key and run:

```powershell
git remote add origin https://github.com/YOUR_ACCOUNT/ReckonME.git
git remote -v
git push -u origin main
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

If origin already exists, inspect it before changing anything. Verify the
repository's private visibility on GitHub and compare the two commit hashes.
Never put an access token in a remote URL or tracked file. Until that push and
comparison succeed, there is no verified remote backup.
