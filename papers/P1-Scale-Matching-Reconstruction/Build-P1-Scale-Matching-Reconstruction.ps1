# Build P1 PDF with content-title + versioned share name.
# Prerequisite: conda activate itsm_env
#
# Usage:
#   cd papers\P1-Scale-Matching-Reconstruction
#   .\Build-P1-Scale-Matching-Reconstruction.ps1

$ErrorActionPreference = "Stop"
$PaperDir = $PSScriptRoot
$RepoRoot = Resolve-Path (Join-Path $PaperDir "..\..")

# Content slug (stable product identity) + VERSION file (bumped by author)
$Author = "Boyd"
$Year = "2026"
$ContentSlug = "Present-Epoch_Scale_Matching_Cobs_Hygiene"
$VersionFile = Join-Path $PaperDir "VERSION"
if (-not (Test-Path $VersionFile)) {
    throw "Missing VERSION file in $PaperDir (expected e.g. 0.1.0-draft)"
}
$Version = (Get-Content -Raw $VersionFile).Trim()
if (-not $Version) { throw "VERSION file is empty" }
$ShareName = "${Author}_${Year}_${ContentSlug}_v${Version}.pdf"

if ($env:CONDA_DEFAULT_ENV -and $env:CONDA_DEFAULT_ENV -ne "itsm_env") {
    Write-Warning "Current conda env is '$($env:CONDA_DEFAULT_ENV)', not itsm_env."
}
elseif (-not $env:CONDA_DEFAULT_ENV) {
    Write-Warning "No conda env on CONDA_DEFAULT_ENV. If builds fail: conda activate itsm_env"
}
else {
    Write-Host "Using conda env: $env:CONDA_DEFAULT_ENV"
}

$fig = Join-Path $RepoRoot "Assets\Figures\itsm_t3_fundamental_domain.pdf"
$figScript = Join-Path $RepoRoot "Scripts\itsm_t3_fundamental_domain.py"
if (-not (Test-Path $fig)) {
    Write-Host "Generating T^3 fundamental-domain figure ..."
    Push-Location $RepoRoot
    try { python $figScript }
    finally { Pop-Location }
}

foreach ($cmd in @("pdflatex", "bibtex")) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        throw "$cmd not found on PATH (system TeX required)."
    }
}

Push-Location $PaperDir
try {
    Write-Host "pdflatex pass 1 ..."
    & pdflatex -interaction=nonstopmode main.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 1 failed. See main.log" }

    Write-Host "bibtex ..."
    & bibtex main | Out-Null

    Write-Host "pdflatex pass 2 ..."
    & pdflatex -interaction=nonstopmode main.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 2 failed. See main.log" }

    Write-Host "pdflatex pass 3 ..."
    & pdflatex -interaction=nonstopmode main.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 3 failed. See main.log" }

    $pdf = Get-Item (Join-Path $PaperDir "main.pdf")
    $named = Join-Path $PaperDir $ShareName
    Copy-Item -Force $pdf.FullName $named

    # Remove obsolete unversioned share names if present
    @(
        "Boyd_P1_Present-Epoch_Scale_Matching_Cobs_Hygiene.pdf"
    ) | ForEach-Object {
        $old = Join-Path $PaperDir $_
        if (Test-Path $old) { Remove-Item -Force $old }
    }

    Write-Host "OK: $($pdf.FullName) ($([math]::Round($pdf.Length/1KB,1)) KB)"
    Write-Host "OK share PDF: $named"
    Write-Host "VERSION: $Version"
}
finally {
    Pop-Location
}
