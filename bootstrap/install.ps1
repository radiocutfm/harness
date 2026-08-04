$ErrorActionPreference = "Stop"
$version = if ($env:FIERRO_AGENTS_VERSION) { $env:FIERRO_AGENTS_VERSION } else { "latest" }
$repo = if ($env:FIERRO_AGENTS_REPOSITORY) { $env:FIERRO_AGENTS_REPOSITORY } else { "radiocutfm/harness" }
$base = if ($version -eq "latest") { "https://github.com/$repo/releases/latest/download" } else { "https://github.com/$repo/releases/download/$version" }
$wheelName = if ($version -eq "latest") { "fierro_harness-latest.whl" } else { "fierro_harness-$($version.TrimStart('v'))-py3-none-any.whl" }
$wheelPath = Join-Path $env:TEMP $wheelName
Invoke-WebRequest "$base/$wheelName" -OutFile $wheelPath
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  irm https://astral.sh/uv/install.ps1 | iex
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw "No se pudo instalar uv." }
uv run --with $wheelPath fierro-harness install
