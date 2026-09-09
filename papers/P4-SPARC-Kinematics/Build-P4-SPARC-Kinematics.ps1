# Build P4 PDF directly to its canonical content-title + versioned name.
# Prerequisite: conda activate itsm_env (if the local Python/TeX environment requires it)
#
# Usage:
#   cd papers\P4-SPARC-Kinematics
#   .\Build-P4-SPARC-Kinematics.ps1

$ErrorActionPreference = "Stop"
$PaperDir = $PSScriptRoot

$Author = "Boyd"
$Year = "2026"
$ContentSlug = "SPARC_Galactic_Kinematics_AQUAL_Picard_Solutions"
$VersionFile = Join-Path $PaperDir "VERSION"
if (-not (Test-Path $VersionFile)) {
    throw "Missing VERSION file in $PaperDir"
}
$Version = (Get-Content -Raw $VersionFile).Trim()
if (-not $Version) { throw "VERSION file is empty" }
$JobStem = "${Author}_${Year}_${ContentSlug}_v${Version}"
$PdfName = "${JobStem}.pdf"
$SidecarName = "${PdfName}.sha256"
$SourceName = "main.tex"

foreach ($cmd in @("python", "pdflatex", "bibtex")) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        throw "$cmd not found on PATH."
    }
}

Push-Location $PaperDir
try {
    Write-Host "Generating RAR figure ..."
    & python generate_rar_figure.py | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "generate_rar_figure.py failed" }

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

    Write-Host "OK canonical PDF: $($pdf.FullName) ($([math]::Round($pdf.Length/1KB,1)) KB)"
    Write-Host "OK PDF sidecar: $(Join-Path $PaperDir $SidecarName)"
    Write-Host "VERSION: $Version"
}
finally {
    Pop-Location
}
