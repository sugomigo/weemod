# Security & disclosure rules

Never contribute company-owned/customer code, proprietary documents, internal roadmaps, production datasets, account identifiers, API tokens, passwords, private keys, or credentials.

Before submitting a new module:
1. Verify original authorship, employment IP restrictions, contributor agreements, and license compatibility.
2. Use a new, clean project directory. Do not import Git history from private applications.
3. Scan files and commit diff for `.env`, credentials, hostnames, endpoints, secrets, customer data and internal architecture.
4. Review dependencies and package licenses; do not rely on secret scanning alone.
5. Run tests and compare exported files with the allowlist.

If a real secret is disclosed, revoke/rotate it immediately and follow the relevant provider's incident procedure. Deleting the file does not remove all copies or history.

Issues may disclose public vulnerabilities; avoid posting exploit details that would expose any private infrastructure.
