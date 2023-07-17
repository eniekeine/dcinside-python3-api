# 글에 달린 댓글을 나타내는 클래스
class Comment:
    __slots__ = ["id", "is_reply", "author", "author_id", "contents", "dccon", "voice", "time"]
    def __init__(self, id, is_reply, author, author_id, contents, dccon, voice, time):
        # 댓글 ID
        self.id = id
        # 다른 댓글에 대한 답변인가?
        self.is_reply = is_reply
        # 작성자 이름
        self.author = author
        # 작성자 ID
        self.author_id = author_id
        # 댓글 내용
        self.contents = contents
        # 디씨콘
        self.dccon = dccon
        # 보이스 리플
        self.voice = voice
        # 시간
        self.time = time
    def __str__(self):
        return f"ㄴ{'ㄴ' if self.is_reply else ''} {self.author}: {self.contents or ''}{self.dccon or ''}{self.voice or ''} | {self.time}"
