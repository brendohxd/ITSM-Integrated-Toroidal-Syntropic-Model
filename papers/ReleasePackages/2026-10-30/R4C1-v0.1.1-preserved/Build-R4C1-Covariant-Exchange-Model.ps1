# Build the versioned R4C1 conditional theory paper.
# Prerequisite: conda activate itsm_env

$ErrorActionPreference = "Stop"
$PaperDir = $PSScriptRoot
$Version = (Get-Content -Raw -LiteralPath (Join-Path $PaperDir "VERSION")).Trim()
if (-not $Version) { throw "VERSION file is empty" }

$SourceName = "main.tex"
$JobStem = "Boyd_2026_Covariant_Finite-Density_Exchange_Model_v$Version"
$PdfName = "$JobStem.pdf"
$SidecarName = "$PdfName.sha256"

foreach ($cmd in @("pdflatex", "bibtex")) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        throw "$cmd not found on PATH (system TeX required)."
    }
}

Push-Location $PaperDir
try {
    & pdflatex -interaction=nonstopmode "-jobname=$JobStem" $SourceName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 1 failed. See $JobStem.log" }

    & bibtex $JobStem | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "bibtex failed. See $JobStem.blg" }

    & pdflatex -interaction=nonstopmode "-jobname=$JobStem" $SourceName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 2 failed. See $JobStem.log" }

    & pdflatex -interaction=nonstopmode "-jobname=$JobStem" $SourceName | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "pdflatex pass 3 failed. See $JobStem.log" }

    $pdf = Get-Item -LiteralPath (Join-Path $PaperDir $PdfName)
    $sha256 = [Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [IO.File]::ReadAllBytes($pdf.FullName)
        $hash = ([BitConverter]::ToString($sha256.ComputeHash($bytes))).Replace('-', '').ToLowerInvariant()
    }
    finally {
        $sha256.Dispose()
    }
    "$hash  $PdfName" | Set-Content -LiteralPath (Join-Path $PaperDir $SidecarName) -Encoding ascii

    @($JobStem + ".bbl", $JobStem + "Notes.bib") | ForEach-Object {
        $generated = Join-Path $PaperDir $_
        if (Test-Path -LiteralPath $generated) { Remove-Item -LiteralPath $generated -Force }
    }

    Write-Host "OK canonical PDF: $($pdf.FullName)"
    Write-Host "OK PDF sidecar: $(Join-Path $PaperDir $SidecarName)"
}
finally {
    Pop-Location
}
