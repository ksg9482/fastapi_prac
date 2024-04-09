from typing import List, Set, Union
from pydantic import BaseModel, Field

# Pydantic 모델의 각 어트리뷰트는 타입을 갖는다.
# 해당 타입 자체로 또다른 Pydantic 모델의 타입이 될 수 있다.
# 특정한 어트리뷰트의 이름, 타입, 검증을 사용하여 깊게 중첩된 JSON "객체"를 선언할 수 있음
class Image(BaseModel):
    url: str
    name: str

    def update_name(self, name):
        self.name = name

class Item(BaseModel):
    name: str
    # Field를 이용하면 모델 내에서 검증과 메타데이터를 선언할 수 있음
    description: str|None = Field(
        default=None, 
        title="The description of the item", max_length=300
    )
    price: float
    tax: float|None = None
    # tags: List[str] = []
    tags: Set[str] = set() # tag는 중복되면 안된다는 조건을 추가하면 이렇게
    image: Union[List[Image], None] = None

"""
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
"""