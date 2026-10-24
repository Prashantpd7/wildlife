"""Extract the registered Sylva Living World source bundle.
Downloads are expected at tools/sylva-living-world.json (via curl).
Writes the four registered files at their exact paths and verifies SHA-256."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # portfolio project root
BUNDLE = os.path.join(HERE, "sylva-living-world.json")

EXPECTED = {
    "src/shaders/sylva-living-world/SylvaLivingWorldScene.tsx":
        "e29b92a16596bc9383e1dbd4630e83b70ec2a59dbae48de1d3b7ddc48c0b2082",
    "src/shaders/sylva-living-world/sources/inner-green-3d.html":
        "69c3694bd63f44ef9f007ebe4dac57a83e4402e0cdf6b54dd10b96dd4f05e197",
    "src/shaders/sylva-living-world/sources/inner-green-assets/three.min.js":
        "8a5f7249903b54d30f79f708699d2fed2d6a1d0741a4cd41377d1f01bb5a2271",
    "src/shaders/threeui.css":
        "efe4447139f1358dd8e9be68edf6fa46cbefbd1de423a4d6c439ca61d2c8eccf",
}


def main() -> int:
    if not os.path.exists(BUNDLE):
        print("bundle not found:", BUNDLE)
        return 1
    with open(BUNDLE, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("id") != "sylva-living-world":
        print("unexpected bundle id:", data.get("id"))
        return 1
    ok = True
    for entry in data.get("files", []):
        path = entry.get("path")
        code = entry.get("code") or ""
        digest = hashlib.sha256(code.encode("utf-8")).hexdigest()
        expected = EXPECTED.get(path)
        status = "OK" if digest == expected else "MISMATCH"
        print(f"{status} {path} ({len(code)} bytes)")
        if digest != expected:
            ok = False
            continue
        dest = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(code)
    print("ALL VERIFIED" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
