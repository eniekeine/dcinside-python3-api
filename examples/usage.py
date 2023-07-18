import asyncio
import dc_api

api = dc_api.API()

async def main():
    async for index in api.board(board_id="programming", num=-1, start_page=1, document_id_upper_limit=None, document_id_lower_limit=None):
        index.id         # => 835027
        index.board_id   # => programming
        index.title      # => "땔감 벗어나는법.tip"
        index.author     # => "ㅇㅇ(10.20)"
        index.time       # => datetime("2020-01-01 01:41:00.000000")
        index.comment_count # => 3
        index.voteup_count  # => 0
        index.view_count    # => 14

        doc = await index.document()
        doc.id         # => 835027
        doc.board_id   # => "programming"
        doc.title      # => "땔감 벗어나는법.tip"
        doc.author     # => "ㅇㅇ(10.20)"
        doc.author_id  # => None (고닉일 경우 고닉 아이디 반환)
        doc.time       # => datetime("2020-01-01 01:41:00.000000")
        doc.comment_count   # => 3
        doc.voteup_count    # => 0
        doc.logined_voteup_count  # => 0
        doc.votedown_count  # => 0
        doc.view_count # => 14.id
        doc.contents   # => "자바를 한다"
        doc.html       # => "<p> 자바를 한다 </p>" 

        for image in doc.images:
            image.src         # => "https://..."
            image.document_id # => 835027
            image.board_id    # => "programming"
            await image.load()# => raw image binary
            await image.download(path) # => download image to local path(automatically add ext)

        async for com in index.comments():
            com.id            # => 123123
            com.is_reply      # => False
            com.time          # => "1:55"
            com.author        # => "ㅇㅇ(192.23)"
            com.author_id     # => None (고닉일 경우 아이디 반환)
            com.contents      # => "개솔 ㄴㄴ"
            com.dccon         # => None (디시콘일경우 디시콘 주소 반환)
            com.voice         # => None (보이스리플일경우 보이스리플 주소 반환)

            
    doc = await api.document(board_id="programming", document_id=835027)

    async for comm in api.comments(board_id="programming", document_id=835027):
        comm


    doc_id = await api.write_document(board_id="programming",
                                name="점진적자살", password="1234", 
                                title="제목", contents="내용", is_minor=False)
    doc_id = await api.modify_document(board_id="programming", document_id=doc_id, 
                            name="얄파고", pw="1234", 
                            title="수정된 제목", contents="수정된 내용", is_minor=False)
    com_id = await api.write_comment(board_id="programming", document_id=doc_id, 
                            name="점진적자살", password="1234", contents="설리")
    await api.remove_document(board_id="programming", document_id=com_id, password="1234")

asyncio.run(main())
