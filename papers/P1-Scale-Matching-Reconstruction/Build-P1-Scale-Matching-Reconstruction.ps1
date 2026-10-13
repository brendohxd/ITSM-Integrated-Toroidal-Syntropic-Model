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
$JobStem = "${Author}_${Year}_${ContentSlug}_v${Version}"
$PdfName = "${JobStem}.pdf"
$SidecarName = "${PdfName}.sha256"
$SourceName = "main.tex"

# A generic or obsolete PDF may be a distinct historical build. Never delete
# it as a side effect of compiling the current versioned artifact.
@("main.pdf", "main.pdf.sha256", "Boyd_P1_Present-Epoch_Scale_Matching_Cobs_Hygiene.pdf") | ForEach-Object {
    $legacy = Join-Path $PaperDir $_
    if (Test-Path -LiteralPath $legacy) {
        throw "Unversioned PDF artifact found: $legacy. Hash and archive it before building."
    }
}

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
    $stream = [System.IO.File]::OpenRead($pdf.FullName)
    try {
        $sha256 = [System.Security.Cryptography.SHA256]::Create()
        try {
            $hash = ([System.BitConverter]::ToString($sha256.ComputeHash($stream))).Replace("-", "").ToLowerInvariant()
        }
        finally {
            $sha256.Dispose()
        }
    }
    finally {
        $stream.Dispose()
    }
    "$hash  $PdfName" | Set-Content -LiteralPath (Join-Path $PaperDir $SidecarName) -Encoding ascii

    # Keep generated bibliography byproducts out of the paper directory.
    @("$JobStem.bbl", "${JobStem}Notes.bib") | ForEach-Object {
        $buildProduct = Join-Path $PaperDir $_
        if (Test-Path $buildProduct) { Remove-Item -Force $buildProduct }
    }

    Write-Host "OK canonical PDF: $($pdf.FullName) ($([math]::Round($pdf.Length/1KB,1)) KB)"
    Write-Host "OK PDF sidecar: $(Join-Path $PaperDir $SidecarName)"
    Write-Host "VERSION: $Version"
}
finally {
    Pop-Location
}
