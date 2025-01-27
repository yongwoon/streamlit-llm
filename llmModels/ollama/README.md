# Download Model

## HuggingFace

허깅페이스(HuggingFace) 에서 오픈모델을 다운로드 받습니다 (.gguf 확장자)

- GGUF: https://huggingface.co/teddylee777/EEVE-Korean-Instruct-10.8B-v1.0-gguf

다룬로드 한 모델을 ollma 에서 실행시키는 방법

```bash
# model 을 ollama 에 추가
cd llmModels/ollama
ollama create EEVE-Korean-Instruct-10.8B-v1.0-Q8_0.gguf

# local model 실행하여 test 해보기
ollama run EEVE-Korean-Instruct-10.8B-v1.0-Q8_0.gguf
```

## Ollama 제공하는 모델

`ollama pull <name-of-model>` 명령을 사용하여 사용 가능한 LLM 모델을 가져오세요.

- 예: `ollama pull gemma:7b`

아래의 경로에 모델의 기본 태그 버전이 다운로드됩니다.

- Mac: `~/.ollama/models`
- Linux/WSL: `/usr/share/ollama/.ollama/models`

`ollama list`로 가져온 모든 모델을 확인하세요.

`ollama run <name-of-model>`로 명령줄에서 모델과 직접 채팅하세요.

## Modelfile 로부터 커스텀 모델 생성하기

모델을 임포트하기 위해 ModelFile을 먼저 생성해야 합니다. 자세한 정보는 [ModelFile 관련 공식 문서](https://github.com/ollama/ollama/blob/69f392c9b7ea7c5cc3d46c29774e37fdef51abd8/docs/modelfile.md)에서 확인할 수 있습니다.

> 샘플 모델파일 예시

```text
FROM ggml-model-Q5_K_M.gguf

TEMPLATE """{{- if .System }}
<s>{{ .System }}</s>
{{- end }}
<s>Human:
{{ .Prompt }}</s>
<s>Assistant:
"""

SYSTEM """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions."""

PARAMETER stop <s>
PARAMETER stop </s>
```

---

## Chat 모델

Llama `chat` 모델(예: `ollama pull llama2:7b-chat`)을 사용하는 경우 `ChatOllama` 인터페이스를 사용할 수 있습니다. 여기에는 시스템 메시지 및 사용자 입력을 위한 special tokens이 포함됩니다.

## Ollama 모델 활용

- 모든 로컬 모델은 `localhost:11434`에서 제공됩니다.
- Command 창에서 직접 상호 작용하려면 `ollama run <name-of-model>`을 실행하세요.
