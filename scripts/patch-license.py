#!/usr/bin/env python3
"""
Patches LicenseViewModel.swift to always set licenseState = .licensed,
bypassing trial/license validation entirely.
"""

import re
import sys

FILE = "VoiceInk/Models/LicenseViewModel.swift"

with open(FILE, "r") as f:
    content = f.read()

original = content

# Remove the #if LOCAL_BUILD / #else / #endif conditional in init(),
# keeping only: licenseState = .licensed
content = re.sub(
    r"(\binit\(\)\s*\{)\s*#if LOCAL_BUILD\s*\n"
    r"(\s*licenseState = \.licensed)\s*\n"
    r"\s*#else\s*\n"
    r"\s*loadLicenseState\(\)\s*\n"
    r"\s*#endif",
    r"\1\n\2",
    content,
)

if content == original:
    print(f"ERROR: patch pattern not found in {FILE}", file=sys.stderr)
    print(
        "Upstream may have changed LicenseViewModel.init(). Manual update needed.",
        file=sys.stderr,
    )
    sys.exit(1)

with open(FILE, "w") as f:
    f.write(content)

print(f"Patched {FILE} — licenseState always set to .licensed")
