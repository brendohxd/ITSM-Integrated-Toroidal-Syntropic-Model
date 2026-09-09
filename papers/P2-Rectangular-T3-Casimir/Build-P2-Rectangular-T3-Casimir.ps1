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
$ContentSlug = "Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control"
$VersionFile = Join-Path $PaperDir "VERSION"
if (-not (Test-Path $VersionFile)) {
    throw "Missing VERSION file in $PaperDir (expected e.g. 0.1.0-draft)"
}
$Version = (Get-Content -Raw $VersionFile).Trim()
if (-not $Version) { throw "VERSION file is empty" }
$JobStem = "${Author}_${Year}_${ContentSlug}_v${Version}"
$PdfName = "${JobStem}.pdf"
$SidecarName = "${PdfName}.sha256"
$SourceName = "main.tex"

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
    & pdflatex -interaction=nonstopmode "-jobname=$JobStem" $SourceName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 1 failed. See $JobStem.log" }

    Write-Host "bibtex ..."
    & bibtex $JobStem | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "bibtex failed. See $JobStem.blg" }

    Write-Host "pdflatex pass 2 ..."
    & pdflatex -interaction=nonstopmode "-jobname=$JobStem" $SourceName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 2 failed. See $JobStem.log" }

    Write-Host "pdflatex pass 3 ..."
    & pdflatex -interaction=nonstopmode "-jobname=$JobStem" $SourceName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 3 failed. See $JobStem.log" }

    $named = Join-Path $PaperDir $PdfName
    $pdf = Get-Item $named
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $pdf.FullName).Hash.ToLowerInvariant()
    "$hash  $PdfName" | Set-Content -LiteralPath (Join-Path $PaperDir $SidecarName) -Encoding ascii

    # Keep generated bibliography byproducts out of the paper directory.
    @("$JobStem.bbl", "${JobStem}Notes.bib") | ForEach-Object {
        $buildProduct = Join-Path $PaperDir $_
        if (Test-Path $buildProduct) { Remove-Item -Force $buildProduct }
    }

    # Remove the generic deliverable name after the canonical output is verified.
    @("main.pdf", "main.pdf.sha256") | ForEach-Object {
        $legacy = Join-Path $PaperDir $_
        if (Test-Path $legacy) { Remove-Item -Force $legacy }
    }

    @(
        "Boyd_P2_Anisotropic_Casimir_Rectangular_T3.pdf"
    ) | ForEach-Object {
        $old = Join-Path $PaperDir $_
        if (Test-Path $old) { Remove-Item -Force $old }
    }

    Write-Host "OK canonical PDF: $($pdf.FullName) ($([math]::Round($pdf.Length/1KB,1)) KB)"
    Write-Host "OK PDF sidecar: $(Join-Path $PaperDir $SidecarName)"
    Write-Host "VERSION: $Version"
}
finally {
    Pop-Location
}
