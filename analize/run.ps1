# run.ps1
# Helper: tymczasowo ustawia ExecutionPolicy Bypass dla tej sesji i uruchamia CLI projektu.
# Uruchom z katalogu projektu PowerShell:
#   powershell -ExecutionPolicy Bypass -File .\analize\run.ps1

try {
    $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
} catch {
    $scriptRoot = $PSScriptRoot
}

# Ścieżka do interpretera w venv (zakładamy, że .venv jest w katalogu głównym projektu)
$python = Join-Path $scriptRoot '..\.venv\Scripts\python.exe'
$cli = Join-Path $scriptRoot 'cli.py'

Write-Host "Using python: $python"
Write-Host "Starting CLI: $cli"

# Ustawienie tymczasowe dla tej sesji
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Uruchom CLI
& $python $cli

Write-Host "CLI finished"
