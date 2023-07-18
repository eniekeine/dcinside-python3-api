# 프로그래밍 갤러리 글 무한 크롤링
import asyncio
import dc_api

async def run():
  async with dc_api.API() as api:
    async for index in api.board(board_id="programming"):
        print(index.title)            # => 땔감 벗어나는법.tip
        doc = await index.document()
        print(doc.contents)           # => 자바를 한다
        for img in doc.images:
          img.download('./img')       # => ./img.gif
        async for comm in index.comments():
            print(com.contents)       # => ㅇㅇ(1.224) 지랄 ㄴ

asyncio.run(run())
