# Build the versioned covariant entropy-accounting manuscript.
# Prerequisite: conda activate itsm_env

$ErrorActionPreference = "Stop"
$PaperDir = $PSScriptRoot
$Version = (Get-Content -Raw -LiteralPath (Join-Path $PaperDir "VERSION")).Trim()
if (-not $Version) { throw "VERSION file is empty" }

$SourceName = "ITSM_Covariant_Entropy_Accounting_v0.7.1-conditional-draft.tex"
$JobStem = "Boyd_2026_Covariant_Entropy_Accounting_Interacting_Sectors_v$Version"
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
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $pdf.FullName).Hash.ToLowerInvariant()
    "$hash  $PdfName" | Set-Content -LiteralPath (Join-Path $PaperDir $SidecarName) -Encoding ascii

    @("$JobStem.bbl", "${JobStem}Notes.bib") | ForEach-Object {
        $generated = Join-Path $PaperDir $_
        if (Test-Path -LiteralPath $generated) { Remove-Item -LiteralPath $generated -Force }
    }

    Write-Host "OK canonical PDF: $($pdf.FullName)"
    Write-Host "OK PDF sidecar: $(Join-Path $PaperDir $SidecarName)"
}
finally {
    Pop-Location
}
