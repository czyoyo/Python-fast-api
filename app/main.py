from datetime import datetime
from typing import List, Union, Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Movie(BaseModel):
    mid: int
    genre: str
    rate: Union[int, float]
    tag: Optional[str] = None
    date: Optional[datetime] = None
    some_variable_list: List[int] = []




tmp_data = {
    'mid': '1',
    'genre': 'action',
    'rate': 9.0,
    'tag': None,
    'date': '2024-01-03 00:00:00',
}
tmp_movie = Movie(**tmp_data)
print(tmp_movie)


@app.get("/")
def read_root():
    return tmp_data
