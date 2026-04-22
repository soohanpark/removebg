# removebg

이미지에서 배경을 지우는 간단한 CLI 도구. [`rembg`](https://github.com/danielgatis/rembg)(U^2-Net/BiRefNet 등) 기반입니다.

## 설치

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
