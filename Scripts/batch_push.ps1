$files = Get-ChildItem -Path "Assets\SPARC_Batch_Outputs\" -File
$batchSize = 30
$batchCount = [math]::Ceiling($files.Count / $batchSize)

for ($i = 0; $i -lt $batchCount; $i++) {
    $batch = $files | Select-Object -Skip ($i * $batchSize) -First $batchSize
    Write-Host "Processing batch $($i + 1) of $batchCount..."
    foreach ($file in $batch) {
        git add "Assets\SPARC_Batch_Outputs\$($file.Name)"
    }
    git commit -m "chore: Upload SPARC outputs batch $($i + 1)/$batchCount"
    git push
}
Write-Host "All batches pushed successfully."
