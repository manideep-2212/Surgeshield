# Security

Implemented locally:
- JWT authentication
- bcrypt password hashing
- role-based access for organizer endpoints
- Helmet security headers
- CORS middleware
- API rate limiting
- parameterized PostgreSQL queries
- request IDs
- JSON body size limit
- duplicate/Idempotency protection

Production additions:
- HTTPS/TLS
- managed identity provider / OAuth2/OIDC
- secret manager
- WAF/bot protection
- audit logging
- stricter per-user/IP rate limits
- database encryption and backups
- least-privilege DB roles
- dependency and container scanning
