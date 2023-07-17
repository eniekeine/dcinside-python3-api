class DocumentIndex:
    __slots__ = ["id", "subject", "title", "board_id", "has_image", "author", "time", "view_count", "comment_count", "voteup_count", "document", "comments", "image_available"]
    def __init__(self, id, board_id, title, has_image, author, time, view_count, comment_count, voteup_count, document, comments, subject, image_available):
        self.id = id
        self.board_id = board_id
        self.title = title
        self.has_image = has_image
        self.author = author
        self.time = time
        self.view_count = view_count
        self.comment_count = comment_count
        self.voteup_count = voteup_count
        self.document = document
        self.comments = comments
        self.subject = subject
        self.image_available = image_available
    def __str__(self):
        return f"{self.subject or ''}\t|{self.id}\t|{self.time.isoformat()}\t|{self.author}\t|{self.title}({self.comment_count}) +{self.voteup_count}"