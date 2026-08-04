$ErrorActionPreference = "Stop"
$version = if ($env:FIERRO_AGENTS_VERSION) { $env:FIERRO_AGENTS_VERSION } else { "latest" }
$repo = if ($env:FIERRO_AGENTS_REPOSITORY) { $env:FIERRO_AGENTS_REPOSITORY } else { "radiocutfm/harness" }
$base = if ($version -eq "latest") { "https://github.com/$repo/releases/latest/download" } else { "https://github.com/$repo/releases/download/$version" }
if ($version -eq "latest") {
  $release = Invoke-RestMethod "https://api.github.com/repos/$repo/releases/latest"
  $asset = $release.assets | Where-Object { $_.name -like "fierro_harness-*.whl" } | Select-Object -First 1
  if (-not $asset) { throw "No se encontró el wheel del último release." }
  $wheelName = $asset.name
  $wheelUrl = $asset.browser_download_url
} else {
  $wheelName = "fierro_harness-$($version.TrimStart('v'))-py3-none-any.whl"
  $wheelUrl = "$base/$wheelName"
}
$wheelPath = Join-Path $env:TEMP $wheelName
Invoke-WebRequest $wheelUrl -OutFile $wheelPath
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
  irm https://astral.sh/uv/install.ps1 | iex
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw "No se pudo instalar uv." }
uv run --with $wheelPath fierro-harness install
