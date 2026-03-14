# ============================================================
# Billiontags - Fix Empty Files & Move Content HTML Files
# Root: D:\billiontags.com
# Logic:
#   1. Delete empty files inside subfolders
#   2. Move real content files from country root into subfolders
# ============================================================

$rootPath = "D:\billiontags.com"

$countries = @(
    "australia",
    "canada",
    "malaysia",
    "newzealand",
    "singapore",
    "southafrica",
    "uae",
    "uk",
    "usa"
)

$structure = @{
    "arab-marketing-agency-in-COUNTRY"                       = "general-16.html"
    "black-and-african-american-marketing-agency-in-COUNTRY" = "general-23.html"
    "chinese-marketing-agency-in-COUNTRY"                    = "general-17.html"
    "community-marketing-strategist-in-COUNTRY"              = "general-22.html"
    "cricket-advertising-in-COUNTRY"                         = "general-9.html"
    "cross-cultural-marketing-agency-in-COUNTRY"             = "general-1.html"
    "culture-marketing-agency-in-COUNTRY"                    = "general-3.html"
    "dei-marketing-agency-in-COUNTRY"                        = "general-6.html"
    "diaspora-marketing-agency-in-COUNTRY"                   = "general-8.html"
    "diversity-marketing-agency-in-COUNTRY"                  = "general-5.html"
    "ethnic-marketing-agency-in-COUNTRY"                     = "general-11.html"
    "ethnic-strategy-agency-in-COUNTRY"                      = "general-10.html"
    "event-marketing-agency-in-COUNTRY"                      = "general-4.html"
    "filipino-marketing-agency-in-COUNTRY"                   = "general-19.html"
    "hispanic-marketing-agency-in-COUNTRY"                   = "general-13.html"
    "immigrants-marketing-strategist-in-COUNTRY"             = "general-7.html"
    "latino-marketing-agency-in-COUNTRY"                     = "general-18.html"
    "lgbtq-marketing-agency-in-COUNTRY"                      = "general-20.html"
    "multilingual-marketing-services-agency-in-COUNTRY"      = "general-14.html"
    "neocultural-marketing-company-in-COUNTRY"               = "general-2.html"
    "newcomer-marketing-company-in-COUNTRY"                  = "general-15.html"
    "nri-marketing-agency-in-COUNTRY"                        = "general-21.html"
    "south-asian-marketing-agency-in-COUNTRY"                = "general-12.html"
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Billiontags - Fix Empty Files & Move Real Content" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$totalMoved   = 0
$totalSkipped = 0
$totalMissing = 0
$totalDeleted = 0

foreach ($country in $countries) {

    $countryFolder = "$rootPath\$country-keyword"
    Write-Host "Processing: $country-keyword" -ForegroundColor Yellow

    foreach ($folderTemplate in $structure.Keys) {

        $folderName    = $folderTemplate -replace "COUNTRY", $country
        $htmlFile      = $structure[$folderTemplate]

        $subfolderPath = "$countryFolder\$folderName"
        $sourcePath    = "$countryFolder\$htmlFile"     # real file at root level
        $destPath      = "$subfolderPath\$htmlFile"     # target inside subfolder

        # Create subfolder if missing
        if (-not (Test-Path $subfolderPath)) {
            New-Item -ItemType Directory -Path $subfolderPath -Force | Out-Null
        }

        # Step 1: If destination file exists but is EMPTY, delete it
        if (Test-Path $destPath) {
            $fileSize = (Get-Item $destPath).Length
            if ($fileSize -eq 0) {
                Remove-Item -Path $destPath -Force
                Write-Host "  [DELETED]  Empty file removed: $folderName\$htmlFile" -ForegroundColor DarkYellow
                $totalDeleted++
            } else {
                # File exists and has content - skip
                Write-Host "  [SKIP]     Already has content: $folderName\$htmlFile" -ForegroundColor Gray
                $totalSkipped++
                continue
            }
        }

        # Step 2: Move real content file from root into subfolder
        if (Test-Path $sourcePath) {
            $fileSize = (Get-Item $sourcePath).Length
            if ($fileSize -gt 0) {
                Move-Item -Path $sourcePath -Destination $destPath -Force
                Write-Host "  [MOVED]    $htmlFile => $folderName\$htmlFile ($fileSize bytes)" -ForegroundColor Green
                $totalMoved++
            } else {
                Write-Host "  [WARNING]  Source file is also empty: $htmlFile" -ForegroundColor Red
                $totalMissing++
            }
        } else {
            Write-Host "  [MISSING]  Not found at root: $htmlFile" -ForegroundColor Red
            $totalMissing++
        }

    }

    Write-Host ""

}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Done! Summary:" -ForegroundColor Cyan
Write-Host "  Empty files deleted : $totalDeleted" -ForegroundColor DarkYellow
Write-Host "  Files moved         : $totalMoved"   -ForegroundColor Green
Write-Host "  Files skipped       : $totalSkipped" -ForegroundColor Gray
Write-Host "  Files missing       : $totalMissing" -ForegroundColor Red
Write-Host "============================================================" -ForegroundColor Cyan
