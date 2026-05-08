## 2025-05-15 - SSRF Vulnerability in Web Adapter
**Vulnerability:** Server-Side Request Forgery (SSRF) in `WebAdapterService`. The service was fetching arbitrary URLs provided by users without validation, allowing access to internal resources (localhost, private network).
**Learning:** Initial attempt at fixing SSRF only checked the input URL. This is insufficient because:
1. `httpx` (and other libraries) follow redirects by default, allowing attackers to bypass initial checks via a redirect to an internal IP.
2. DNS rebinding can bypass IP checks if resolution happens multiple times.
3. IPv6 addresses must also be explicitly blocked.
**Prevention:**
1. Disable automatic redirects and manually validate each hop.
2. Use `socket.getaddrinfo` to resolve and check all associated IP addresses (v4 and v6).
3. Validate resolved IPs against a blacklist of private/reserved ranges before each request.
4. Use generic error messages to avoid leaking details about why a request failed.
