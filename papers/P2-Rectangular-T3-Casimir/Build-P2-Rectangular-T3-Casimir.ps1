# Build P2 PDF with content-title + versioned share name.
# Prerequisite: conda activate itsm_env
#
# Usage:
#   cd papers\P2-Rectangular-T3-Casimir
#   .\Build-P2-Rectangular-T3-Casimir.ps1

$ErrorActionPreference = "Stop"
$PaperDir = $PSScriptRoot

$Author = "Boyd"
$Year = "2026"
$ContentSlug = "Anisotropic_Casimir_Rectangular_T3_Free-Field_Backreaction"
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

    @(
        "Boyd_P2_Anisotropic_Casimir_Rectangular_T3.pdf"
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
