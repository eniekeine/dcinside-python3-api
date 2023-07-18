import asyncio
import dc_api

async def run():
  api = dc_api.API()

  # 댓글 작성
  await api.write_comment(board_id="programming", doc_id=149123, name="ㅇㅇ", password="1234", contents="ㅇㅈ")

  # 글 작성
  doc_id = await api.write_document(board_id="programming", title="java vs python", contents="닥치고 자바", name="ㅇㅇ", password="1234")

  # 글 삭제
  await api.remove_document(board_id="programming", doc_id=doc_id, password="1234")

  # 마이너갤 글 작성
  doc_id = await api.write_document(board_id="aoegame", title="java vs python", contents="닥치고 자바", name="ㅇㅇ", password="1234", is_minor=True)

  await api.close()

asyncio.run(run())