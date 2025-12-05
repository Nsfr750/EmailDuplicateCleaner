# Troubleshooting Guide

This guide helps you resolve common issues with EmailDuplicateCleaner. If you don't find your issue here, please check the [GitHub Issues](https://github.com/Nsfr750/EmailDuplicateCleaner/issues) or submit a new one.

## Table of Contents

1. [Connection Issues](#connection-issues)
2. [Performance Problems](#performance-problems)
3. [Duplicate Detection](#duplicate-detection-issues)
4. [Error Messages](#error-messages)
5. [Common Questions](#common-questions)
6. [Getting Help](#getting-help)

## Connection Issues

### Can't connect to email server

**Symptoms:**
- "Connection timed out" error
- "Invalid credentials" message
- Connection drops frequently

**Solutions:**
1. **Check your internet connection**
   - Ensure you have a stable internet connection
   - Try accessing your email through webmail to verify connectivity

2. **Verify server settings**
   - Double-check server addresses and ports
   - Ensure SSL/TLS settings are correct
   - Example settings for common providers:
     - Gmail: imap.gmail.com (993), smtp.gmail.com (465/587)
     - Outlook: outlook.office365.com (993), smtp.office365.com (587)

3. **App passwords**
   - For Gmail, you might need to generate an "App Password" if 2FA is enabled
   - Go to Google Account > Security > App passwords

## Performance Problems

### Application is slow

**Solutions:**
1. **Reduce batch size**
   - Decrease the number of emails processed at once
   - Settings > Performance > Batch size

2. **Limit scan scope**
   - Select specific folders instead of scanning all
   - Use date filters to limit the time range

3. **Free up system resources**
   - Close other memory-intensive applications
   - Increase system memory if possible

## Duplicate Detection Issues

### Missing duplicates

**Solutions:**
1. **Adjust sensitivity**
   - Increase the similarity threshold
   - Settings > Duplicate Detection > Sensitivity

2. **Check comparison settings**
   - Verify which fields are being compared
   - Enable/disable attachment comparison as needed

3. **Rescan with different parameters**
   - Try different date ranges
   - Include/exclude specific folders

## Error Messages

### "Authentication Failed"
- Verify your username and password
- Check if your account is locked
- For Gmail, allow less secure apps or use an App Password

### "Connection Refused"
- Check if your firewall is blocking the connection
- Verify the server address and port
- Contact your email provider for the correct settings

### "Out of Memory"
- Reduce the number of emails processed at once
- Close other applications
- Allocate more memory to the application if possible

## Common Questions

### How do I update the application?
1. Check for updates in Help > Check for Updates
2. Or download the latest version from GitHub
3. Your settings will be preserved during updates

### Where are my settings stored?
- Windows: `%APPDATA%\EmailDuplicateCleaner\`
- macOS: `~/Library/Application Support/EmailDuplicateCleaner/`
- Linux: `~/.config/EmailDuplicateCleaner/`

### How do I reset the application?
1. Close the application
2. Delete the configuration directory (see above)
3. Restart the application

## Getting Help

### Before submitting an issue:
1. Check the logs in `Help > View Logs`
2. Note the exact error message
3. Check if the issue is already reported on GitHub

### When submitting an issue:
1. Include the error message
2. Describe what you were doing when the error occurred
3. Attach relevant log files (remove sensitive information)
4. Include your operating system and application version
