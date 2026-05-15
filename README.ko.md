# nobg

이미지에서 배경을 지우는 간단한 CLI 도구. [`rembg`](https://github.com/danielgatis/rembg)(U^2-Net/BiRefNet 등) 기반입니다.

> English documentation: [README.md](README.md)

## 빠른 설치 (One-liner)

macOS / Linux:

```bash
curl -LsSf https://raw.githubusercontent.com/soohanpark/nobg/main/install.sh | sh
```

스크립트가 [`uv`](https://docs.astral.sh/uv/)를 자동 설치한 뒤 GitHub에서 `nobg`를 내려받아 격리된 환경에 설치합니다. 다시 실행하면 그대로 최신 커밋으로 업그레이드됩니다.

> **⚠️ uv를 이번에 처음 깐 경우에는 새 터미널을 한 번 열고 시작하세요.** uv 설치 스크립트가 `~/.zshrc` / `~/.bashrc`에 PATH를 추가하는데, 이 변경은 현재 셸에 즉시 반영되지 않습니다. 다음 중 하나를 하면 됩니다.
>
> - 새 터미널 창/탭을 열기 (가장 간단)
> - 또는 현재 셸에서 `exec $SHELL -l` 실행
> - 또는 `source ~/.zshrc` (bash 사용 시 `source ~/.bashrc`)
>
> 이미 `uv`가 깔려 있던 사용자는 곧장 같은 터미널에서 `nobg`를 호출할 수 있습니다.

준비가 끝나면:

```bash
nobg --help
nobg photo.jpg                 # photo_nobg.png 생성
```

그래도 `nobg: command not found`가 뜨면 `uv tool update-shell` 실행 후 새 터미널을 여세요.

## 다른 설치 방법

GitHub에서 직접 (이미 `uv`가 깔려 있는 경우):

```bash
uv tool install git+https://github.com/soohanpark/nobg.git
```

설치 없이 한 번만 실행:

```bash
uvx --from git+https://github.com/soohanpark/nobg.git nobg input.jpg
```

`pipx` 사용자라면:

```bash
pipx install git+https://github.com/soohanpark/nobg.git
```

GPU(CUDA) 사용:

```bash
uv tool install --with onnxruntime-gpu git+https://github.com/soohanpark/nobg.git
```

> CUDA 툴킷이 시스템에 이미 설치되어 있어야 합니다.

업그레이드 / 제거:

```bash
uv tool upgrade nobg
uv tool uninstall nobg
# pipx면: pipx upgrade nobg / pipx uninstall nobg
```

### 요구 사항

- 인터넷 (최초 실행 시 `~/.u2net/`로 모델 가중치 다운로드)
- 디스크 여유 공간 약 2GB (모델 + 의존성)
- Python ≥ 3.11 (`uv`가 알아서 받아오므로 사전 설치 불필요)
- OS: Linux / macOS / Windows (Windows는 PowerShell에서 `irm https://astral.sh/uv/install.ps1 | iex`로 uv 설치 후 위 `uv tool install ...` 명령 사용)

## 사용법

```bash
# 단일 이미지
nobg photo.jpg

# 출력 경로 지정
nobg photo.jpg -o out.png

# 디렉토리 일괄 처리
nobg ./photos -o ./out

# 하위 디렉토리 포함
nobg ./photos -o ./out -r

# 다른 모델 사용 (인물/애니메 등)
nobg photo.jpg -m isnet-anime
nobg portrait.jpg -m birefnet-portrait

# 부드러운 가장자리 (alpha matting)
nobg photo.jpg --alpha-matting

# 투명 대신 배경색 채우기
nobg photo.jpg --bgcolor 255,255,255

# 마스크만 출력
nobg photo.jpg --only-mask
```

## 옵션

- `-o, --output` 출력 파일 또는 디렉토리. 기본값은 `<이름>_nobg.png`
- `-m, --model` 세그멘테이션 모델 (`u2net`, `isnet-general-use`, `birefnet-general` 등)
- `-r, --recursive` 디렉토리 재귀 탐색
- `--alpha-matting` 알파 매팅 활성화 (느리지만 경계가 매끄러움)
- `--fg-threshold`, `--bg-threshold`, `--erode-size` 알파 매팅 파라미터
- `--post-process-mask` 마스크 후처리
- `--only-mask` 컷아웃 대신 알파 마스크 출력
- `--bgcolor R,G,B[,A]` 투명 대신 단색 배경 채움
- `--overwrite` 기존 출력 덮어쓰기

## 지원 포맷

입력: `.jpg .jpeg .png .webp .bmp .tiff .tif`
출력: 기본 `.png` (투명도 유지). 확장자가 `.jpg`/`.jpeg`이면 흰 배경 위에 합성해 저장.

## 프로그래밍 방식 호출

```python
from pathlib import Path
from nobg.core import RemoveOptions, process_file

process_file(
    src=Path("input.jpg"),
    dst=Path("output.png"),
    options=RemoveOptions(model="u2net"),
)
```

## 문제 해결

| 증상 | 해결 |
| --- | --- |
| `command not found: nobg` | `uv tool update-shell` 후 새 셸 |
| `error: externally-managed-environment` | 시스템 Python 직접 설치 시도 → 위의 `uv` / `pipx` 방식 사용 |
| 첫 실행이 오래 걸림 | 모델 다운로드(정상). 이후부터 캐시 사용 |
| `No supported images found` | 입력 확장자를 `.jpg .jpeg .png .webp .bmp .tiff .tif` 중 하나로 |
| 경계가 거침 | `-m birefnet-general` 또는 `--alpha-matting` |
| CUDA 미사용 | `--with onnxruntime-gpu`로 재설치 |

## 개발 (소스 체크아웃)

```bash
git clone https://github.com/soohanpark/nobg.git
cd nobg
uv sync
uv run nobg --help
```

## 삭제

```bash
uv tool uninstall nobg     # 또는 pipx uninstall nobg
rm -rf ~/.u2net            # 모델 캐시까지 정리하려면
```
