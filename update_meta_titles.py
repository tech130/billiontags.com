import os
import re

# ─────────────────────────────────────────────
# CONFIGURATION  ← only change this line
# ─────────────────────────────────────────────

ROOT_DIR = r"D:\billiontags-bundle\billliontags.com"   # root folder containing all your HTML files

# The script tag to inject
NAV_SCRIPT_TAG = '<script src="/nav.js"></script>'

# ─────────────────────────────────────────────
# WHAT THIS SCRIPT DOES:
# Finds every HTML file and injects
#   <script src="/nav.js"></script>
# just before </head>
# Skips files that already have it
# ─────────────────────────────────────────────

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Skip if already has nav.js
    if '/nav.js' in content:
        return False, "already-injected"

    # Skip if no </head> tag found
    if not re.search(r'</head>', content, re.IGNORECASE):
        return False, "no-head-tag"

    # Inject just before </head>
    new_content = re.sub(
        r'(</head>)',
        f'  {NAV_SCRIPT_TAG}\n\\1',
        content,
        count=1,
        flags=re.IGNORECASE,
    )

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True, "updated"

    return False, "pattern-not-matched"


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    total     = 0
    updated   = 0
    already   = 0
    no_head   = 0
    no_match  = 0
    errors    = []

    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        # Skip hidden folders and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != 'node_modules']

        for filename in filenames:
            if not filename.lower().endswith('.html'):
                continue

            filepath = os.path.join(dirpath, filename)
            total += 1

            try:
                changed, reason = process_file(filepath)
                rel_path = os.path.relpath(filepath, ROOT_DIR)

                if changed:
                    updated += 1
                    print(f"[UPDATED]  {rel_path}")
                elif reason == "already-injected":
                    already += 1
                elif reason == "no-head-tag":
                    no_head += 1
                    print(f"[NO HEAD]  {rel_path}  ← no </head> tag found")
                elif reason == "pattern-not-matched":
                    no_match += 1
                    print(f"[NO MATCH] {rel_path}  ← check manually")

            except Exception as e:
                errors.append(filepath)
                print(f"[ERROR]    {filepath} — {e}")

    print(f"\n{'='*65}")
    print(f"  Total HTML files scanned : {total}")
    print(f"  Files updated            : {updated}")
    print(f"  Already had nav.js       : {already}")
    print(f"  No </head> tag found     : {no_head}")
    print(f"  Pattern not matched      : {no_match}")
    print(f"  Errors                   : {len(errors)}")
    print(f"{'='*65}")

    if errors:
        print("\nFailed files:")
        for e in errors:
            print(f"  {e}")


if __name__ == "__main__":
    main()