# OIDC + PKCE quick notes

## What is PKCE
PKCE (Proof Key for Code Exchange) is an OAuth 2.0 extension that protects the authorization code flow for public clients (mobile, SPA) by binding the authorization code to a one-time secret. It was originally designed for mobile apps but is now recommended for all public clients, including SPAs.

## High-level flow
1. Client generates a random `code_verifier` (43-128 characters, URL-safe).
2. Client derives `code_challenge = BASE64URL(SHA256(code_verifier))` (S256 method).
3. Client starts authorization request with `code_challenge` and `code_challenge_method=S256`.
4. Authorization server issues an authorization code (bound to the challenge).
5. Client exchanges the code at the token endpoint, providing the original `code_verifier`.
6. Server validates that SHA256(code_verifier) matches the stored `code_challenge`.

## Why it helps
If an attacker intercepts the authorization code, they cannot redeem it without the `code_verifier`. This prevents authorization code interception attacks, especially important for public clients that cannot securely store client secrets.

## OIDC vs OAuth 2.0
- OAuth 2.0: authorization framework (delegated access to resources).
- OIDC (OpenID Connect): identity layer on top of OAuth 2.0 (authentication + user info).
- OIDC adds ID tokens (JWT) containing user identity claims.
- OAuth 2.0 access tokens are opaque or JWT; OIDC ID tokens are always JWT.

## Common flows
- Authorization Code Flow: most secure, requires client secret (or PKCE for public clients).
- Implicit Flow: deprecated, avoid using.
- Client Credentials: for service-to-service (no user involved).
- Device Flow: for devices with limited input capabilities.

## Security best practices
- Always use HTTPS in production.
- Use PKCE for public clients (SPAs, mobile apps).
- Store tokens securely (httpOnly cookies for web, secure storage for mobile).
- Validate ID token signature and claims (iss, aud, exp, nonce).
- Use short-lived access tokens with refresh tokens.
- Implement proper token rotation and revocation.

## Token types
- Access Token: short-lived, used to access protected resources.
- Refresh Token: long-lived, used to obtain new access tokens.
- ID Token: contains user identity claims (OIDC only).

## Common claims in ID token
- `sub`: subject (user ID)
- `iss`: issuer (authorization server)
- `aud`: audience (client ID)
- `exp`: expiration time
- `iat`: issued at time
- `nonce`: random value to prevent replay attacks

