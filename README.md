# streamlit-llm

- [Setup virtual env](./docs/setup/setup-virtual-env.md)
- [Poetry command](docs/portry-command.md)

## virtual env command

```bash
# activate env
source env/bin/activate

# deactivate
deactivate
```

## streamlit command

```bash
# run streamlit
streamlit run main.py
```

## Links

- [langchain hub](https://smith.langchain.com/hub)
  - 좋은 결과를 얻기 위해 참고할 수 있는 Prompt 예제들이 있음
  - Tips
    - `rlm/xxx` rlm 은 langchain 에서 제공하는 모델 이름
    - rlm 이 붙은건 평균적은 prompt 보단 `rlm` 이 붙지 않은 우선 순위의 prompt 를 사용하는 것도 좋은 선택이다.
- [serpapi](https://serpapi.com/integrations/python)
  - 참고: https://serpapi.com/integrations/python

### LLM Services

- [OpenAI API](https://platform.openai.com/)
- [Anthropic API](https://console.anthropic.com/)
- [Upstage API](https://upstage.ai/)
- [Cohere API](https://cohere.com/)
- [Jina API](https://jina.ai/)
- [DeepL API](https://www.deepl.com/docs-api)
- [perplexity API](https://pplx.ai/)

### DB

- [Pinecone API](https://www.pinecone.io/)

### bechmark

- [LogicKor(한국어 LLM benchmark)](https://lk.instruct.kr/)

## 実装順番

- `pages/dynamic-prompt.py`
- `pages/pdf-based-qa.py`
- `pages/email-bot.py`
- `pages/local-RAG.py`
  - `pdf-based-qa` 와 동일한 기능을 가지고 있음
- `pages/multi-modal.py`
- `pages/multi-tern.py`
-
