import os
import re
import shutil

# ─────────────────────────────────────────────
# CONFIGURATION  ← only change this line
# ─────────────────────────────────────────────

ROOT_DIR = r"D:\billliontags.com"   # folder containing ALL folders

BASE_URL = "https://www.billiontags.com"

# ─────────────────────────────────────────────
# COUNTRY MAP
# source folder  →  (destination folder, display name)
#
# SOURCE:  ROOT_DIR/australia/index.html          ← market page content
# DEST:    ROOT_DIR/multicultural-marketing-.../market/index.html
# ─────────────────────────────────────────────

COUNTRIES = {
    "australia":   ("multicultural-marketing-company-in-australia",   "Australia"),
    "canada":      ("multicultural-marketing-company-in-canada",      "Canada"),
    "malaysia":    ("multicultural-marketing-company-in-malaysia",    "Malaysia"),
    "new-zealand": ("multicultural-marketing-company-in-new-zealand", "New Zealand"),
    "singapore":   ("multicultural-marketing-company-in-singapore",   "Singapore"),
    "south-africa":("multicultural-marketing-company-in-south-africa","South Africa"),
    "uae":         ("multicultural-marketing-company-in-uae",         "UAE"),
    "uk":          ("multicultural-marketing-company-in-uk",          "UK"),
    "usa":         ("multicultural-marketing-company-in-usa",         "USA"),
}


# ─────────────────────────────────────────────
# BUILD META CONTENT
# ─────────────────────────────────────────────

def get_meta(dest_folder, display):
    canonical = f"{BASE_URL}/{dest_folder}/market/"
    title = (
        f"Multicultural Marketing in {display} | "
        f"Immigrant & Ethnic Market Insights – Billiontags"
    )
    desc = (
        f"Explore {display}'s multicultural market. Billiontags provides deep insights "
        f"into immigrant and ethnic audience demographics to help brands build effective, "
        f"inclusive marketing strategies."
    )
    return title, desc, canonical


# ─────────────────────────────────────────────
# UPDATE ALL META TAGS IN HTML FILE
# ─────────────────────────────────────────────

def update_html(filepath, title, desc, canonical):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content

    # 1. <title>
    content = re.sub(
        r"(<title>)(.*?)(</title>)",
        lambda m: m.group(1) + title + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 2. og:title
    content = re.sub(
        r'(<meta\s+property=["\']og:title["\']\s+content=["\'])(.*?)(["\'](\s*/)?>)',
        lambda m: m.group(1) + title + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 3. twitter:title
    content = re.sub(
        r'(<meta\s+name=["\']twitter:title["\']\s+content=["\'])(.*?)(["\'](\s*/)?>)',
        lambda m: m.group(1) + title + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 4. meta description
    content = re.sub(
        r'(<meta\s+name=["\']description["\']\s+content=["\'])(.*?)(["\'](\s*/)?>)',
        lambda m: m.group(1) + desc + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 5. og:description
    content = re.sub(
        r'(<meta\s+property=["\']og:description["\']\s+content=["\'])(.*?)(["\'](\s*/)?>)',
        lambda m: m.group(1) + desc + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 6. twitter:description
    content = re.sub(
        r'(<meta\s+name=["\']twitter:description["\']\s+content=["\'])(.*?)(["\'](\s*/)?>)',
        lambda m: m.group(1) + desc + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 7. canonical (rel first) — re.DOTALL handles newlines inside href
    content = re.sub(
        r'(<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\'])(.*?)(["\'][^>]*>)',
        lambda m: m.group(1) + canonical + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 7b. canonical (href first) — re.DOTALL handles newlines inside href
    content = re.sub(
        r'(<link\s+[^>]*href=["\'])(.*?)(["\'][^>]*rel=["\']canonical["\'][^>]*>)',
        lambda m: m.group(1) + canonical + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )
    # 8. og:url
    content = re.sub(
        r'(<meta\s+property=["\']og:url["\']\s+content=["\'])(.*?)(["\'](\s*/)?>)',
        lambda m: m.group(1) + canonical + m.group(3),
        content, flags=re.IGNORECASE | re.DOTALL,
    )

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    copied  = 0
    updated = 0
    skipped = 0
    errors  = []

    for src_folder, (dest_folder, display) in COUNTRIES.items():

        # ── Source: australia/index.html ──
        src_file = os.path.join(ROOT_DIR, src_folder, "index.html")

        # ── Destination: multicultural-.../market/index.html ──
        market_path = os.path.join(ROOT_DIR, dest_folder, "market")
        dest_file   = os.path.join(market_path, "index.html")

        print(f"\n{'='*65}")
        print(f"  Country : {display}")

        # Validate source
        if not os.path.isfile(src_file):
            print(f"[WARNING] Source not found: {src_folder}/index.html — skipping")
            continue

        # Validate destination country folder exists
        dest_country_path = os.path.join(ROOT_DIR, dest_folder)
        if not os.path.isdir(dest_country_path):
            print(f"[WARNING] Dest folder not found: {dest_folder}/ — skipping")
            continue

        # Create market/ subfolder
        os.makedirs(market_path, exist_ok=True)

        # Copy source → dest/market/index.html  (overwrite if exists)
        shutil.copy2(src_file, dest_file)
        copied += 1
        print(f"[COPIED]  {src_folder}/index.html")
        print(f"       →  {dest_folder}/market/index.html")

        # Build and apply meta tags
        title, desc, canonical = get_meta(dest_folder, display)

        try:
            changed = update_html(dest_file, title, desc, canonical)
            if changed:
                updated += 1
                print(f"[UPDATED] Meta tags:")
                print(f"          Title     → {title}")
                print(f"          Canonical → {canonical}")
                print(f"          Desc      → {desc[:75]}...")
            else:
                skipped += 1
                print(f"[SKIPPED] Tags already correct")
        except Exception as e:
            errors.append(dest_file)
            print(f"[ERROR]   {dest_file} — {e}")

    print(f"\n{'='*65}")
    print(f"  Files copied   : {copied}")
    print(f"  Files updated  : {updated}")
    print(f"  Files skipped  : {skipped}")
    print(f"  Errors         : {len(errors)}")
    print(f"{'='*65}")

    if errors:
        print("\nFailed files:")
        for e in errors:
            print(f"  {e}")

    print("\nFinal structure (per country):")
    print("  multicultural-marketing-company-in-{country}/")
    print("      ├── index.html          ← homepage (untouched) ✅")
    print("      └── market/")
    print("              └── index.html  ← market page (copied + updated) ✅")


if __name__ == "__main__":
    main()


    aaaaaaaaaaaaaaaa