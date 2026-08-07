#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  .claude/scripts/check-docker.sh [--path FILE|DIR]... [--all] [--addon-consistency]

Checks Dockerfile / build.json / build.yaml / config.yaml / .dockerignore against
.claude/rules/common/dockerfile.md (通用铁律 + add-on 镜像约定).

Modes:
  (default)            files changed since HEAD + add-on template consistency
  --path FILE|DIR      check specific file(s) or add-on dir(s); repeatable
  --all                scan every top-level add-on dir (reports baseline debt)
  --addon-consistency  only the scaffold <-> template diff

Exit codes: 0 pass, 1 failure(s), 2 usage error.
USAGE
}

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCAFFOLD_DOCKERFILE="${PROJECT_ROOT}/.claude/skills/hassio-addon-sync/templates/new-addon/Dockerfile"
TEMPLATE_DOCKERFILE="${PROJECT_ROOT}/.claude/templates/docker/Dockerfile.addon"

CHECK_ALL=false
CONSISTENCY_ONLY=false
PATHS=()
status=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --path)
      [ "$#" -ge 2 ] || { echo "check-docker: --path requires a value" >&2; exit 2; }
      PATHS+=("$2")
      shift 2
      ;;
    --all)
      CHECK_ALL=true
      shift
      ;;
    --addon-consistency)
      CONSISTENCY_ONLY=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "check-docker: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

fail() {
  local file="$1" ln="$2" msg="$3"
  if [ -n "$ln" ]; then
    echo "check-docker: ${file#$PROJECT_ROOT/}#${ln}: ${msg}"
  else
    echo "check-docker: ${file#$PROJECT_ROOT/}: ${msg}"
  fi
  status=1
}

rel() { printf '%s' "${1#$PROJECT_ROOT/}"; }

# 输出每个逻辑 RUN 语句：先起始行号，再整条内容（含 \ 续行）。行内不作过滤。
run_blocks() {
  awk '
    function flush() {
      if (block != "") { print start; print block; block = "" }
    }
    /^[[:space:]]*RUN[[:space:]]/ {
      if (block != "") flush()
      start = NR; block = $0
      if ($0 !~ /\\$/) flush()
      next
    }
    {
      if (block != "") {
        if (block ~ /\\$/) { block = block " " $0; if ($0 !~ /\\$/) flush() }
        else flush()
      }
    }
    END { if (block != "") flush() }
  ' "$1"
}

check_addon_consistency() {
  if [ ! -f "$SCAFFOLD_DOCKERFILE" ]; then
    echo "check-docker: 脚手架 Dockerfile 不存在: $(rel "$SCAFFOLD_DOCKERFILE")" >&2
    status=1
    return
  fi
  if [ ! -f "$TEMPLATE_DOCKERFILE" ]; then
    echo "check-docker: add-on 模板不存在: $(rel "$TEMPLATE_DOCKERFILE")" >&2
    status=1
    return
  fi
  if ! diff -q "$SCAFFOLD_DOCKERFILE" "$TEMPLATE_DOCKERFILE" >/dev/null 2>&1; then
    echo "check-docker: add-on Dockerfile 模板与脚手架不一致（必须逐字节一致，铁律 addon-2）:"
    diff -u "$SCAFFOLD_DOCKERFILE" "$TEMPLATE_DOCKERFILE" | sed 's/^/  /'
    status=1
  fi
}

check_dockerfile() {
  local file="$1"
  local is_addon=false exempt=false
  local ln rest ref
  if grep -qE '^ARG[[:space:]]+BUILD_FROM([[:space:]]|=|$)' "$file"; then is_addon=true; fi
  if grep -qE '#[[:space:]]*(check-docker:[[:space:]]*exempt|hadolint[[:space:]]+ignore=DL3007)' "$file"; then exempt=true; fi
  stages="$(grep -oE 'AS[[:space:]]+[A-Za-z_][A-Za-z0-9_]*' "$file" | awk '{print $2}' | sort -u || true)"
  is_stage() { grep -qxF -- "$1" <<<"$stages"; }

  # 1. 基础镜像 pinning（铁律 a）
  if [ "$is_addon" = true ]; then
    while IFS=: read -r ln rest; do
      ref="$(printf '%s' "$rest" | sed -E 's/^[[:space:]]*FROM([[:space:]]+--[^[:space:]]+)*[[:space:]]+//; s/[[:space:]].*$//')"
      case "$ref" in
        '$BUILD_FROM'|'${BUILD_FROM}') : ;;
        *:latest*) fail "$file" "$ln" "FROM 使用 latest（add-on 禁浮动 tag）" ;;
        *@sha256:*) fail "$file" "$ln" "FROM 使用 digest（add-on 禁止 digest，tag 必须可读）" ;;
      esac
    done < <(grep -nE '^[[:space:]]*FROM[[:space:]]' "$file" || true)
  else
    while IFS=: read -r ln rest; do
      [ "$exempt" = true ] && continue
      ref="$(printf '%s' "$rest" | sed -E 's/^[[:space:]]*FROM([[:space:]]+--[^[:space:]]+)*[[:space:]]+//; s/[[:space:]].*$//')"
      case "$ref" in
        scratch) : ;;
        *:latest*) fail "$file" "$ln" "FROM 使用 latest（禁浮动 tag）" ;;
        *:stable*) fail "$file" "$ln" "FROM 使用 stable（禁浮动 tag）" ;;
        *:*) : ;;
        *) if is_stage "$ref"; then :; else fail "$file" "$ln" "FROM 裸仓库名（隐式 latest），请 pin 具体版本"; fi ;;
      esac
    done < <(grep -nE '^[[:space:]]*FROM[[:space:]]' "$file" || true)
  fi

  # 2. 非 root USER（铁律 c，仅 generic）
  if [ "$is_addon" != true ]; then
    if grep -qE '^[[:space:]]*USER[[:space:]]+root([[:space:]]|$)' "$file"; then
      fail "$file" "" "USER root（应降权，铁律 c）"
    elif ! grep -qE '^[[:space:]]*USER[[:space:]]' "$file" && \
         ! grep -qE '#[[:space:]]*(check-docker:[[:space:]]*(exempt|root-ok)|hadolint[[:space:]]+ignore=DL3002)' "$file"; then
      fail "$file" "" "缺少非 root USER（铁律 c）"
    fi
  fi

  # 3. HEALTHCHECK（铁律 d，仅 generic）
  if [ "$is_addon" != true ]; then
    if ! grep -qE '^[[:space:]]*HEALTHCHECK[[:space:]]' "$file" && \
       ! grep -qE '#[[:space:]]*(check-docker:[[:space:]]*(exempt|no-healthcheck))' "$file"; then
      fail "$file" "" "缺少 HEALTHCHECK（长驻服务必备，铁律 d）"
    fi
  fi

  # 4. 密钥/敏感信息（铁律 e）
  while IFS= read -r hit; do
    ln="${hit%%:*}"
    fail "$file" "$ln" "ENV/ARG 含疑似密钥且非占位符（铁律 e）: ${hit#*:}"
  done < <(perl -ne '
    next unless /^\s*(?:ENV|ARG)\s+/;
    my $ln=$.;
    while (/([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"?([^"\s]*)"?/g) {
      my ($k,$v)=($1,$2);
      next unless $k =~ /(?:KEY|PASSWORD|TOKEN|SECRET|PASSWD|_DSN|_API_KEY)$/;
      next if $v eq "" || $v =~ /^(your-|example-|change-me|placeholder)/i;
      print "$ln:$k=$v\n";
    }
  ' "$file" || true)
  while IFS=: read -r ln rest; do
    case "$rest" in
      *.env*|*.pem*|*.key*) fail "$file" "$ln" "COPY 密钥/敏感文件（铁律 e）" ;;
    esac
  done < <(grep -nE '^[[:space:]]*COPY[[:space:]]' "$file" || true)

  # 5. 镜像精简（铁律 f，仅 generic）——按逻辑 RUN 语句（连接 \ 续行）检查
  if [ "$is_addon" != true ]; then
    while IFS= read -r ln; do
      IFS= read -r block
      if [[ "$block" =~ apk[[:space:]]+add ]] && ! [[ "$block" =~ --no-cache ]]; then
        fail "$file" "$ln" "apk add 未用 --no-cache（铁律 f）"
      fi
      if [[ "$block" =~ apt-get[[:space:]]+install ]] && ! [[ "$block" =~ --no-install-recommends ]]; then
        fail "$file" "$ln" "apt-get install 未用 --no-install-recommends（铁律 f）"
      fi
      if [[ "$block" =~ apt-get[[:space:]]+update ]] && ! [[ "$block" =~ rm[[:space:]]+-rf[[:space:]]+/var/lib/apt/lists ]]; then
        fail "$file" "$ln" "apt-get update 未同层清理 apt 缓存（铁律 f）"
      fi
    done < <(run_blocks "$file" || true)
    while IFS=: read -r a b; do
      fail "$file" "$a" "相邻 RUN 可合并为单层（铁律 f）"
    done < <(awk '/^[[:space:]]*RUN/{ if (prev && NR == prev+1) print prev ":" NR; prev=NR }' "$file" || true)
  fi

  # 6. CMD/ENTRYPOINT exec 形式（铁律 h）
  while IFS=: read -r ln rest; do
    content="$(printf '%s' "$rest" | sed -E 's/^(CMD|ENTRYPOINT)[[:space:]]+//')"
    case "$content" in
      \[*) : ;;
      *) fail "$file" "$ln" "CMD/ENTRYPOINT 用 shell 形式，应改 JSON 数组 exec 形式（铁律 h）" ;;
    esac
  done < <(grep -nE '^(CMD|ENTRYPOINT)[[:space:]]' "$file" || true)
}

check_build_from() {
  local file="$1"
  local ln
  while IFS=: read -r ln rest; do
    fail "$file" "$ln" "build_from 使用 latest/digest（add-on 必须 pin 具体版本 tag）"
  done < <(grep -nE '(:latest|@sha256:)' "$file" || true)
}

check_config_yaml() {
  local file="$1"
  local il ln image
  il="$(grep -nE '^[[:space:]]*image:[[:space:]]' "$file" | head -1 || true)"
  [ -n "$il" ] || return 0
  ln="${il%%:*}"
  image="$(printf '%s' "$il" | sed -E 's/^[0-9]+:[[:space:]]*image:[[:space:]]*//; s/[[:space:]]*$//' | sed "s/^[\"']//; s/[\"']\$//")"

  # 8. image {arch} 形态（铁律 addon-3）
  case "$image" in
    *'{arch}'*)
      if printf '%s' "$image" | grep -qE '^homeassistant/\{arch\}-addon-[A-Za-z0-9_-]+$' || \
         printf '%s' "$image" | grep -qE '^[A-Za-z0-9./:_-]+-\{arch\}$' || \
         printf '%s' "$image" | grep -qE '^[A-Za-z0-9./:_-]+/\{arch\}$'; then
        : # ok
      else
        fail "$file" "$ln" "image 含 {arch} 但形态不合法（只允许四种形态，铁律 addon-3）"
      fi
      ;;
    *)
      if printf '%s' "$image" | grep -qE '^[A-Za-z0-9./:_-]+$'; then
        : # ok
      else
        fail "$file" "$ln" "image 值不合法"
      fi
      ;;
  esac

  # 9. source: local 保护（铁律 addon-7）
  if grep -qE '^[[:space:]]*source:[[:space:]]*local([[:space:]]|$)' "$file" && \
     printf '%s' "$image" | grep -qE 'ghcr\.nju\.edu\.cn'; then
    fail "$file" "$ln" "source: local 的 image 被改写为镜像源（铁律 addon-7，永不改写）"
  fi
}

check_file() {
  local f="$1"
  case "$(basename "$f")" in
    Dockerfile*) check_dockerfile "$f" ;;
    build.json|build.yaml) check_build_from "$f" ;;
    config.yaml) check_config_yaml "$f" ;;
  esac
}

collect_dir() {
  local dir="$1" b
  for b in Dockerfile build.json build.yaml config.yaml .dockerignore; do
    [ -f "$dir/$b" ] && printf '%s\n' "$dir/$b"
  done
}

warn_missing_dockerignore() {
  local dir="$1"
  [ -f "$dir/Dockerfile" ] || return 0
  if { [ -d "$dir/node_modules" ] || [ -d "$dir/.git" ]; } && [ ! -f "$dir/.dockerignore" ]; then
    echo "check-docker: warn: $(rel "$dir"): 构建上下文较大但缺 .dockerignore（铁律 b）"
  fi
}

collect_changed() {
  { git -C "$PROJECT_ROOT" diff --name-only --diff-filter=ACMR HEAD; \
    git -C "$PROJECT_ROOT" ls-files --others --exclude-standard; } \
    | sort -u | while IFS= read -r f; do
        [ -n "$f" ] || continue
        case "$(basename "$f")" in
          Dockerfile*|build.json|build.yaml|config.yaml|.dockerignore) printf '%s\n' "$f" ;;
          *) case "$f" in .claude/templates/docker/*) printf '%s\n' "$f" ;; esac ;;
        esac
      done
}

FILES=()

if [ "$CONSISTENCY_ONLY" = true ]; then
  check_addon_consistency
else
  if [ "$CHECK_ALL" = true ]; then
    for dir in "$PROJECT_ROOT"/*/; do
      b="$(basename "${dir%/}")"
      case "$b" in .*|docs|workspace) continue ;; esac
      while IFS= read -r f; do FILES+=("$f"); done < <(collect_dir "${dir%/}")
      warn_missing_dockerignore "${dir%/}"
    done
  elif [ "${#PATHS[@]}" -gt 0 ]; then
    for p in "${PATHS[@]}"; do
      case "$p" in /*) p_abs="$p" ;; *) p_abs="$PROJECT_ROOT/$p" ;; esac
      if [ -d "$p_abs" ]; then
        while IFS= read -r f; do FILES+=("$f"); done < <(collect_dir "$p_abs")
        warn_missing_dockerignore "$p_abs"
      elif [ -f "$p_abs" ]; then
        FILES+=("$p_abs")
      else
        echo "check-docker: 路径不存在: $p" >&2
        exit 1
      fi
    done
  else
    while IFS= read -r f; do FILES+=("$f"); done < <(collect_changed)
  fi

  # 去重
  if [ "${#FILES[@]}" -gt 0 ]; then
    mapfile -t FILES < <(printf '%s\n' "${FILES[@]}" | sort -u)
  fi

  if [ "${#FILES[@]}" -gt 0 ]; then
    echo "Docker check: $(rel "$PROJECT_ROOT")  (${#FILES[@]} 个目标文件)"
    for f in "${FILES[@]}"; do
      check_file "$f"
    done
    echo
  fi

  check_addon_consistency
fi

if [ "$status" -eq 0 ]; then
  echo "Docker check passed."
else
  echo "Docker check failed."
fi
exit "$status"
