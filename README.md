# certified_services_expiration_report

This script performs SSL certificate checks on target systems and extracts the desired information for a report.

Currently, the script only grabs:
- The certifying organization's name.
- The NotBefore date.
- The NotAfter date.
- The common name listed on the cert.