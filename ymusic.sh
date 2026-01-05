#!/usr/bin/env bash
set -euo pipefail

readonly VERSION='main'
: "${YM_COOKIES:=}"
: "${YM_BROWSER:=}"
: "${YM_URL:="https://music.youtube.com/playlist?list=LM"}"
: "${YM_OUTPUT_DIR:="."}"
: "${YM_TEMP_DIR:=".ymusic"}"
: "${YM_FORCE_IPV4:=false}"

if [[ -n "${COLAB_RELEASE_TAG:-}" ]]; then
	INSTALL_DEPENDENCIES="true"
else
	INSTALL_DEPENDENCIES="${INSTALL_DEPENDENCIES:-false}"
fi

YTDLP_OPTS=(--no-warnings --fragment-retries 10)
YTDLP_COOKIE_ARGS=()

function usage() {
	echo "Usage: "$0" [OPTION...] <URL>"
	echo "Options:"
	echo "  -h, --help             Show help"
	echo "  -v, --version          Show version"
	echo "  -4, --ipv4             Force IPv4"
	echo "  -c, --cookies=<path>   Cookies file path"
	echo "  -b, --browser=<name>   Load cookies from browser"
	echo "  -o, --output=<path>    Output directory"
	echo "  --temp-dir=<path>      Temporary directory"
	echo ""
	echo "Environment:"
	echo "  INSTALL_DEPENDENCIES   Set 'true' to auto-install packages (default: false)"
	exit 0
}

function print_version() {
	echo "${VERSION}"
	exit 0
}

function cleanup() {
	local exit_code=$?
	rm -rf "${YM_TEMP_DIR}"
	exit "${exit_code}"
}
trap cleanup EXIT INT TERM

function error() {
	echo -e "❌ [ERROR] ${1:-}" >&2
	exit 1
}

function log() {
	echo "[INFO] ${1:-}"
}

function install_dependency() {
	local dependency="${1%%=*}"
	local pkg_manager="${2:-apt}"
	local pkg_name="${3:-${dependency}}"
	local sudo=""
	if ! command -v "${dependency}" &>/dev/null; then
		if ! "${INSTALL_DEPENDENCIES}"; then
			error "Dependency '${dependency}' is missing. Please install it manually or set INSTALL_DEPENDENCIES=true"
		fi
		log "Installing: ${dependency}..."
		[ "$(id -u)" -gt 0 ] && sudo="sudo"
		case "${pkg_manager}" in
			apt)
				if command -v apt-get &>/dev/null; then
					${sudo} apt-get update -qq && ${sudo} apt-get install -y "${pkg_name}" >/dev/null
				else
					error "apt-get not found. Cannot auto-install '${dependency}'. Please install it manually."
				fi
			;;
			pip)
				if ! command -v pip &>/dev/null && ! command -v pip3 &>/dev/null; then
					install_dependency "pip" "apt" "python3-pip"
				fi
				python3 -m pip install --quiet --break-system-packages "${pkg_name}"
			;;
		esac
	fi
}

function check_dependencies() {
	log "Checking base dependencies..."
	install_dependency "ffmpeg"
	install_dependency "python3"
	install_dependency "yt-dlp" "pip"
}

function call_ytdlp() {
	local raw_args="$*"
	local force_cookies=false

	# WL = Watch Later, LL = Liked Videos, LM = Liked Music
	if [[ "${raw_args}" =~ list=(L[LM]|WL) ]] || [[ "${raw_args}" == *"--mark-watched"* ]] || [[ "${raw_args}" == *"--batch-file"* ]]; then
		force_cookies=true
	fi
	if ! "${force_cookies}" && yt-dlp "${YTDLP_OPTS[@]}" "$@" 2>/dev/null; then
		return 0
	fi
	local cmd_args=("${YTDLP_OPTS[@]}")
	[[ ${#YTDLP_COOKIE_ARGS[@]} -gt 0 ]] && cmd_args+=("${YTDLP_COOKIE_ARGS[@]}")
	yt-dlp "${cmd_args[@]}" "$@"
}

function fetch_track() {
	local url="$1"
	local title="$2"

	local final_file="${YM_OUTPUT_DIR}/${title}.mp3"
	if [[ -f "${final_file}" ]]; then
		log "File exists: ${final_file}. Skipping."
		return
	fi

	log "Processing: ${title}"

	local video_id="${url:(-11)}"
	local fetch_opts=(
		--progress
		--extract-audio
		--audio-format mp3
		--audio-quality 0
		--embed-thumbnail
		--embed-metadata
		--output "${YM_TEMP_DIR}/temp_${video_id}.%(ext)s"
	)
	if call_ytdlp "${fetch_opts[@]}" -t mp3 "${url}"; then
		local audio_file=$(find "${YM_TEMP_DIR}" -type f -name "temp_${video_id}.*" | head -n 1)
		if [[ -n "${audio_file}" ]]; then
			mv "${audio_file}" "${final_file}"
			return 0
		fi
	fi
	return 1
}

function main() {
	if [[ $# -gt 0 ]]; then
		local OPTIONS="hv4c:b:o:"
		local LONGOPTS="help,version,ipv4,cookies:,browser:,output:,temp-dir:"
		eval set -- $(getopt --options="${OPTIONS}" --longoptions="${LONGOPTS}" --name "$0" -- "$@")
		while getopts "${OPTIONS}-:" OPT; do
			if [[ "${OPT}" = "-" ]]; then
				OPT="${OPTARG}"
				OPTARG=""
				if [[ "${LONGOPTS}" =~ (^|,)${OPT}: ]]; then
					OPTARG="${!OPTIND}"
					((OPTIND++))
				fi
			fi
			case "${OPT}" in
				h|help) usage;;
				v|version) print_version;;
				4|ipv4) YM_FORCE_IPV4=true;;
				c|cookies) YM_COOKIES="${OPTARG}";;
				b|browser) YM_BROWSER="${OPTARG}";;
				o|output) YM_OUTPUT_DIR="${OPTARG}";;
				temp-dir) YM_TEMP_DIR="${OPTARG}";;
			esac
		done
		shift $((OPTIND - 1))
		[[ -n "${1:-}" ]] && YM_URL="$1"
	fi
	[[ -z "${YM_URL}" ]] && error "URL or File not specified."

	"${YM_FORCE_IPV4}" && YTDLP_OPTS+=(--force-ipv4)
	[[ -n "${YM_COOKIES}" ]] && YTDLP_COOKIE_ARGS+=(--cookies "${YM_COOKIES}")
	[[ -n "${YM_BROWSER}" ]] && YTDLP_COOKIE_ARGS+=(--cookies-from-browser "${YM_BROWSER}")

	check_dependencies
	mkdir -p "${YM_OUTPUT_DIR}" "${YM_TEMP_DIR}"

	local is_batch_file=false
	local input_args=()
	
	if [[ -f "${YM_URL}" ]]; then
		log "Input is a file. Using batch mode: ${YM_URL}"
		is_batch_file=true
		input_args=(--batch-file "${YM_URL}")
	else
		input_args=("${YM_URL}")
	fi

	log "Fetching playlist info..."
	local fetch_opts=(
		--ignore-errors
		--flat-playlist
		--print filename

		# === Правила очистки ===
		--replace-in-metadata "uploader" " - Topic" ""
		--replace-in-metadata "artist,uploader,title" "\s*[:：]\s*" " - "
		--replace-in-metadata "artist,uploader,title" "[/⧸]" "_"
		--replace-in-metadata "artist,uploader,title" "[\"＂“”«»]" "'"
		--replace-in-metadata "artist,uploader,title" "\s*[|｜]\s*" " - "
		--replace-in-metadata "artist,uploader,title" "\s*[—–]\s*" " - "

		# === Правила парсинга ===
		--parse-metadata "uploader:%(artist)s"
		--parse-metadata "title:%(artist)s - %(title)s"
		--parse-metadata "playlist_index:%(track_number)s"

		# === Формат вывода ===
		--output "%(uploader)s - %(title)s [%(id)s]"
	)
	local playlist_items=()
	mapfile -t playlist_items < <(call_ytdlp "${fetch_opts[@]}" "${input_args[@]}")

	local count=1
	local total=${#playlist_items[@]}
	[[ ${total} -eq 0 ]] && error "Playlist is empty or failed to fetch."

	if [[ "${YM_URL}" == *"list="* ]] && ! "${is_batch_file}"; then
		log "Sync mode: Checking for removed tracks..."

		declare -A valid_ids
		for item in "${playlist_items[@]}"; do
			local id="${item:(-12):11}"
			valid_ids["${id}"]=1
		done

		local deleted_count=0
		while IFS= read -r -d '' file; do
			if [[ "${file}" =~ \[([a-zA-Z0-9_-]{11})\]\.mp3$ ]]; then
				local file_id="${BASH_REMATCH[1]}"
				if [[ -z "${valid_ids[${file_id}]:-}" ]]; then
					log "Deleting removed track: $(basename "${file}")"
					rm "${file}"
					((deleted_count++))
				fi
			fi
		done < <(find "${YM_OUTPUT_DIR}" -maxdepth 1 -name "* \[???????????\].mp3" -print0)

		if [[ ${deleted_count} -gt 0 ]]; then
			log "Cleaned ${deleted_count} files."
		else
			log "No files to clean."
		fi
	fi

	local failed_items=()
	for item in "${playlist_items[@]}"; do
		log "=== [${count}/${total}] Processing ==="
		if [[ "${item}" =~ ^NA\ -\ \[(Deleted|Private)\ video\] ]]; then
			((count++))
			continue
		fi
		local title="${item}"
		local id="${item:(-12):11}"
		local video_url="https://music.youtube.com/watch?v=${id}"
		if ! fetch_track "${video_url}" "${title}"; then
			log "⚠️ Download failed for: ${title}"
			failed_items+=("# ${title}"$'\n'"${video_url}")
		fi
		((count++))
	done

	if [[ ${#failed_items[@]} -gt 0 ]]; then
		echo ""
		log "----------------------------------------------------------------"
		log "⚠️  COMPLETED WITH ERRORS"
		log "The following ${#failed_items[@]} tracks failed to download:"
		echo ""
		for failed in "${failed_items[@]}"; do
			echo "${failed}"
		done
		log "----------------------------------------------------------------"
	else
		log "✅ All completed successfully."
	fi
}

if [[ "${BASH_SOURCE:-${0}}" == "${0}" ]]; then
	[[ -f ".env" ]] && source ".env"
	main "$@"
fi
