$ErrorActionPreference = "Stop"
$version = if ($env:FIERRO_AGENTS_VERSION) { $env:FIERRO_AGENTS_VERSION } else { "latest" }
$repo = if ($env:FIERRO_AGENTS_REPOSITORY) { $env:FIERRO_AGENTS_REPOSITORY } else { "radiocutfm/harness" }
$base = if ($version -eq "latest") { "https://github.com/$repo/releases/latest/download" } else { "https://github.com/$repo/releases/download/$version" }
$scriptPath = Join-Path $env:TEMP "fierro-harness-install.py"
$archivePath = Join-Path $env:TEMP "fierro-harness-skills.tar.gz"
Invoke-WebRequest "$base/install.py" -OutFile $scriptPath
Invoke-WebRequest "$base/skills.tar.gz" -OutFile $archivePath
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  irm https://astral.sh/uv/install.ps1 | iex
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw "No se pudo instalar uv." }
uv run $scriptPath --skills-archive $archivePath
