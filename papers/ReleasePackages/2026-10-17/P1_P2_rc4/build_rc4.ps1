param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('P1', 'P2')]
    [string]$Paper,
    [switch]$Portable,
    [switch]$UseBundledTectonic,
    [string]$TectonicPath = 'C:/Program Files/WindowsApps/OpenAI.Codex_26.1007.9446.0_x64__2p2nqsd0c76g0/app/resources/tectonic/tectonic.exe'
)

# Local review build only. No package installation, shell escape, or release.
$ErrorActionPreference = 'Stop'
$rc4Repo = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$rc4Names = @{
    P1 = @('P1-Scale-Matching-Reconstruction', 'Boyd_2026_Present-Epoch_Scale_Matching_Cobs_Hygiene_v0.2.0-rc4')
    P2 = @('P2-Rectangular-T3-Casimir', 'Boyd_2026_Anisotropic_Casimir_Rectangular_T3_Instantaneous-Closure-Control_v0.2.0-rc4')
}
$rc4PaperDir = Join-Path $rc4Repo ('papers/' + $rc4Names[$Paper][0])
$rc4Stem = $rc4Names[$Paper][1]
if ($Portable) {
    $rc4PaperDir = Join-Path $PSScriptRoot ('portable/' + $Paper)
}
if ((Get-Content -LiteralPath (Join-Path $rc4PaperDir 'VERSION') -Raw).Trim() -ne '0.2.0-rc4') {
    throw 'Refusing to build a different version'
}
Push-Location $rc4PaperDir
try {
    if ($UseBundledTectonic) {
        $rc4BuildKind = 'final'
        if ($Portable) { $rc4BuildKind = 'portable_check' }
        $rc4OutDir = Join-Path $rc4Repo ('.local/p1-p2-rc4/' + $rc4BuildKind + '/' + $Paper)
        New-Item -ItemType Directory -Path $rc4OutDir -Force | Out-Null
        & $TectonicPath -X compile --untrusted --keep-logs --keep-intermediates --print --outdir $rc4OutDir main.tex
        if ($LASTEXITCODE -ne 0) { throw 'Bundled Tectonic build failed' }
        Write-Output "LOCAL_REVIEW_BUILD_COMPLETE $Paper portable=$Portable compiler=Tectonic"
        return
    }
    $rc4PdfLatex = (Get-Command pdflatex.exe -ErrorAction Stop).Source
    $rc4Bibtex = (Get-Command bibtex.exe -ErrorAction Stop).Source
    & $rc4PdfLatex --disable-installer -no-shell-escape -halt-on-error -interaction=nonstopmode "-jobname=$rc4Stem" main.tex
    if ($LASTEXITCODE -ne 0) { throw 'First pdfLaTeX pass failed' }
    & $rc4Bibtex --disable-installer $rc4Stem
    if ($LASTEXITCODE -ne 0) { throw 'BibTeX failed' }
    foreach ($rc4Pass in @(2, 3)) {
        & $rc4PdfLatex --disable-installer -no-shell-escape -halt-on-error -interaction=nonstopmode "-jobname=$rc4Stem" main.tex
        if ($LASTEXITCODE -ne 0) { throw "pdfLaTeX pass $rc4Pass failed" }
    }
    Write-Output "LOCAL_REVIEW_BUILD_COMPLETE $Paper portable=$Portable"
}
finally { Pop-Location }
