import sys
import unittest
from datetime import datetime, timedelta
from dc_api import API
# Check version info
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    class Test(unittest.IsolatedAsyncioTestCase):
        def setUp(self):
            pass
        async def asyncSetUp(self):
            self.api = API()
        async def asyncTearDown(self):
            await self.api.close()
        async def test_async_with(self):
            async with API() as api:
                doc = api.board(board_id='aoegame', num=1).__anext__()
                self.assertNotEqual(doc, None)
        async def test_read_minor_board_one(self):
            async for doc in self.api.board(board_id='aoegame', num=1):
                for attr in doc.__slots__:
                    if attr == 'subject': continue
                    val = getattr(doc, attr)
                    self.assertNotEqual(val, None, attr)
                    self.assertNotEqual(val, '', attr)
                self.assertGreater(doc.time, datetime.now() - timedelta(hours=1))
                self.assertLess(doc.time, datetime.now() + timedelta(hours=1))
        async def test_read_minor_board_many(self):
            count = 0
            async for doc in self.api.board(board_id='aoegame', num=201):
                for attr in doc.__slots__:
                    if attr == 'subject': continue
                    val = getattr(doc, attr)
                    self.assertNotEqual(val, None, attr)
                    self.assertNotEqual(val, '', attr)
                count += 1
                self.assertGreater(doc.time, datetime.now() - timedelta(hours=1))
                self.assertLess(doc.time, datetime.now() + timedelta(hours=1))
            self.assertAlmostEqual(count, 201)
        async def test_read_major_comment(self):
            comms = ' '.join([str(comm) async for comm in self.api.comments(board_id='programming', document_id=1847628)])
            self.assertEqual(comms, 'ㄴ ㅇㅇ(112.172): 뭐하러일함  - dc App | 2021-08-21 12:28:00 ㄴ ㅇㅇ(39.121): 나였으면 뒤질때까지 디씨질만 함 | 2021-08-21 12:32:00 ㄴㄴ ㅇㅇ(202.150): 심심한 인생 | 2021-08-21 12:40:00 ㄴㄴ ㅇㅇ(39.121): 난 디씨질이 세상에서 젤 재밌어 | 2021-08-21 12:42:00 ㄴ ㅇㅇ(202.150): 저건 그냥 부자인데 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ | 2021-08-21 12:45:00')
        async def test_read_minor_recent_comments(self):
            async for doc in self.api.board(board_id='aoegame'):
                comments = [comm async for comm in doc.comments()]
                if not comments: continue
                for comm in comments:
                    for attr in comm.__slots__:
                        if attr in ['contents', 'dccon', 'voice', 'author_id']: continue
                        val = getattr(comm, attr)
                        self.assertNotEqual(val, None, attr)
                        self.assertNotEqual(val, '', attr)
                    self.assertNotEqual(comm.contents or comm.dccon or comm.voice, None)
                    self.assertGreater(comm.time, datetime.now() - timedelta(hours=1))
                    self.assertLess(comm.time, datetime.now() + timedelta(hours=1))
                break
        async def test_read_board_one(self):
            async for doc in self.api.board(board_id='programming', num=1):
                for attr in doc.__slots__:
                    if attr == 'subject': continue
                    val = getattr(doc, attr)
                    self.assertNotEqual(val, None, attr)
                    self.assertNotEqual(val, '', attr)
                self.assertGreater(doc.time, datetime.now() - timedelta(hours=24))
                self.assertLess(doc.time, datetime.now() + timedelta(hours=1))
        async def test_read_board_many(self):
            count = 0
            async for doc in self.api.board(board_id='programming', num=201):
                for attr in doc.__slots__:
                    if attr == 'subject': continue
                    val = getattr(doc, attr)
                    self.assertNotEqual(val, None, attr)
                    self.assertNotEqual(val, '', attr)
                count += 1
                self.assertGreater(doc.time, datetime.now() - timedelta(hours=24))
                self.assertLess(doc.time, datetime.now() + timedelta(hours=1))
            self.assertAlmostEqual(count, 201)
        async def test_read_recent_comments(self):
            async for doc in self.api.board(board_id='aoegame'):
                comments = [comm async for comm in doc.comments()]
                if not comments: continue
                for comm in comments:
                    for attr in comm.__slots__:
                        if attr in ['contents', 'dccon', 'voice', 'author_id']: continue
                        val = getattr(comm, attr)
                        self.assertNotEqual(val, None, attr)
                        self.assertNotEqual(val, '', attr)
                    self.assertNotEqual(comm.contents or comm.dccon or comm.voice, None)
                    self.assertGreater(comm.time, datetime.now() - timedelta(hours=24))
                    self.assertLess(comm.time, datetime.now() + timedelta(hours=1))
                break
        async def test_minor_document(self):
            doc = await (await self.api.board(board_id='aoegame', num=1).__anext__()).document()
            self.assertNotEqual(doc, None)
            for attr in doc.__slots__:
                if attr in ['author_id', 'subject']: continue
                val = getattr(doc, attr)
                self.assertNotEqual(val, None, attr)
                self.assertNotEqual(val, '', attr)
            self.assertGreater(doc.time, datetime.now() - timedelta(hours=1))
            self.assertLess(doc.time, datetime.now() + timedelta(hours=1))
        async def test_document(self):
            doc = await (await self.api.board(board_id='programming', num=1).__anext__()).document()
            self.assertNotEqual(doc, None)
            for attr in doc.__slots__:
                if attr in ['author_id', 'subject']: continue
                val = getattr(doc, attr)
                self.assertNotEqual(val, None, attr)
            self.assertGreater(doc.time, datetime.now() - timedelta(hours=1))
            self.assertLess(doc.time, datetime.now() + timedelta(hours=1))
        '''
        async def test_write_mod_del_document_comment(self):
            board_id='programming'
            doc_id = await self.api.write_document(board_id=board_id, title="제목", contents="내용", name="닉네임", password="비밀번호")
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            self.assertEqual(doc.contents, "내용")
            doc_id = await self.api.modify_document(board_id=board_id, document_id=doc_id, title="수정된 제목", contents="수정된 내용", name="수정된 닉네임", password="비밀번호")
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            self.assertEqual(doc.contents, "수정된 내용")
            comm_id = await self.api.write_comment(board_id=board_id, document_id=doc_id, contents="댓글", name="닉네임", password="비밀번호")
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            comm = await doc.comments().__anext__()
            self.assertEqual(comm.contents, "댓글")
            await self.api.remove_document(board_id=board_id, document_id=doc_id, password="비밀번호")
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            self.assertEqual(doc, None)
        async def test_minor_write_mod_del_document_comment(self):
            board_id='stick'
            doc_id = await self.api.write_document(board_id=board_id, title="제목", contents="내용", name="닉네임", password="비밀번호", is_minor=True)
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            self.assertEqual(doc.contents, "내용")
            doc_id = await self.api.modify_document(board_id=board_id, document_id=doc_id, title="수정된 제목", contents="수정된 내용", name="수정된 닉네임", password="비밀번호", is_minor=True)
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            self.assertEqual(doc.contents, "수정된 내용")
            comm_id = await self.api.write_comment(board_id=board_id, document_id=doc_id, contents="댓글", name="닉네임", password="비밀번호")
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            comm = await doc.comments().__anext__()
            self.assertEqual(comm.contents, "댓글")
            await self.api.remove_document(board_id=board_id, document_id=doc_id, password="비밀번호")
            doc = await self.api.document(board_id=board_id, document_id=doc_id)
            self.assertEqual(doc, None)
        '''

if __name__ == "__main__":
    unittest.main()
