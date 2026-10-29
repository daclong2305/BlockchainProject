param([int]$Port=8081, [int]$GpuLayers=99)
$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSScriptRoot
$taskServer=Join-Path $taskRoot '.tools\llama-b11962\llama-server.exe'
$taskModel=Join-Path $taskRoot 'models\qwen-vitext2sql-3b\model-q4_k_m.gguf'
if (-not (Test-Path -LiteralPath $taskServer) -or -not (Test-Path -LiteralPath $taskModel)) {
    throw 'Run .\.venv\Scripts\python.exe scripts/setup_local_qwen.py first.'
}
& $taskServer -m $taskModel --alias 'zhenlong54/qwen-vitext2sql-3b-GGUF' --host 127.0.0.1 --port $Port -c 8192 -np 1 -ngl $GpuLayers -b 512 -ub 128 -t 6 --jinja
exit $LASTEXITCODE
