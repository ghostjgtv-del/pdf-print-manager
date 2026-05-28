<#
.SYNOPSIS
    Script to print multiple PDF files from a folder
.DESCRIPTION
    Prints all PDF files found in a specified folder
    with error handling and activity logging
.AUTHOR
    Eng. Justo Torres - Lagudis Fresh Food Group
.DATE
    February 2026
#>
param(
    [string]$PDFFolder = "C:\Test",
    [int]$WaitTimeSeconds = 3,
    [switch]$ShowLog = $true
)

$ErrorActionPreference = "Continue"

function Write-Log {
    param([string]$Message, [string]$Type = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch($Type) {
        "ERROR"   { "Red" }
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        default   { "White" }
    }
    if($ShowLog) {
        Write-Host "[$timestamp] [$Type] $Message" -ForegroundColor $color
    }
}

function Test-FolderExists {
    param([string]$Path)
    if(-not (Test-Path -Path $Path)) {
        Write-Log "ERROR: The folder does not exist: $Path" "ERROR"
        Write-Host "`nPress any key to exit..." -ForegroundColor Red
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

function Get-PDFsInFolder {
    param([string]$Path)
    try {
        $files = Get-ChildItem -Path $Path -Filter *.pdf -ErrorAction Stop | Sort-Object Name
        return $files
    }
    catch {
        Write-Log "ERROR reading files: $($_.Exception.Message)" "ERROR"
        return $null
    }
}

function Get-PrinterSelection {
    $printers = Get-Printer | Where-Object {$_.Type -eq "Local" -or $_.Type -eq "Connection"} | Sort-Object Name
    
    if($printers.Count -eq 0) {
        Write-Log "No printers found on this computer" "ERROR"
        Write-Host "`nPress any key to exit..." -ForegroundColor Red
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
    
    Write-Host "`nAvailable Printers:" -ForegroundColor Yellow
    Write-Host "  0. Use Default Printer" -ForegroundColor Cyan
    
    for($i = 0; $i -lt $printers.Count; $i++) {
        $defaultMark = ""
        if($printers[$i].Default) {
            $defaultMark = " (Default)"
        }
        Write-Host "  $($i+1). $($printers[$i].Name)$defaultMark" -ForegroundColor Gray
    }
    
    Write-Host "`nSelect printer number (0 for default): " -ForegroundColor Yellow -NoNewline
    $selection = Read-Host
    
    if($selection -eq "0" -or $selection -eq "") {
        Write-Log "Using default printer" "SUCCESS"
        return $null
    }
    
    $index = [int]$selection - 1
    if($index -ge 0 -and $index -lt $printers.Count) {
        $selectedPrinter = $printers[$index].Name
        Write-Log "Selected printer: $selectedPrinter" "SUCCESS"
        return $selectedPrinter
    }
    else {
        Write-Log "Invalid selection, using default printer" "WARNING"
        return $null
    }
}

function Print-PDFFile {
    param(
        [string]$FilePath,
        [string]$PrinterName = $null
    )
    
    if($null -eq $PrinterName -or $PrinterName -eq "") {
        Start-Process -FilePath $FilePath -Verb Print -ErrorAction Stop
    }
    else {
        $pdfApp = (Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.pdf\UserChoice" -ErrorAction SilentlyContinue).ProgId
        
        if($pdfApp -like "*Edge*" -or $pdfApp -like "*Chrome*") {
            $tempBat = [System.IO.Path]::GetTempFileName() + ".bat"
            $batContent = "@echo off`nrundll32.exe `"C:\Windows\System32\mshtml.dll`",PrintHTML `"$FilePath`""
            $batContent | Out-File -FilePath $tempBat -Encoding ASCII
            Start-Process -FilePath $tempBat -Wait -WindowStyle Hidden
            Remove-Item $tempBat -Force
        }
        else {
            Start-Process -FilePath $FilePath -Verb Print -ErrorAction Stop
        }
    }
}

try {
    Clear-Host
    Write-Host "========================================"
    Write-Host "  MASS PDF PRINTING"
    Write-Host "  Lagudis Fresh Food Group"
    Write-Host "  Autor: Eng. Justo Torres"
    Write-Host "========================================"
    Write-Host ""
    
    Test-FolderExists -Path $PDFFolder
    Write-Log "Searching for PDF files in: $PDFFolder"
    
    $pdfFiles = Get-PDFsInFolder -Path $PDFFolder
    
    if($null -eq $pdfFiles -or $pdfFiles.Count -eq 0) {
        Write-Log "No PDF files found in folder" "WARNING"
        Write-Host "`nPress any key to exit..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 0
    }
    
    Write-Log "Files found: $($pdfFiles.Count)" "SUCCESS"
    Write-Host "`nFiles to print:"
    for($i = 0; $i -lt $pdfFiles.Count; $i++) {
        Write-Host "  $($i+1). $($pdfFiles[$i].Name)"
    }
    
    $selectedPrinter = Get-PrinterSelection
    
    Write-Host "`nDo you want to continue with printing? (Y/N): " -ForegroundColor Yellow -NoNewline
    $confirmation = Read-Host
    
    if($confirmation -ne "Y" -and $confirmation -ne "y") {
        Write-Log "Cancelled by user" "WARNING"
        exit 0
    }
    
    Write-Host ""
    Write-Log "Starting print process..." "SUCCESS"
    Write-Host ""
    
    $successful = 0
    $failed = 0
    $errorLog = @()
    
    foreach($file in $pdfFiles) {
        try {
            Write-Log "Printing: $($file.Name)"
            Print-PDFFile -FilePath $file.FullName -PrinterName $selectedPrinter
            $successful++
            Write-Log "Sent to printer" "SUCCESS"
            Start-Sleep -Seconds $WaitTimeSeconds
        }
        catch {
            $failed++
            $errorMessage = "Error: $($_.Exception.Message)"
            Write-Log $errorMessage "ERROR"
            $errorLog += "$($file.Name): $($_.Exception.Message)"
        }
    }
    
    Write-Host "`n========================================"
    Write-Host "  PRINTING SUMMARY"
    Write-Host "========================================"
    Write-Host "Total files: $($pdfFiles.Count)"
    Write-Host "Successful: $successful"
    Write-Host "Failed: $failed"
    Write-Host "========================================"
    
    if($errorLog.Count -gt 0) {
        Write-Host "`nERRORS DETECTED:"
        foreach($error in $errorLog) {
            Write-Host "  - $error"
        }
    }
    
    $logFileName = "PrintLog_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
    $logFilePath = Join-Path -Path $PDFFolder -ChildPath $logFileName
    
    $logContent = "========================================`n"
    $logContent += "PRINT LOG - Lagudis Fresh Food Group`n"
    $logContent += "========================================`n"
    $logContent += "Author: Eng. Justo Torres`n"
    $logContent += "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
    $logContent += "Folder: $PDFFolder`n"
    if($selectedPrinter) {
        $logContent += "Printer: $selectedPrinter`n"
    } else {
        $logContent += "Printer: Default`n"
    }
    $logContent += "Total files: $($pdfFiles.Count)`n"
    $logContent += "Successful: $successful`n"
    $logContent += "Failed: $failed`n`n"
    $logContent += "PROCESSED FILES:`n"
    
    foreach($file in $pdfFiles) {
        $logContent += "  - $($file.Name)`n"
    }
    
    if($errorLog.Count -gt 0) {
        $logContent += "`nERRORS:`n"
        foreach($error in $errorLog) {
            $logContent += "  - $error`n"
        }
    }
    
    $logContent | Out-File -FilePath $logFilePath -Encoding UTF8
    Write-Host "`nLog saved at: $logFilePath"
}
catch {
    Write-Host "`nCRITICAL ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
finally {
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}