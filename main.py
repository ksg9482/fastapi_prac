"""
uvicorn main:app --reload --host=0.0.0.0 --port=8080
"""
from typing import Annotated, List, Optional, Union
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel
from Item import Item
from User import User
from model_name_enum import ModelName

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # 타입 선언하면 자동으로 파싱한다
    # int로 변환 안되면 타입 에러 발생
    # 어느 지점에서 에러가 발생했는지 알려준다 
    # 모든 데이터 검증은 pydantic이 처리한다
    """
    "loc": [
                "path",
                "item_id"
            ]
    path의 item_id에서 에러가 발생
    """
    return {"item_id": item_id}

# 경로 작동은 순차적으로 실행. 먼저 실행되기 원하는 라우터가 상단에 위치해야 한다
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# Enum 사용. 열거형은 파이썬 3.4 이상에서 사용 가능
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.cal:
        return {"model_name": model_name, "message": "cal is caluculator`s cal"}
    
    if model_name == "lin":
        return {"model_name": model_name, "message": "lin is linear regression`s lin"}
    
    return {"model_name": model_name,  "message": "Hmm... I don't know"}

# 경로 매캐변수의 일부가 아닌 다른 함수 매개변수를 선언하면 쿼리 매개변수로 자동 해석.
@app.get("/items/") # /유무로 다른 경로. 보통 하나로 취급해 바꿔주던데 fastapi는 아닌가보네?
async def read_item(skip:int=0, limit:int=10): # 중요한건 RUL의 일부이므로 문자열이라는 것. 타입을 선언하면 해당 타입으로 변환 및 검증된다.
    return fake_items_db[skip:skip + limit] # 배열 자르기. skip부터 skip + limit까지 자른다. 0~9인덱스.

@app.get("/items/{item_id}")
async def read_item(item_id:str, q:Optional[str]=None, short:bool=False): # 기본값을 주지 않으면 required로 간주한다.
    # Union[str, None] == Optional[str]
    item = {'item_id': item_id}
    if q:
        item.update({'q': q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
"""
파이썬의 기본(built-in) 오브젝트 중 Falsy 오브젝트
False
None
0, 0.0, 0L, 0j
""
[]
()
{}

이 외의 모든 기본 오브젝트는 Truthy 오브젝트
"""

# pydantic의 BaseModel을 상속받은 클래스. request dto 같은 느낌
@app.post("/items")
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def update_item(item_id:int, item:Item):
    return {"item_id": item_id, **item.dict()} # **는 dict를 풀어서 전달한다. dict()는 모델의 모든 필드를 가져온다.


# 쿼리 매개변수와 문자열 검증
@app.get("/items/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
"""
q는 optional 자료형. None이 가능하기 때문에 필수가 아니며, fastapi는 그것을 안다.
기본값 None을 탐지하고 옵셔널임을 탐지. optional은 fastapi가 사용하는게 아니지만 편집기에게 지원과 오류탐지를 제공하게 해준다
"""

# 추가검증
@app.get("/items/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=3, max_length=50, pattern="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
"""
Query를 매개변수의 기본값으로 사용. Query는 더 많은 매개변수를 전달한다. 
매개변수와 일치해야 하는 정규표현식을 정의할 수 도 있음
"""
# 기본값은 매개변수를 선택적으로 만든다.
# Query를 필수값으로 만드려면 첫번째 인자로 ...전달하기. ...는 파이썬의 내장 상수로 Ellipsis라 부른다.(보통 배열을 슬라이싱할 때 사용)

# 쿼리 매개변수를 Query와 함게 명시적으로 선언 할 때, 여러 값을 받는 법
@app.get("/items/")
async def read_items(q: Union[List[str], None]=Query(default=None)):
    # http://localhost:8000/items/?q=foo&q=bar q여러번 사용 -> 리스트로 받음
    query_items = {"q": q}
    return query_items

@app.get("/items/")
async def read_items(q: List[str] = Query(default=["foo", "bar"])):
    # http://localhost:8000/items/ default를 리스트로 지정
    query_items = {"q": q}
    return query_items


# 메타데이터 선언 -> 추가예시. api 문서화에 사용
@app.get("/items2/meta")
async def read_items(
    q: Union[str, None] = Query(
        default=None, 
        title="Query string", 
        description="Query string for the items to search in the database that have a good match",
        min_length=3
        ),
):
    print("call")
    print(q)
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 별칭 사용
@app.get("/items2/alias")
async def read_items(
    q: Union[str, None] = Query(
        default=None, 
        # 매개변수는 유효한 파이썬 변수명이여야 한다. 하지만 HTTP와 다를경우 alias를 통해 매핑할 수 있다. 
        # ?item-query=foobaritems -> item-query라는 이름으로 전송하면 q로 받는다.
        alias="item-query"
        # deprecated=True # 설정하면 API Docs에 deprecated 표시가 된다.
        ),
):
    print("call")
    print(q)
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

"""
Query, Path 등을 임포트 할 때, 이것들은 실제로 함수.
호출되면 동일한 이름의 클래스의 인스턴스를 반환.
편집기에서 타입에 대한 오류를 표시하지 않도록
오류를 무시하기 위한 사용자 설정을 추가하지 않고도 일반 편집기와 코딩 도구를 사용할 수 있음
"""

# 다중 본문 매개변수
@app.put("/items3/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

# Body
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, importance: int = Body()):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results
"""
단일 값을 그대로 선언한다면, FastAPI는 쿼리 매개변수로 가정.
하지만 Body()를 사용하면 본문 키로 처리하도록 제어.
"""
@app.put("/items4/{item_id}")
async def update_item(item_id:int, item: Annotated[Item, Body(embed=True)]): #Annotated 사용 -> Body의 추가적인 메타데이터를 제공
    results = {"item_id": item_id, "item": item}
    item.image.update_name()
    return results

# 요청 예제 데이터 선언
