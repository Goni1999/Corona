# Define the path to the PDF
$pdfPath = "$pwd\adobe.pdf"

# Check if the PDF file exists
if (Test-Path $pdfPath) {
    # Open the PDF file
    Write-Host "Opening PDF file..."
    Start-Process -FilePath $pdfPath
} else {
    Write-Host "PDF file not found."
}

Write-Host "Payload executed and PDF opened."
