# Build Paper 2 PDF.
# Prerequisite: activate the project env once in this terminal:
#   conda activate itsm_env
#
# Usage:
#   cd papers\P2-Rectangular-T3-Casimir
#   .\Build-P2-Rectangular-T3-Casimir.ps1

$ErrorActionPreference = "Stop"
$PaperDir = $PSScriptRoot
$RepoRoot = Resolve-Path (Join-Path $PaperDir "..\..")

if ($env:CONDA_DEFAULT_ENV -and $env:CONDA_DEFAULT_ENV -ne "itsm_env") {
    Write-Warning "Current conda env is '$($env:CONDA_DEFAULT_ENV)', not itsm_env. Activate itsm_env in this terminal first."
}
elseif (-not $env:CONDA_DEFAULT_ENV) {
    Write-Warning "No conda env detected on CONDA_DEFAULT_ENV. If builds fail, run: conda activate itsm_env"
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
    # Canonical paper filename (matches folder + title identity)
    $named = Join-Path $PaperDir "Boyd_P2_Anisotropic_Casimir_Rectangular_T3.pdf"
    Copy-Item -Force $pdf.FullName $named
    Write-Host "OK: $($pdf.FullName) ($([math]::Round($pdf.Length/1KB,1)) KB)"
    Write-Host "OK: $named"
}
finally {
    Pop-Location
}
