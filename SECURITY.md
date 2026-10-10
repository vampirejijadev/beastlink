# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in Beastlink, please **do not** open a public issue.

Report it privately via one of these methods:

- **GitHub Security Advisories**: https://github.com/vampirejjjadev/beastlink/security/advisories/new
- **Discord**: https://discord.gg/jwo
- **Direct contact**: Open a private discussion with the maintainer on GitHub.

Please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You can expect:

- An acknowledgement within 48 hours
- A status update within 7 days
- Credit in the release notes once fixed (unless you prefer to stay anonymous)

## Security Considerations

### Cookies

`cookies/cookies.txt` grants full access to your YouTube account. Never:

- Commit it to a public repository
- Share it with untrusted parties
- Post it in issues or discussions

Beastlink already gitignores this file.

### Server Password

`beastlink.yml` contains the server password. Never:

- Use the default password (`youshallnotpass`) in production
- Expose the node's port to the public internet without a firewall
- Share the password in public channels

Recommended: bind the node to `127.0.0.1` if only local bots need it.

### Environment Variables

The `.env` file contains your Discord bot token. Never:

- Commit it to git
- Share it publicly
- Paste it in Discord or GitHub issues

If your token leaks, regenerate it immediately at https://discord.com/developers/applications
