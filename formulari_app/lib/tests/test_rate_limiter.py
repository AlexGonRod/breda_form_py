from formulari_app.lib.rate_limiter import RateLimiter


class TestRateLimiter:
    """Test suite for rate limiter."""

    def setup_method(self):
        """Reset rate limiter before each test."""
        RateLimiter.reset()

    def test_first_request_allowed(self):
        """First request should always be allowed."""
        allowed, msg = RateLimiter.is_allowed("192.168.1.1")
        assert allowed is True
        assert msg == "OK"

    def test_multiple_requests_within_limit(self):
        """Multiple requests within limit should be allowed."""
        ip = "192.168.1.1"

        # First 3 requests should be OK
        for i in range(3):
            allowed, msg = RateLimiter.is_allowed(ip)
            assert allowed is True, f"Request {i+1} should be allowed"

    def test_request_exceeds_limit(self):
        """4th request should be rejected."""
        ip = "192.168.1.2"

        # Fill limit
        for _ in range(RateLimiter.MAX_REQUESTS):
            RateLimiter.is_allowed(ip)

        # This should fail
        allowed, msg = RateLimiter.is_allowed(ip)
        assert allowed is False
        assert "Rate limit exceeded" in msg
        assert "Try again in" in msg

    def test_different_ips_separate_limits(self):
        """Different IPs should have separate rate limits."""
        ip1 = "192.168.1.1"
        ip2 = "192.168.1.2"

        # Fill limit for IP1
        for _ in range(RateLimiter.MAX_REQUESTS):
            RateLimiter.is_allowed(ip1)

        # IP1 should be limited
        allowed1, _ = RateLimiter.is_allowed(ip1)
        assert allowed1 is False

        # IP2 should still be allowed
        allowed2, msg2 = RateLimiter.is_allowed(ip2)
        assert allowed2 is True
        assert msg2 == "OK"

    def test_reset_single_ip(self):
        """Reset should clear limits for specific IP."""
        ip = "192.168.1.3"

        # Fill limit
        for _ in range(RateLimiter.MAX_REQUESTS):
            RateLimiter.is_allowed(ip)

        # Should be limited
        allowed, _ = RateLimiter.is_allowed(ip)
        assert allowed is False

        # Reset
        RateLimiter.reset(ip)

        # Should work again
        allowed, msg = RateLimiter.is_allowed(ip)
        assert allowed is True
        assert msg == "OK"

    def test_reset_all_ips(self):
        """Reset all should clear limits for all IPs."""
        ip1 = "192.168.1.4"
        ip2 = "192.168.1.5"

        # Fill limit for both
        for _ in range(RateLimiter.MAX_REQUESTS):
            RateLimiter.is_allowed(ip1)
            RateLimiter.is_allowed(ip2)

        # Reset all
        RateLimiter.reset()

        # Both should work
        for ip in [ip1, ip2]:
            allowed, msg = RateLimiter.is_allowed(ip)
            assert allowed is True
            assert msg == "OK"
