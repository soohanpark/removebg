# Homebrew 패키징 (`removebg`) — **현재 미지원, 추후 검토**

> **현재 상태**: numba/llvmlite/onnxruntime/opencv 등 ML 의존성이 Homebrew의 source-build 모델과 잘 맞지 않아 안정적인 설치가 불가합니다. 사용자 설치 경로는 PyPI + pipx (`pipx install removebg`)로 일원화했습니다. 이 디렉토리의 산출물은 향후 homebrew-core 승격 시도(스타·포크 기준 충족 후) 또는 wheel 기반 Formula 재작성 시 재활용을 위해 보관합니다.

이 디렉토리는 [`soohanpark/homebrew-tap`](https://github.com/soohanpark/homebrew-tap) 리포에 그대로 복사할 산출물을 보관합니다. (활성화되면) 사용자에게는 다음 한 줄로 노출됩니다.

```bash
brew install soohanpark/tap/removebg
```

## 디렉토리 구조

```
packaging/homebrew/
├── Formula/
│   └── removebg.rb        # Homebrew Formula. virtualenv 기반.
├── generate-resources.sh  # 의존성 resource 블록 자동 생성 헬퍼
└── README.md              # (이 파일)
```

## 새 버전 릴리즈 절차

다음 작업은 모두 메인테이너(저장소 소유자)가 직접 수행합니다.

### 1. 이 리포(`soohanpark/removebg`)에서 태그 푸시

`pyproject.toml`의 `version`과 일치하는 git 태그를 생성해 푸시합니다.

```bash
git tag v0.1.0
git push origin v0.1.0
```

`v*` 패턴의 태그가 푸시되면 [`.github/workflows/release.yml`](../../.github/workflows/release.yml)이 자동으로 다음을 수행합니다.

- `pyproject.toml`의 `version`과 태그가 일치하는지 검증.
- 소스 tarball(`https://github.com/soohanpark/removebg/archive/refs/tags/<tag>.tar.gz`)의 sha256 계산.
- GitHub Release 생성 + 자동 생성 changelog + Formula에 그대로 붙여 넣을 `url` / `sha256` 스니펫을 릴리즈 노트에 포함.

릴리즈 페이지의 "Homebrew Formula update" 섹션에서 `url`과 `sha256` 두 줄을 복사해 다음 단계에서 사용합니다.

### 2. Formula 갱신

`Formula/removebg.rb`에서 다음 두 항목을 갱신합니다.

- `url` — 새 태그를 가리키도록.
- `sha256` — 위에서 계산한 값.

이어서 의존성 resource 블록을 재생성합니다.

```bash
./packaging/homebrew/generate-resources.sh
```

스크립트가 `homebrew-pypi-poet`을 임시 venv에 설치한 뒤 `removebg`의 전체 의존성 트리를 해석해 `Formula/removebg.rb`의 `BEGIN_RESOURCES` / `END_RESOURCES` 마커 사이를 자동 갱신합니다.

### 3. 로컬 검증

`brew` 가 설치된 머신에서:

```bash
brew install --build-from-source ./Formula/removebg.rb
brew test removebg
brew audit --strict --new-formula removebg
brew style ./Formula/removebg.rb
```

`brew test`는 `removebg --help`가 `Usage:` 문자열을 출력하는지를 검증합니다.

엔드투엔드 검증:

```bash
python3 -c "from PIL import Image, ImageDraw; im=Image.new('RGB',(256,256),(30,30,30)); ImageDraw.Draw(im).ellipse((60,60,196,196),fill=(220,180,60)); im.save('/tmp/s.png')"
removebg /tmp/s.png -o /tmp/s_out.png -m u2netp
python3 -c "from PIL import Image; assert Image.open('/tmp/s_out.png').mode=='RGBA'; print('ok')"
```

### 4. 탭 리포에 푸시

```bash
cp -R packaging/homebrew/Formula /path/to/homebrew-tap/
cp packaging/homebrew/README.md  /path/to/homebrew-tap/
cd /path/to/homebrew-tap
git add Formula/removebg.rb README.md
git commit -m "removebg 0.1.0 (new formula)"
git push
```

### 5. 사용자 설치 흐름

```bash
brew install soohanpark/tap/removebg
# 또는
brew tap soohanpark/tap
brew install removebg
removebg --help
```

업그레이드:

```bash
brew update
brew upgrade removebg
```

## 까다로운 의존성 메모

- **`onnxruntime`** — sdist 빌드가 사실상 불가하므로 wheel resource를 사용합니다. macOS / Linux, x86_64 / arm64 별로 wheel URL이 다를 수 있어, 필요 시 Formula 내부에서 `on_macos` / `on_linux` / `on_arm` 블록으로 분기합니다.
- **`Pillow`, `numpy`, `opencv-python-headless`** — wheel 제공. poet 결과를 그대로 사용.
- **`rembg`의 `[cli]` extra** — 라이브러리만 사용하므로 plain `rembg`만 핀합니다 (현재 `pyproject.toml`도 그렇게 설정).

## 추후 homebrew-core 승격

이 프로젝트의 GitHub 지표가 다음 중 하나를 충족하고 안정 릴리즈가 누적되면 `Homebrew/homebrew-core`로 승격 PR을 보낼 수 있습니다.

- 스타 ≥ 75
- 포크 ≥ 30
- watchers ≥ 30

승격 시 Formula의 위치만 옮기면 되며, resource 핀 형식은 동일합니다.
