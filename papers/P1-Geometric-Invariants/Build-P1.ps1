# Build Paper 1 PDF.
# Prerequisite: activate the project env once in this terminal, then leave it active:
#   conda activate itsm_env
# After that, python / scripts / any commands in this shell use itsm_env packages
# until the terminal exits. Do not re-activate per script or install ad-hoc deps.
#
# Usage (env already active):
#   cd papers\P1-Geometric-Invariants
#   .\Build-P1.ps1

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

$fig = Join-Path $RepoRoot "Assets\Figures\itsm_t3_fundamental_domain.pdf"
$figScript = Join-Path $RepoRoot "Scripts\itsm_t3_fundamental_domain.py"
if (-not (Test-Path $fig)) {
    Write-Host "Generating T^3 fundamental-domain figure with current python ..."
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
    Write-Host "OK: $($pdf.FullName) ($([math]::Round($pdf.Length/1KB,1)) KB)"
}
finally {
    Pop-Location
}
