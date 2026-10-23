param([ValidateSet('app','prepare','documents','benchmark','doctor','test')][string]$Task='app')
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskPython=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) { throw 'Create .venv and install the project first; see README.md.' }
$taskTemp=Join-Path $PSScriptRoot '.tmp'
New-Item -ItemType Directory -Path $taskTemp -Force | Out-Null
$env:TEMP=$taskTemp
$env:TMP=$taskTemp
if ($Task -eq 'app') { & $taskPython -m streamlit run app.py --server.address localhost }
elseif ($Task -eq 'test') { & $taskPython -m pytest }
else { & $taskPython -m aave_analyst.cli $Task }
exit $LASTEXITCODE
