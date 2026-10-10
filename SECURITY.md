# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in Beastlink, please do not open a public issue.

Report it privately:

- GitHub Security Advisories: https://github.com/vampirejjjadev/beastlink/security/advisories/new
- Discord: https://discord.gg/jwo

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You can expect an acknowledgement within 48 hours and a status update within 7 days.

## Security Considerations

### Cookies

`cookies/cookies.txt` grants full access to your YouTube account. Never commit it, share it, or post it publicly.

### Server Password

`beastlink.yml` contains the server password. Never use the default in production. Bind the node to `127.0.0.1` if only local bots need it.
