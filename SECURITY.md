# Security Policy

## Report a vulnerability

Please do not open a public issue for vulnerabilities that expose credentials, private data, or an approval bypass. Contact the maintainer privately through the email listed on the maintainer's public GitHub profile.

## Data handling

The reference implementation is local and file-first. It does not transmit task content to a model provider by itself. Deployers are responsible for reviewing the privacy, retention, and authorization terms of any model or integration they add.

Never place the following in a public task or delivery artifact:

- API keys, passwords, tokens, cookies, or signing secrets;
- customer identities or production records without authorization;
- contracts, pricing, personal identifiers, or unpublished application data;
- internal file paths that reveal sensitive organization structure.

## Approval bypasses

The validator is a guardrail, not an access-control system. Production deployments should enforce external-action approval in the system that actually sends, publishes, deploys, purchases, signs, or deletes.
