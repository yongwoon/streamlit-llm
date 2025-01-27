# Parser

## 주요 메서드

대부분의 OutputParser에는 주로 **두 가지 핵심 메서드**가 구현되어 있습니다.

- **`get_format_instructions()`**: 언어 모델이 출력해야 할 정보의 형식을 정의하는 지침을 제공합니다. 예를 들어, 언어 모델이 출력해야 할 데이터의 필드와 그 형태를 설명하는 지침을 문자열로 반환할 수 있습니다. 이 지침은 언어 모델이 출력을 구조화하고 특정 데이터 모델에 맞게 변환하는 데 매우 중요합니다.

- **`parse()`**: 언어 모델의 출력(문자열로 가정)을 받아 이를 특정 구조로 분석하고 변환합니다. Pydantic과 같은 도구를 사용하여 입력된 문자열을 사전 정의된 스키마에 따라 검증하고, 해당 스키마를 따르는 데이터 구조로 변환합니다.

ex.

- `from langchain_core.output_parsers import PydanticOutputParser`
- `from langchain_core.output_parsers import CommaSeparatedListOutputParser`
- `from langchain.output_parsers import StructuredOutputParser
- `from langchain_core.output_parsers import JsonOutputParser`
- `from langchain.output_parsers import PandasDataFrameOutputParser`
- `from langchain.output_parsers import DatetimeOutputParser`
- `from langchain.output_parsers.enum import EnumOutputParser`
- `from langchain.output_parsers import OutputFixingParser`

## class

### PydanticOutputParser

`PydanticOutputParser`는 언어 모델의 출력을 **구조화된 정보**로 변환하는 데 도움을 주는 클래스입니다. 이 클래스는 단순 텍스트 응답 대신 **명확하고 체계적인 형태로 필요한 정보를 제공**할 수 있습니다.

이 클래스를 활용하면 언어 모델의 출력을 특정 데이터 모델에 맞게 변환하여 정보를 더 쉽게 처리하고 활용할 수 있습니다.

- 주요 메서드

`PydanticOutputParser` (대부분의 OutputParser에 해당)에는 주로 **두 가지 핵심 메서드**가 구현되어야 합니다.

**`get_format_instructions()`**: 언어 모델이 출력해야 할 정보의 형식을 정의하는 지침을 제공합니다. 예를 들어, 언어 모델이 출력해야 할 데이터의 필드와 그 형태를 설명하는 지침을 문자열로 반환할 수 있습니다. 이 지침은 언어 모델이 출력을 구조화하고 특정 데이터 모델에 맞게 변환하는 데 매우 중요합니다.

**`parse()`**: 언어 모델의 출력(문자열로 가정)을 받아 이를 특정 구조로 분석하고 변환합니다. Pydantic과 같은 도구를 사용하여 입력된 문자열을 사전 정의된 스키마에 따라 검증하고, 해당 스키마를 따르는 데이터 구조로 변환합니다.

- 참고 자료

### CommaSeparatedListOutputParser

`CommaSeparatedListOutputParser`는 쉼표로 구분된 항목 목록을 반환할 필요가 있을 때 유용한 출력 파서입니다.

이 파서를 사용하면, 입력된 데이터나 요청된 정보를 쉼표로 구분하여 명확하고 간결한 목록 형태로 제공할 수 있습니다. 예를 들어, 여러 개의 데이터 포인트, 이름, 항목 또는 다양한 값을 나열할 때 효과적으로 정보를 정리하고 사용자에게 전달할 수 있습니다.

이 방법은 정보를 구조화하고 가독성을 높이며, 특히 데이터를 다루거나 리스트 형태의 결과를 요구하는 경우에 매우 유용합니다.

### StructuredOutputParser

StructuredOutputParser는 LLM에 대한 답변을 `dict` 형식으로 구성하고, key/value 쌍으로 여러 필드를 반환하고자 할 때 유용하게 사용할 수 있습니다.

- 장점

Pydantic/JSON 파서가 더 강력하다는 평가를 받지만, StructuredOutputParser는 로컬 모델과 같은 덜 강력한 모델에서도 유용합니다. 이는 GPT나 Claude 모델보다 인텔리전스가 낮은(즉, parameter 수가 적은) 모델에서 특히 효과적입니다.

- 참고 사항

로컬 모델의 경우 `Pydantic` 파서가 동작하지 않는 상황이 빈번하게 발생할 수 있습니다. 이러한 경우, 대안으로 StructuredOutputParser를 사용하는 것이 좋은 해결책이 될 수 있습니다.

### JsonOutputParser

JsonOutputParser는 사용자가 원하는 JSON 스키마를 지정할 수 있게 해주는 도구입니다. 이 도구는 Large Language Model (LLM)이 데이터를 조회하고 결과를 도출할 때, 지정된 스키마에 맞게 JSON 형식으로 데이터를 반환할 수 있도록 설계되었습니다.

LLM이 데이터를 정확하고 효율적으로 처리하여 사용자가 원하는 형태의 JSON을 생성하기 위해서는, 모델의 용량(예: 인텔리전스)이 충분히 커야 합니다. 예를 들어, llama-70B 모델은 llama-8B 모델보다 더 큰 용량을 가지고 있어 보다 복잡한 데이터를 처리하는 데 유리합니다.

**[참고]**

`JSON (JavaScript Object Notation)` 은 데이터를 저장하고 구조적으로 전달하기 위해 사용되는 경량의 데이터 교환 포맷입니다. 웹 개발에서 매우 중요한 역할을 하며, 서버와 클라이언트 간의 통신을 위해 널리 사용됩니다. JSON은 읽기 쉽고, 기계가 파싱하고 생성하기 쉬운 텍스트를 기반으로 합니다.

JSON의 기본 구조
JSON 데이터는 이름(키)과 값의 쌍으로 이루어져 있습니다. 여기서 "이름"은 문자열이고, "값"은 다양한 데이터 유형일 수 있습니다. JSON은 두 가지 기본 구조를 가집니다:

- 객체: 중괄호 {}로 둘러싸인 키-값 쌍의 집합입니다. 각 키는 콜론 :을 사용하여 해당하는 값과 연결되며, 여러 키-값 쌍은 쉼표 ,로 구분됩니다.
- 배열: 대괄호 []로 둘러싸인 값의 순서 있는 목록입니다. 배열 내의 값은 쉼표 ,로 구분됩니다.

```json
{
  "name": "John Doe",
  "age": 30,
  "is_student": false,
  "skills": ["Java", "Python", "JavaScript"],
  "address": {
    "street": "123 Main St",
    "city": "Anytown"
  }
}
```

### PandasDataFrameOutputParser

**Pandas DataFrame**은 Python 프로그래밍 언어에서 널리 사용되는 데이터 구조로, 데이터 조작 및 분석을 위한 강력한 도구입니다. DataFrame은 구조화된 데이터를 효과적으로 다루기 위한 포괄적인 도구 세트를 제공하며, 이를 통해 데이터 정제, 변환 및 분석과 같은 다양한 작업을 수행할 수 있습니다.

이 **출력 파서**는 사용자가 임의의 Pandas DataFrame을 지정하여 해당 DataFrame에서 데이터를 추출하고, 이를 형식화된 사전(dictionary) 형태로 조회할 수 있게 해주는 LLM(Large Language Model) 기반 도구입니다.

### DatetimeOutputParser

`DatetimeOutputParser` 는 LLM의 출력을 `datetime` 형식으로 파싱하는 데 사용할 수 있습니다.

### EnumOutputParser

LangChain의 EnumOutputParser는 언어 모델의 출력을 미리 정의된 열거형(Enum) 값 중 하나로 파싱하는 도구입니다. 이 파서의 주요 특징과 사용법은 다음과 같습니다.

- 주요 특징

  - **열거형 파싱**: 문자열 출력을 미리 정의된 Enum 값으로 변환합니다.
  - **타입 안전성**: 파싱된 결과가 반드시 정의된 Enum 값 중 하나임을 보장합니다.
  - **유연성**: 공백이나 줄바꿈 문자를 자동으로 처리합니다.

- 사용 방법

EnumOutputParser는 언어 모델의 출력에서 유효한 Enum 값을 추출하는 데 유용합니다. 이를 통해 출력 데이터의 일관성을 유지하고 예측 가능성을 높일 수 있습니다. 파서를 사용하려면, 미리 정의된 Enum 값을 설정하고 해당 값을 기준으로 문자열 출력을 파싱합니다.

### OutputFixingParser

`OutputFixingParser`는 출력 파싱 과정에서 발생할 수 있는 오류를 자동으로 수정하는 기능을 제공합니다. 이 파서는 기본적으로 다른 파서, 예를 들어 `PydanticOutputParser` 를 래핑하고, 이 파서가 처리할 수 없는 형식의 출력이나 오류를 반환할 경우, 추가적인 LLM 호출을 통해 오류를 수정하도록 설계되었습니다.

이러한 접근 방식의 핵심은, 첫 번째 시도에서 스키마를 준수하지 않는 결과가 나올 경우, `OutputFixingParser` 가 자동으로 형식이 잘못된 출력을 인식하고, 이를 수정하기 위한 새로운 명령어와 함께 모델에 다시 제출한다는 것입니다. 이 과정에서, 수정을 위한 명령어는 오류를 정확히 지적하고, 올바른 형식으로 데이터를 재구성할 수 있도록 구체적인 지시를 포함해야 합니다.

예를 들어, `PydanticOutputParser` 를 사용하여 특정 데이터 스키마를 준수하는 출력을 생성하려고 했지만, 일부 필드가 누락되었거나 데이터 유형이 잘못된 경우가 발생할 수 있습니다. 이때 `OutputFixingParser` 는 다음 단계로, 해당 오류를 수정하는 지시를 포함한 새로운 요청을 LLM에 제출합니다. LLM은 이 지시를 바탕으로 오류를 수정한 새로운 출력을 생성하게 됩니다.
