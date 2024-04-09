from enum import Enum

# str, Enum을 상속
# str을 상속함으로써 API문서는 값이 문자열 형이여야 함을 알게된다.
class ModelName(str, Enum):
    cal = "cal"
    lin = "lin"
    raven = "raven"

