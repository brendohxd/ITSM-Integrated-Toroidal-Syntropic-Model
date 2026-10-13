# Verify filename version tags for retained document PDFs. Read-only.
# Figures and the mutable Core working build are not retained documents.
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path

Push-Location $repoRoot
try {
    $gitPaths = @(git -c core.quotepath=false ls-files --cached --others --exclude-standard -- '*.pdf')
    if ($LASTEXITCODE -ne 0) { throw 'Could not enumerate repository PDFs with Git.' }

    # Local historical binaries are intentionally Git-ignored, but still need
    # the same version-token check when present on this machine.
    $legacyRoot = Join-Path $repoRoot 'papers\LegacyBuilds'
    $localLegacyPaths = @()
    if (Test-Path -LiteralPath $legacyRoot -PathType Container) {
        $localLegacyPaths = @(Get-ChildItem -LiteralPath $legacyRoot -Recurse -File -Filter '*.pdf' |
            ForEach-Object { $_.FullName.Substring($repoRoot.Length + 1).Replace('\', '/') })
    }

    $checked = 0
    $violations = @()
    foreach ($relativePath in @($gitPaths + $localLegacyPaths | Sort-Object -Unique)) {
        if ($relativePath -notmatch '^(Manuscript|papers)/') { continue }
        if ($relativePath -match '(^|/)figures/') { continue }
        if ($relativePath -eq 'Manuscript/CoreRecovery/ITSM_Core_working.pdf') { continue }
        $absolutePath = Join-Path $repoRoot $relativePath
        if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) { continue }
        $checked++
        if ($relativePath -notmatch '(?i)_v[0-9]+\.[0-9]+(?:\.[0-9]+)?(?:[-.][A-Za-z0-9]+)*\.pdf$') {
            $violations += $relativePath
        }
    }
    if ($checked -eq 0) { throw 'No retained PDF files were inspected.' }
    Write-Output "retained_document_pdfs_checked=$checked"
    if ($violations.Count -gt 0) {
        $violations | ForEach-Object { Write-Error "Unversioned retained PDF: $_" }
        throw "Retained PDF naming check failed: $($violations.Count) unversioned file(s)."
    }
    Write-Output 'versioned_filename_check=PASS'
}
finally {
    Pop-Location
}
