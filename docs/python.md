# Python

## inheritance VS mixin

1. 개념적 차이

```python
# 일반 상속 - "is-a" 관계
class Animal:
    def breathe(self):
        pass

class Dog(Animal):  # 개는 동물이다
    pass

# Mixin - 부가 기능 제공
class SwimMixin:
    def swim(self):
        print("수영할 수 있음")

class Dog(Animal, SwimMixin):  # 개는 동물이며, 수영 기능을 추가
    pass
```

2. Mixin의 특징

- 단독으로 인스턴스화하지 않음
- 상태(state)를 가지지 않음
- 특정 기능만 제공

````python
class JsonSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

# Mixin은 단독으로 사용하지 않음
# wrong_usage = JsonSerializableMixin()  # 이렇게 사용하지 않음
```

3. 실제 사용 예시

```python
class JsonSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LoggableMixin:
    def log(self, message):
        print(f"Log: {message}")

class User(JsonSerializableMixin, LoggableMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

# 사용
user = User("John", 30)
print(user.to_json()) # JSON 직렬화 기능 사용
user.log("User created") # 로깅 기능 사용
```

4. 주요 차이점 요약

- 일반 상속:
  - is-a 관계
  - 계층 구조 형성
  - 상태와 동작 모두 상속
- Mixin:
  - 부가 기능 제공
  - 독립적인 기능 단위
  - 상태 없이 동작만 정의
  - 다중 기능 조합 용이

이러한 차이로 인해 Mixin은 코드 재사용과 기능 확장에 더 유연한 방식을 제공합니다.

````
