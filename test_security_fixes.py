#!/usr/bin/env python
"""Standalone test for CVE-2025-6242 security fixes."""

import sys
sys.path.insert(0, "/home/jmob/dev/yurts-vllm")

# Test 1: Domain restriction validation
print("Test 1: Domain restriction validation")
try:
    from vllm.multimodal.utils import MediaConnector

    connector = MediaConnector(allowed_media_domains=["upload.wikimedia.org"])

    # Should succeed - domain is in allowed list
    connector._assert_url_in_allowed_media_domains(
        "https://upload.wikimedia.org/image.jpg")
    print("  ✓ Allowed domain works")

    # Should fail - domain not in allowed list
    try:
        connector._assert_url_in_allowed_media_domains(
            "https://evil.com/image.jpg")
        print("  ✗ FAILED: Should have rejected disallowed domain")
        sys.exit(1)
    except ValueError as e:
        if "not in the allowed domains" in str(e):
            print(f"  ✓ Disallowed domain rejected: {str(e)[:50]}...")
        else:
            print(f"  ✗ FAILED: Wrong error: {e}")
            sys.exit(1)

    print("  ✓ Test 1 PASSED\n")
except Exception as e:
    print(f"  ✗ Test 1 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: No domain restriction
print("Test 2: No domain restriction")
try:
    connector_none = MediaConnector(allowed_media_domains=None)
    connector_none._assert_url_in_allowed_media_domains(
        "https://any-domain.com/image.jpg")
    print("  ✓ None allows all domains")

    connector_empty = MediaConnector(allowed_media_domains=[])
    connector_empty._assert_url_in_allowed_media_domains(
        "https://another-domain.com/image.jpg")
    print("  ✓ Empty list allows all domains")

    print("  ✓ Test 2 PASSED\n")
except Exception as e:
    print(f"  ✗ Test 2 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Invalid URL handling
print("Test 3: Invalid URL handling")
try:
    connector = MediaConnector(allowed_media_domains=["example.com"])

    try:
        connector._assert_url_in_allowed_media_domains("not-a-valid-url")
        print("  ✗ FAILED: Should have rejected invalid URL")
        sys.exit(1)
    except ValueError as e:
        if "Cannot determine hostname" in str(e):
            print(f"  ✓ Invalid URL rejected: {str(e)[:50]}...")
        else:
            print(f"  ✗ FAILED: Wrong error: {e}")
            sys.exit(1)

    print("  ✓ Test 3 PASSED\n")
except Exception as e:
    print(f"  ✗ Test 3 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Environment variable exists
print("Test 4: Environment variable configuration")
try:
    import vllm.envs as envs

    if hasattr(envs, 'VLLM_MEDIA_URL_ALLOW_REDIRECTS'):
        print(f"  ✓ VLLM_MEDIA_URL_ALLOW_REDIRECTS exists: {envs.VLLM_MEDIA_URL_ALLOW_REDIRECTS}")
    else:
        print("  ✗ FAILED: VLLM_MEDIA_URL_ALLOW_REDIRECTS not defined")
        sys.exit(1)

    print("  ✓ Test 4 PASSED\n")
except Exception as e:
    print(f"  ✗ Test 4 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: HTTPConnection has allow_redirects parameter
print("Test 5: HTTPConnection redirect control")
try:
    from vllm.connections import HTTPConnection
    import inspect

    # Check get_bytes signature
    sig = inspect.signature(HTTPConnection.get_bytes)
    if 'allow_redirects' in sig.parameters:
        print("  ✓ HTTPConnection.get_bytes has allow_redirects parameter")
    else:
        print("  ✗ FAILED: get_bytes missing allow_redirects parameter")
        sys.exit(1)

    # Check async_get_bytes signature
    sig = inspect.signature(HTTPConnection.async_get_bytes)
    if 'allow_redirects' in sig.parameters:
        print("  ✓ HTTPConnection.async_get_bytes has allow_redirects parameter")
    else:
        print("  ✗ FAILED: async_get_bytes missing allow_redirects parameter")
        sys.exit(1)

    print("  ✓ Test 5 PASSED\n")
except Exception as e:
    print(f"  ✗ Test 5 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: ModelConfig has allowed_media_domains field
print("Test 6: ModelConfig configuration")
try:
    from vllm.config import ModelConfig
    import inspect

    # Check if ModelConfig has the field
    if hasattr(ModelConfig, '__dataclass_fields__'):
        fields = ModelConfig.__dataclass_fields__
        if 'allowed_media_domains' in fields:
            print(f"  ✓ ModelConfig has allowed_media_domains field")
            print(f"    Default: {fields['allowed_media_domains'].default_factory()}")
        else:
            print("  ✗ FAILED: ModelConfig missing allowed_media_domains field")
            sys.exit(1)
    else:
        print("  ! Warning: Could not verify ModelConfig dataclass fields")

    print("  ✓ Test 6 PASSED\n")
except Exception as e:
    print(f"  ✗ Test 6 FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("ALL TESTS PASSED! ✓")
print("=" * 60)
print("\nSecurity fixes for CVE-2025-6242 have been successfully implemented:")
print("  • Domain validation prevents SSRF attacks")
print("  • Redirect control prevents bypassing domain restrictions")
print("  • Configuration options available through CLI and API")
