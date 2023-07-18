from typing import Union
from datetime import datetime
# 글에 달린 댓글을 나타내는 클래스
class Comment:
    __slots__ = ["id", "is_reply", "author", "author_id", "contents", "dccon", "voice", "time"]
    def __init__(
            self, 
            id : str, 
            is_reply : bool, 
            author : str, 
            author_id : Union[str,None], 
            contents : str, 
            dccon : Union[str,None], 
            voice : Union[str,None], 
            time : int
            ):
        """
        Args:
            id: 댓글 ID
            is_reply: 다른 댓글에 대한 답변인가?
            author: 작성자 이름
            author_id: 작성자 ID
            contents: 댓글 내용
            dccon: 디씨콘
            voice: 보이스 리플
            time: 시간
        """
        self.id = id
        self.is_reply = is_reply
        self.author = author
        self.author_id = author_id
        self.contents = contents
        self.dccon = dccon
        self.voice = voice
        self.time = time

        print("id", type(id))
        print("is_reply", type(is_reply))
        print("author", type(author))
        print("author_id", type(author_id))
        print("contents", type(contents))
        print("dccon", type(dccon))
        print("voice", type(voice))
        print("time", type(time))

    def __str__(self):
        return f"ㄴ{'ㄴ' if self.is_reply else ''} {self.author}: {self.contents or ''}{self.dccon or ''}{self.voice or ''} | {self.time}"
