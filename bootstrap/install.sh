#!/usr/bin/env sh
set -eu

version="${FIERRO_AGENTS_VERSION:-latest}"
repo="${FIERRO_AGENTS_REPOSITORY:-radiocutfm/harness}"
base="https://github.com/${repo}/releases/${version}/download"

if [ "$version" = latest ]; then
  base="https://github.com/${repo}/releases/latest/download"
fi

command -v curl >/dev/null 2>&1 || { printf '%s\n' 'curl es requerido.' >&2; exit 1; }
wheel="$(mktemp --suffix=.whl)"
trap 'rm -f "$wheel"' EXIT
wheel_name="fierro_harness-latest.whl"
if [ "$version" != latest ]; then
  wheel_name="fierro_harness-${version#v}-py3-none-any.whl"
fi
curl -fsSL "${base}/${wheel_name}" -o "$wheel"
uv_cmd="$(command -v uv || true)"
if [ -z "$uv_cmd" ]; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="${HOME}/.local/bin:${PATH}"
  uv_cmd="$(command -v uv || true)"
fi
[ -n "$uv_cmd" ] || { printf '%s\n' 'No se pudo instalar uv.' >&2; exit 1; }
exec "$uv_cmd" run --with "$wheel" fierro-harness install
