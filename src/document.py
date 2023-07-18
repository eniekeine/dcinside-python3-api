from typing import Union
from src.image import Image
import datetime
from asyncio import coroutine
class Document:
    """
    게시글을 나타내는 클래스
    """
    __slots__ = ["id", "board_id", "title", "author", "author_id", "contents", "images", "html", "view_count", "voteup_count", "votedown_count", "logined_voteup_count", "time", "subject", "comments"]
    """
    Args:
        id : 문서 id
        board_id : 갤러리 id
        title : 게시글 제목
        author : 게시글 작성자
        author_id : 게시글 작성자 ID
        contents : HTML 태그를 제외한 게시글의 내용
        images : 게시글에 포함된 이미지의 리스트. 리스트의 각 아이템은 Image 클래스이다.
        html : 게시글의 내용
        view_count : 조회수
        voteup_count : 추천수
        votedown_count : 비추천수
        logined_voteup_count : 고닉 추천수
        time : 게시글의 게시일
        comments : 게시글의 댓글
        subject : 주제
    """
    def __init__(
            self, 
            id : int, 
            board_id : int, 
            title : str, 
            author : str, 
            author_id : Union[None, str], 
            contents : str, 
            images : list[Image], 
            html : str, 
            view_count : int, 
            voteup_count : int, 
            votedown_count : int, 
            logined_voteup_count : int, 
            time : datetime.time, 
            comments : list[coroutine], 
            subject : Union[None, str] = None):
        self.id = id
        self.board_id = board_id
        self.title = title
        self.author = author
        self.author_id = author_id
        self.contents = contents
        self.images = images
        self.html = html
        self.view_count = view_count
        self.voteup_count = voteup_count
        self.votedown_count = votedown_count
        self.logined_voteup_count = logined_voteup_count
        self.comments = comments
        self.time = time
        self.subject = subject
    def __str__(self):
        return f"{self.subject or ''}\t|{self.id}\t|{self.time.isoformat()}\t|{self.author}\t|{self.title}({self.comment_count}) +{self.voteup_count} -{self.votedown_count}\n{self.contents}"
