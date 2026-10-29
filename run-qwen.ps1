param([ValidateSet('app','doctor')][string]$Task='app')
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:AAVE_LLM_PROVIDER='local_qwen'
$env:QWEN_BASE_URL='http://127.0.0.1:8081'
$taskPython=Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$taskTemp=Join-Path $PSScriptRoot '.tmp'
New-Item -ItemType Directory -Path $taskTemp -Force | Out-Null
$taskHealthy=$false
try { $taskHealth=Invoke-RestMethod -Uri "$env:QWEN_BASE_URL/health" -TimeoutSec 2; $taskHealthy=($taskHealth.status -eq 'ok') } catch { }
if (-not $taskHealthy) {
    $taskListener=Get-NetTCPConnection -LocalPort 8081 -State Listen -ErrorAction SilentlyContinue
    if ($taskListener) { throw 'Port 8081 is occupied but the model server is not ready. Check .tmp/qwen-server-error.log.' }
    $taskServer=Join-Path $PSScriptRoot '.tools\llama-b11962\llama-server.exe'
    $taskModel=Join-Path $PSScriptRoot 'models\qwen-vitext2sql-3b\model-q4_k_m.gguf'
    if (-not (Test-Path -LiteralPath $taskServer) -or -not (Test-Path -LiteralPath $taskModel)) {
        throw 'Run .\.venv\Scripts\python.exe scripts/setup_local_qwen.py first.'
    }
    $taskArguments=@('-m', ('"'+$taskModel+'"'), '--alias','zhenlong54/qwen-vitext2sql-3b-GGUF','--host','127.0.0.1','--port','8081','-c','8192','-np','1','-ngl','99','-b','512','-ub','128','-t','6','--jinja')
    $taskProcess=Start-Process -FilePath $taskServer -ArgumentList $taskArguments -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $taskTemp 'qwen-server-output.log') -RedirectStandardError (Join-Path $taskTemp 'qwen-server-error.log')
    $taskProcess.Id | Set-Content (Join-Path $taskTemp 'qwen-server.pid')
    for ($taskAttempt=0; $taskAttempt -lt 60; $taskAttempt++) {
        $taskProcess.Refresh()
        if ($taskProcess.HasExited) { throw 'Qwen server exited; inspect .tmp/qwen-server-error.log.' }
        try { $taskHealth=Invoke-RestMethod -Uri "$env:QWEN_BASE_URL/health" -TimeoutSec 2; $taskHealthy=($taskHealth.status -eq 'ok') } catch { }
        if ($taskHealthy) { break }
        Start-Sleep -Seconds 1
    }
    if (-not $taskHealthy) { throw 'Qwen server is still loading; check the log and retry.' }
}
$taskModels=Invoke-RestMethod -Uri "$env:QWEN_BASE_URL/v1/models" -TimeoutSec 5
if ('zhenlong54/qwen-vitext2sql-3b-GGUF' -notin $taskModels.data.id) {
    throw 'The local server is running a different model. Check port 8081 before continuing.'
}
if ($Task -eq 'app') { & $taskPython -m streamlit run app.py --server.address localhost }
else { & $taskPython -m aave_analyst.cli doctor }
exit $LASTEXITCODE
