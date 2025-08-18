# Security Policy

## Supported Versions

| Version | Supported          | End of Life |
|---------|-------------------|-------------|
| 2.5.x   | :white_check_mark:| TBD         |
| 2.4.x   | :white_check_mark:| TBD         |
| 2.3.x   | :white_check_mark:| TBD         |
| 2.2.x   | :white_check_mark:| TBD         |
| < 2.2.0 | :x:               | 2024-12-31  |

## Reporting a Vulnerability

We take the security of our EmailDuplicateCleaner project seriously. If you've discovered a security vulnerability, we appreciate your help in disclosing it to us in a responsible manner.

### How to Report

Please report security vulnerabilities by emailing our security team at nsfr750@yandex.com with the subject line: `[SECURITY] Vulnerability Report - [Brief Description]`

**Required Information:**
- Detailed description of the vulnerability
- Steps to reproduce the issue
- Impact of the vulnerability
- Environment details (OS, Python version, dependencies)
- Any proof-of-concept code (if available)
- Your name/handle for credit (optional)

### Our Response Process

1. **Acknowledgment**: You will receive a response within 48 hours confirming receipt
2. **Verification**: We will verify the reported vulnerability (1-3 business days)
3. **Assessment**: We will assess the impact and severity (2-5 business days)
4. **Fix Development**: We will develop a fix for the vulnerability
5. **Release**: We will release a patched version with security fixes
6. **Disclosure**: We will publish a security advisory

### Security Advisories

Security advisories will be published on our GitHub repository and will include:
- Description of the vulnerability
- Affected versions
- Impact assessment (CVSS score if applicable)
- Mitigation steps
- Credit to the reporter (if desired)

## Security Best Practices

### For Users
- Always use the latest stable version
- Review and understand the permissions requested by the application
- Run the application with the minimum required privileges
- Keep your system and Python environment updated
- Use virtual environments for isolation
- Never share sensitive information in public forums or issues

### For Developers
- Follow secure coding practices
- Use dependency scanning tools
- Implement input validation and sanitization
- Use secure defaults for all configurations
- Keep dependencies updated
- Implement proper error handling
- Follow the principle of least privilege

## Data Protection

EmailDuplicateCleaner handles sensitive email data. We are committed to:
- Processing data locally on your machine
- Not collecting or transmitting your email data to external servers
- Implementing appropriate encryption for sensitive operations
- Following data minimization principles

## Security Updates

We release security updates through:
- GitHub releases (tagged with [security])
- PyPI updates
- Security advisories on our repository

## Responsible Disclosure Policy

We follow responsible disclosure guidelines:
- We request a reasonable time (typically 90 days) to address reported vulnerabilities
- We will work with reporters to coordinate public disclosure
- We will credit security researchers who report vulnerabilities (if desired)
- We will not take legal action against security researchers acting in good faith

## Contact

**Security Team**: nsfr750@yandex.com  
**Project Maintainer**: Nsfr750  
**PGP Key**: Available upon request  
**Security Updates**: Watch/Star the GitHub repository for notifications

## Legal

By reporting a security vulnerability, you agree to follow this security policy and our code of conduct. We reserve the right to modify this policy at any time.

