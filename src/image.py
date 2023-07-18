import filetype
from src.header import Header
class Image:
    __slots__ = ["src", "document_id", "board_id", "session"]
    def __init__(self, src, document_id, board_id, session):
        """
        Image 클래스를 초기화한다.

        Args:
            src (str) : 이미지 파일 주소
            document_id (int) : 게시글 ID
            board_id (int) : 갤러리 ID
            session (aiohttp.ClientSession) : 디시인사이드 서버와의 HTTP 연결 세션
        """
        self.src = src
        self.document_id = document_id
        self.board_id = board_id
        self.session = session
    async def load(self):
        """
        게시글에 포함된 이미지를 로딩한다.
        어느 갤러리의 어느 게시글인가는 `self.board_id`, `self.document_id`로 판단한다.
        """
        headers = Header.GET_HEADERS.copy()
        headers["Referer"] = "https://m.dcinside.com/board/{}/{}".format(self.board_id, self.document_id)
        async with self.session.get(self.src, cookies=Header.GALLERY_POSTS_COOKIES, headers=headers) as res:
            return await res.read()
    async def download(self, path):
        """
        게시글에 포함된 이미지를 다운롤드한다.
        어느 갤러리의 어느 게시글인가는 `self.board_id`, `self.document_id`로 판단한다.
        """
        headers = Header.GET_HEADERS.copy()
        headers["Referer"] = "https://m.dcinside.com/board/{}/{}".format(self.board_id, self.document_id)
        async with self.session.get(self.src, cookies=Header.GALLERY_POSTS_COOKIES, headers=headers) as res:
            bytes = await res.read()
            ext = filetype.guess(bytes).extension
            with open(path + '.' + ext, 'wb') as f:
                f.write(bytes)
