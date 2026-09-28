from philh_myftp_biz.json import Dict
from philh_myftp_biz.file import JSON
from fastapi import APIRouter
from ... import User

router = APIRouter(
    prefix = '/Apps/Bookmark'
)

class BookmarkData(Dict[str]):

    def __init__(self, user:User) -> None:

        _json = JSON(user.Dir.child('Apps__Bookmark.json'))

        super().__init__(_json)

@router.get("/read")
async def _(
    username: str,
    token: str,
    x: str
) -> str: # pyright: ignore[reportReturnType]
    """Read User Bookmark Data"""
    
    user = User(username)

    if user.checkAuth(token):

        data = BookmarkData(user)

        if data[x] is None:
            return ''
        else:
            return data[x] # pyright: ignore[reportReturnType]
     
@router.get("/save")
async def read_item(
    username: str,
    token: str,
    x: str,
    value: str
) -> None:
    """Write User Bookmark Data"""
    
    user = User(username)

    if user.checkAuth(token):
        
        data = BookmarkData(user)

        data[x] = value
