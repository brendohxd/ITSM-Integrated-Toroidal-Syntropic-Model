[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^\d+\.\d+-alpha\.\d+$')]
    [string]$Version,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$Label
)

$ErrorActionPreference = 'Stop'

$manuscriptRoot = $PSScriptRoot
$workingSource = Join-Path $manuscriptRoot 'ITSM_Core_working.tex'
$sectionsSource = Join-Path $manuscriptRoot 'sections'
$releaseRoot = Join-Path $manuscriptRoot 'releases'
$releaseDirectory = Join-Path $releaseRoot "v$Version"
$releaseSource = Join-Path $releaseDirectory "ITSM_Core_v$Version.tex"
$releaseDate = Get-Date -Format 'dd MMMM yyyy'

if (-not (Test-Path -LiteralPath $workingSource -PathType Leaf)) {
    throw "Working source is missing: $workingSource"
}

if (-not (Test-Path -LiteralPath $sectionsSource -PathType Container)) {
    throw "Working sections are missing: $sectionsSource"
}

if (Test-Path -LiteralPath $releaseDirectory) {
    throw "Release already exists and will not be overwritten: $releaseDirectory"
}

$workingText = Get-Content -LiteralPath $workingSource -Raw
$datePattern = '\\date\{Working draft \(after [^)]+\) --- \\today\}'
$releaseDateLine = "\date{Version $Version --- $Label --- $releaseDate}"
$releaseText = [regex]::Replace($workingText, $datePattern, $releaseDateLine)

if ($releaseText -eq $workingText) {
    throw 'Could not find the expected working-draft date marker.'
}

New-Item -ItemType Directory -Path $releaseDirectory | Out-Null
New-Item -ItemType Directory -Path (Join-Path $releaseDirectory 'sections') |
    Out-Null

Set-Content -LiteralPath $releaseSource -Value $releaseText -Encoding utf8
Copy-Item -Path (Join-Path $sectionsSource '*.tex') `
    -Destination (Join-Path $releaseDirectory 'sections')

$compiler = Get-Command 'pdflatex' -ErrorAction SilentlyContinue
if ($null -eq $compiler) {
    Write-Warning 'pdflatex was not found. Source snapshot created without PDF.'
    Write-Output $releaseDirectory
    exit 0
}

Push-Location $releaseDirectory
try {
    & $compiler.Source -interaction=nonstopmode -halt-on-error `
        (Split-Path -Leaf $releaseSource)
    if ($LASTEXITCODE -ne 0) {
        throw "First pdflatex pass failed with exit code $LASTEXITCODE"
    }

    & $compiler.Source -interaction=nonstopmode -halt-on-error `
        (Split-Path -Leaf $releaseSource)
    if ($LASTEXITCODE -ne 0) {
        throw "Second pdflatex pass failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

$releaseArtifacts = Get-ChildItem -LiteralPath $releaseDirectory -Recurse -File |
    Where-Object { $_.Extension -in '.tex', '.pdf' } |
    Sort-Object FullName
$checksumLines = foreach ($artifact in $releaseArtifacts) {
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $artifact.FullName).Hash
    $relative = $artifact.FullName.Substring($releaseDirectory.Length + 1).
        Replace('\', '/')
    "$hash  $relative"
}
$checksumPath = Join-Path $releaseDirectory 'SHA256SUMS.txt'
Set-Content -LiteralPath $checksumPath -Value $checksumLines -Encoding ascii

Write-Output "Created immutable manuscript release: $releaseDirectory"
Write-Output 'Review the PDF, add RELEASE_NOTES.md, update CHANGELOG.md and VERSION,'
Write-Output 'then commit the complete release together.'
