# removebg

이미지에서 배경을 지우는 간단한 CLI 도구. [`rembg`](https://github.com/danielgatis/rembg)(U^2-Net/BiRefNet 등) 기반입니다.

## AI 에이전트 가이드 (AI Agent Guide)

> Claude Code, Cursor, 기타 코드 에이전트가 이 문서만 보고 설치·검증·사용할 수 있도록 작성한 섹션입니다. 순서대로 실행하세요.

### 요구 사항

- Python `>= 3.9`
- pip `>= 23` 권장
- 인터넷 접속 (최초 실행 시 `~/.u2net/`로 모델 가중치를 다운로드)
- 디스크 여유 공간 `>= 2 GB` (모델 + 의존성)
- OS: Linux / macOS / Windows

사전 확인:

```bash
python --version    # Python 3.9 이상인지 확인
pip --version
```

### 설치 (권장: 격리된 가상 환경)

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -U pip
pip install -e .
```

GPU를 사용할 경우 `pip install -e '.[gpu]'`로 교체합니다. CUDA 툴킷이 시스템에 설치되어 있어야 합니다.

### 설치 검증

아래 두 명령이 모두 0 exit code로 끝나야 정상입니다.

```bash
removebg --help
python -c "import removebg, rembg, PIL, onnxruntime; print('ok')"
```

선택: 합성 이미지를 만들어 실제 파이프라인을 한 번 실행해 보기.

```bash
python - <<'PY'
from PIL import Image, ImageDraw
img = Image.new("RGB", (256, 256), (30, 30, 30))
ImageDraw.Draw(img).ellipse((60, 60, 196, 196), fill=(220, 180, 60))
img.save("/tmp/removebg_sample.png")
PY
removebg /tmp/removebg_sample.png -o /tmp/removebg_sample_out.png -m u2netp
python -c "from PIL import Image; im=Image.open('/tmp/removebg_sample_out.png'); assert im.mode=='RGBA'; print('verified')"
```

> 최초 실행에서는 u2netp 모델(~4.6MB) 또는 선택한 모델을 다운로드하므로 수 초 ~ 수 분이 걸릴 수 있습니다.

### 최소 사용 예 (Minimal Recipes)

| 목표 | 명령 |
| --- | --- |
| 단일 이미지 투명 배경 PNG | `removebg input.jpg` |
| 출력 경로 지정 | `removebg input.jpg -o out.png` |
| 디렉토리 일괄 처리 | `removebg ./in -o ./out` |
| 하위 디렉토리 포함 | `removebg ./in -o ./out -r` |
| 인물 사진 고품질 | `removebg portrait.jpg -m birefnet-portrait --alpha-matting` |
| 흰 배경 JPEG | `removebg input.jpg -o out.jpg --bgcolor 255,255,255` |
| 마스크만 추출 | `removebg input.jpg --only-mask -o mask.png` |

### 실패 시 대응 (Troubleshooting Playbook)

| 증상 | 원인 | 해결 |
| --- | --- | --- |
| `ModuleNotFoundError: rembg` | 설치 실패 또는 가상환경 미활성화 | 가상환경 재활성화 후 `pip install -e .` |
| `onnxruntime` 설치 실패 | Python 버전 비호환 | Python 3.9~3.12로 재시도 |
| 첫 실행이 오래 걸림 | 모델 다운로드 중 | 정상. 이후부터 캐시 사용 |
| `No supported images found` | 입력 확장자 미지원 | 지원 포맷(`.jpg .jpeg .png .webp .bmp .tiff .tif`)으로 변환 |
| 경계가 거침 | 기본 모델의 한계 | `-m birefnet-general` 또는 `--alpha-matting` 추가 |
| CUDA 미사용 | CPU 버전 설치됨 | `pip install -e '.[gpu]'` 후 재설치 |

### 프로그래밍 방식 호출

CLI 없이 Python에서 직접 사용하려면:

```python
from pathlib import Path
from removebg.core import RemoveOptions, process_file

process_file(
    src=Path("input.jpg"),
    dst=Path("output.png"),
    options=RemoveOptions(model="u2net"),
)
```

### 에이전트 체크리스트

- [ ] Python 3.9+ 확인
- [ ] 가상환경 생성 및 활성화
- [ ] `pip install -e .` 성공
- [ ] `removebg --help` 출력 확인
- [ ] 샘플 이미지로 end-to-end 검증
- [ ] 필요 시 `-m` 옵션으로 모델 교체

---

## 설치

### Homebrew (macOS / Linux)

```bash
brew install soohanpark/tap/removebg
```

업그레이드는 `brew upgrade removebg`. Formula는 [`soohanpark/homebrew-tap`](https://github.com/soohanpark/homebrew-tap)에서 호스팅하며, 이 리포의 [`packaging/homebrew/`](packaging/homebrew/)에서 관리됩니다.

### pip (소스 체크아웃)

```bash
pip install -e .
```

GPU(ONNX Runtime CUDA)를 쓰려면:

```bash
pip install -e '.[gpu]'
```

## 사용법

```bash
# 단일 이미지
removebg photo.jpg

# 출력 경로 지정
removebg photo.jpg -o out.png

# 디렉토리 일괄 처리
removebg ./photos -o ./out

# 하위 디렉토리 포함
removebg ./photos -o ./out -r

# 다른 모델 사용 (인물/애니메 등)
removebg photo.jpg -m isnet-anime
removebg portrait.jpg -m birefnet-portrait

# 부드러운 가장자리 (alpha matting)
removebg photo.jpg --alpha-matting

# 투명 대신 배경색 채우기
removebg photo.jpg --bgcolor 255,255,255

# 마스크만 출력
removebg photo.jpg --only-mask
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

## 삭제

패키지 제거:

```bash
pip uninstall removebg
```

의존성(`rembg`, `onnxruntime`, `Pillow`, `click` 등)까지 같이 지우려면:

```bash
pip uninstall removebg rembg onnxruntime Pillow click
```

> GPU 버전을 설치했다면 `onnxruntime` 대신 `onnxruntime-gpu`를 지정하세요.

`rembg`가 처음 실행될 때 모델 파일을 `~/.u2net/`에 캐시합니다. 모델 가중치도 함께 정리하려면:

```bash
rm -rf ~/.u2net
```

소스까지 완전히 제거하려면 클론한 디렉토리를 삭제합니다:

```bash
rm -rf /path/to/removebg
```
