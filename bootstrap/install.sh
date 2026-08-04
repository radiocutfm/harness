#!/usr/bin/env sh
set -eu

version="${FIERRO_AGENTS_VERSION:-latest}"
repo="${FIERRO_AGENTS_REPOSITORY:-radiocutfm/harness}"
base="https://github.com/${repo}/releases/${version}/download"
api="https://api.github.com/repos/${repo}/releases/latest"

if [ "$version" = latest ]; then
  base="https://github.com/${repo}/releases/latest/download"
fi

command -v curl >/dev/null 2>&1 || { printf '%s\n' 'curl es requerido.' >&2; exit 1; }
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
wheel_url=""
wheel=""
if [ "$version" = latest ]; then
  wheel_url="$(curl -fsSL "$api" | sed -n 's/.*"browser_download_url": "\([^"]*fierro_harness-[^"]*\.whl\)".*/\1/p' | head -n 1)"
  [ -n "$wheel_url" ] || { printf '%s\n' 'No se encontró el wheel del último release.' >&2; exit 1; }
  wheel="${tmpdir}/$(basename "$wheel_url")"
else
  wheel_name="fierro_harness-${version#v}-py3-none-any.whl"
  wheel_url="${base}/${wheel_name}"
  wheel="${tmpdir}/${wheel_name}"
fi
curl -fsSL "$wheel_url" -o "$wheel"
uv_cmd="$(command -v uv || true)"
if [ -z "$uv_cmd" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
  uv_cmd="$(command -v uv || true)"
fi
[ -n "$uv_cmd" ] || { printf '%s\n' 'No se pudo instalar uv.' >&2; exit 1; }
exec "$uv_cmd" run --python 3.14 --with "$wheel" fierro-harness install
