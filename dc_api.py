import json
import lxml.html
import aiohttp
from .src.document import Document
from .src.document_index import DocumentIndex
from .src.comment import Comment
from .src.image import Image
from .src.header import Header
from .utils.helper_function import quote, unquote, parse_time
"""
dcinside 웹을 파이선 코드로 사용하기 위한 API입니다.
"""
class API:
    def __init__(self):
        self.session = aiohttp.ClientSession(
            headers=Header.GET_HEADERS, 
            cookies=Header.GOOGLE_ANALYTIC_COOKIES
        )
    async def close(self):
        await self.session.close()
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args, **kwargs):
        await self.close()
    async def watch(self, board_id):
        pass
    async def gallery(self, name=None):
        url = "https://m.dcinside.com/galltotal"
        gallerys={}
        async with self.session.get(url) as res:
            text = await res.text()
            parsed = lxml.html.fromstring(text)
        for i in parsed.xpath('//*[@id="total_1"]/li'):
            for e in i.iter():
                if e.tag == "a":
                    board_name = e.text
                    board_id = e.get("href").split("/")[-1]
                    if name:
                        if name in board_name:
                            gallerys[board_name] = board_id
                    else:
                        gallerys[board_name] = board_id
        return gallerys
    async def board(self, board_id, num=-1, start_page=1, recommend=False, document_id_upper_limit=None, document_id_lower_limit=None, is_minor=False):
        page = start_page
        while num:
            if recommend: # 개념글
                url = "https://m.dcinside.com/board/{}?recommend=1&page={}".format(board_id, page)
            else:
                url = "https://m.dcinside.com/board/{}?page={}".format(board_id, page)
            async with self.session.get(url) as res:
                text = await res.text()
                parsed = lxml.html.fromstring(text)
            doc_headers = (i[0] for i in parsed.xpath("//ul[contains(@class, 'gall-detail-lst')]/li") if not i.get("class", "").startswith("ad"))
            for doc in doc_headers:
                document_id = doc[0].get("href").split("/")[-1].split("?")[0]
                if document_id_upper_limit and int(document_id_upper_limit) <= int(document_id): continue
                if document_id_lower_limit and int(document_id_lower_limit) >= int(document_id): return
                if len(doc[0][1]) == 5:
                    subject = doc[0][1][0].text
                    author = doc[0][1][1].text
                    time= parse_time(doc[0][1][2].text)
                    view_count= int(doc[0][1][3].text.split()[-1])
                    voteup_count= int(doc[0][1][4][0].text.split()[-1])
                else:
                    subject = None
                    author = doc[0][1][0].text
                    time= parse_time(doc[0][1][1].text)
                    view_count= int(doc[0][1][2].text.split()[-1])
                    voteup_count= int(doc[0][1][3].text_content().split()[-1])
                if "sp-lst-img" in doc[0][0][0].get("class"):
                    image_available = True
                else:
                    image_available = False
                title = doc[0][0][1].text
                indexdata = DocumentIndex(
                    id= document_id,
                    board_id=board_id,
                    title= title,
                    has_image= doc[0][0][0].get("class").endswith("img"),
                    author= author,
                    view_count= view_count,
                    voteup_count= voteup_count,
                    comment_count= int(doc[1][0].text),
                    document= lambda: self.document(board_id, document_id),
                    comments= lambda: self.comments(board_id, document_id),
                    time= time,
                    subject=subject,
                    image_available=image_available
                    )
                yield(indexdata)
                num-=1
                if num==0: 
                    break
            if not doc_headers: 
                break
            else: 
                page+=1
    async def document(self, board_id, document_id):
        url = "https://m.dcinside.com/board/{}/{}".format(board_id, document_id)
        async with self.session.get(url) as res:
            text = await res.text()
            parsed = lxml.html.fromstring(text)
        doc_content_container = parsed.xpath("//div[@class='thum-txtin']")
        doc_head_containers = parsed.xpath("//div[starts-with(@class, 'gallview-tit-box')]")
        if not len(doc_head_containers):
            return None
        doc_head_container = doc_head_containers[0]
        if len(doc_content_container):
            title = " ".join(doc_head_container[0].text.strip().split())
            if len(title) == 0: # 제목이 비어있는 경우 파싱을 포기합니다. <https://gall.dcinside.com/board/view/?id=programming&no=231191&page=1>
                return None
            if doc_head_container[1][0][0].text == None: # 작성자가 비어있는 경우 파싱을 포기합니다. <https://gall.dcinside.com/board/view/?id=programming&no=231896&page=1>
                return None
            author = doc_head_container[1][0][0].text.strip()
            author_id = None if len(doc_head_container[1]) <= 1 else doc_head_container[1][1][0].get("href").split("/")[-1]
            time = doc_head_container[1][0][1].text.strip()
            doc_content = parsed.xpath("//div[@class='thum-txtin']")[0]
            for adv in doc_content.xpath("div[@class='adv-groupin']"):
                adv.getparent().remove(adv)
            for adv in doc_content.xpath("div[@class='adv-groupno']"):
                adv.getparent().remove(adv)
            for adv in doc_content.xpath("//img"):
                if adv.get("src", "").startswith("https://nstatic") and not adv.get("data-original"):
                    adv.getparent().remove(adv)
            return Document(
                    id= document_id,
                    board_id = board_id,
                    title= title,
                    author= author,
                    author_id =author_id,
                    contents= '\n'.join(i.strip() for i in doc_content.itertext() if i.strip() and not i.strip().startswith("이미지 광고")),
                    images= [Image(
                        src=i.get("data-original", i.get("src")), 
                        board_id=board_id, 
                        document_id=document_id, 
                        session=self.session)
                        for i in doc_content.xpath("//img") 
                            if i.get("data-original") or (not i.get("src","").startswith("https://nstatic") and
                                not i.get("src", "").startswith("https://img.iacstatic.co.kr") and i.get("src"))],
                    html= lxml.html.tostring(doc_content, encoding=str),
                    view_count= int(parsed.xpath("//ul[@class='ginfo2']")[1][0].text.strip().split()[1]),
                    voteup_count= int(parsed.xpath("//span[@id='recomm_btn']")[0].text.strip().replace(',', '')), # 추천수가 1000을 넘어가는 경우 ,가 포함됨
                    votedown_count= int(parsed.xpath("//span[@id='nonrecomm_btn']")[0].text.strip().replace(',', '')), # 비추수가 1000을 넘어가는 경우 ,가 포함됨
                    logined_voteup_count= int(parsed.xpath("//span[@id='recomm_btn_member']")[0].text.strip()),
                    comments= lambda: self.comments(board_id, document_id),
                    time= parse_time(time)
                    )
        else:
            # fail due to unusual tags in mobile version
            # at now, just skip it
            return None
        ''' !TODO: use an alternative(PC) protocol to fetch document
        else:
            url = "https://gall.dcinside.com/{}?no={}".format(board_id, document_id)
            res = sess.get(url, timeout=TIMEOUT, headers=Header.ALTERNATIVE_GET_HEADERS)
            parsed = lxml.html.fromstring(res.text)
            doc_content = parsed.xpath("//div[@class='thum-txtin']")[0]
            return '\n'.join(i.strip() for i in doc_content.itertext() if i.strip() and not i.strip().startswith("이미지 광고")), [i.get("src") for i in doc_content.xpath("//img") if not i.get("src","").startswith("https://nstatic")], comments(board_id, document_id, sess=sess)
        '''
    async def comments(self, board_id, document_id, num=-1, start_page=1):
        url = "https://m.dcinside.com/ajax/response-comment"
        for page in range(start_page, 999999):
            payload = {"id": board_id, "no": document_id, "cpage": page, "managerskill":"", "del_scope": "1", "csort": ""}
            async with self.session.post(url, headers=Header.XML_HTTP_REQ_HEADERS, data=payload) as res:
                parsed = lxml.html.fromstring(await res.text())
            if not len(parsed[1].xpath("li")): break
            for li in parsed[1].xpath("li"):
                if not len(li[0]) or not li[0].text: continue
                yield Comment(
                    id= li.get("no"),
                    is_reply = "comment-add" in li.get("class", "").strip().split(),
                    author = li[0].text + ("{}".format(li[0][0].text) if li[0][0].text else ""),
                    author_id= li[0][1].get("data-info", None) if len(li[0]) > 1 else None,
                    contents= '\n'.join(i.strip() for i in li[1].itertext()),
                    dccon= li[1][0].get("data-original", li[1][0].get("src", None)) if len(li[1]) and li[1][0].tag=="img" else None,
                    voice= li[1][0].get("src", None) if len(li[1]) and li[1][0].tag=="iframe" else None,
                    time= parse_time(li[2].text))
                num -= 1
                if num == 0:
                    return
            page_num_els = parsed.xpath("span[@class='pgnum']")
            if page_num_els:
                p = page_num_els[0].itertext()
                next(p)
                if page == next(p)[1:]: 
                    break
            else: 
                break 
    async def write_comment(self, board_id, document_id, contents="", dccon_id="", dccon_src="", parent_comment_id="", name="", password="", is_minor=False):
        url = "https://m.dcinside.com/board/{}/{}".format(board_id, document_id)
        async with self.session.get(url) as res:
            parsed = lxml.html.fromstring(await res.text())
        hide_robot = parsed.xpath("//input[@class='hide-robot']")[0].get("name")
        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        title = parsed.xpath("//span[@class='tit']")[0].text.strip()
        board_name = parsed.xpath("//a[@class='gall-tit-lnk']")[0].text.strip()
        con_key = await self.__access("com_submit", url, require_conkey=False, csrf_token=csrf_token)
        header = Header.XML_HTTP_REQ_HEADERS.copy()
        header["Referer"] = url
        header["Host"] = "m.dcinside.com"
        header["Origin"] = "https://m.dcinside.com"
        header["X-CSRF-TOKEN"] = csrf_token
        cookies = {
            "m_dcinside_" + board_id: board_id,
            "m_dcinside_lately": quote(board_id + "|" + board_name + ","),
            "_ga": "GA1.2.693521455.1588839880",
            }
        url = "https://m.dcinside.com/ajax/comment-write"
        payload = {
                "comment_memo": contents,
                "comment_nick": name,
                "comment_pw": password,
                "mode": "com_write",
                "comment_no": parent_comment_id,
                "id": board_id,
                "no": document_id,
                "best_chk": "",
                "subject": title,
                "board_id": "0",
                "reple_id":"",
                "cpage": "1",
                "con_key": con_key,
                hide_robot: "1",
                }
        if dccon_id: payload["detail_idx"] = dccon_id
        if dccon_src: payload["comment_memo"] = "<img src='{}' class='written_dccon' alt='1'>".format(dccon_src)
        #async with self.session.post(url, headers=header, data=payload, cookies=cookies) as res:
        async with self.session.post(url, headers=header, data=payload, cookies=cookies) as res:
            parsed = await res.text()
        try:
            parsed = json.loads(parsed)
        except Exception as e:
            raise Exception("Error while writing comment: " + unquote(str(parsed)))
        if "data" not in parsed:
            raise Exception("Error while writing comment: " + unquote(str(parsed)))
        return str(parsed["data"])
    async def modify_document(self, board_id, document_id, title="", contents="", name="", password="", is_minor=False):
        if not password:
            url = "https://m.dcinside.com/write/{}/modify/{}".format(board_id, document_id)
            async with self.session.get(url) as res:
                return await self.__write_or_modify_document(board_id, title, contents, name, password, intermediate=await res.text(), intermediate_referer=url, document_id=document_id, is_minor=is_minor)
        url = "https://m.dcinside.com/confirmpw/{}/{}?mode=modify".format(board_id, document_id)
        referer = url
        async with self.session.get(url) as res:
            parsed = lxml.html.fromstring(await res.text())
        token = parsed.xpath("//input[@name='_token']")[0].get("value", "")
        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        con_key = await self.__access("Modifypw", url, require_conkey=False, csrf_token=csrf_token)
        payload = {
                "_token": token,
                "board_pw": password,
                "id": board_id,
                "no": document_id,
                "mode": "modify",
                "con_key": con_key,
                }
        header = Header.XML_HTTP_REQ_HEADERS.copy()
        header["Referer"] = referer
        header["Host"] = "m.dcinside.com"
        header["Origin"] = "https://m.dcinside.com"
        header["X-CSRF-TOKEN"] = csrf_token
        url = "https://m.dcinside.com/ajax/pwcheck-board"
        async with self.session.post(url, headers=header, data=payload) as res:
            res = await res.text()
            if not res.strip():
                Exception("Error while modifing: maybe the password is incorrect")
        payload = {
                "board_pw": password,
                "id": board_id,
                "no": document_id,
                "_token": csrf_token
                }
        header = Header.POST_HEADERS.copy()
        header["Referer"] = referer
        url = "https://m.dcinside.com/write/{}/modify/{}".format(board_id, document_id)
        async with self.session.post(url, headers=header, data=payload) as res:
            return await self.__write_or_modify_document(board_id, title, contents, name, password, intermediate=await res.text(), intermediate_referer=url, document_id=document_id)
    async def remove_document(self, board_id, document_id, password="", is_minor=False):
        if not password:
            url = "https://m.dcinside.com/board/{}/{}".format(board_id, document_id)
            async with self.session.get(url) as res:
                parsed = lxml.html.fromstring(await res.text())
            csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
            header = Header.XML_HTTP_REQ_HEADERS.copy()
            header["Referer"] = url
            header["X-CSRF-TOKEN"] = csrf_token
            con_key = await self.__access("board_Del", url, require_conkey=False, csrf_token=csrf_token)
            url = "https://m.dcinside.com/del/board"
            payload = { "id": board_id, "no": document_id, "con_key": con_key }
            async with self.session.post(url, headers=header, data=payload) as res:
                res = await res.text()
            if res.find("true") < 0:
                raise Exception("Error while removing: " + unquote(str(res)))
            return True
        url = "https://m.dcinside.com/confirmpw/{}/{}?mode=del".format(board_id, document_id)
        referer = url
        async with self.session.get(url) as res:
            parsed = lxml.html.fromstring(await res.text())
        token = parsed.xpath("//input[@name='_token']")[0].get("value", "")
        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        board_name = parsed.xpath("//a[@class='gall-tit-lnk']")[0].text.strip()
        con_key = await self.__access("board_Del", url, require_conkey=False, csrf_token=csrf_token)
        payload = {
                "_token": token,
                "board_pw": password,
                "id": board_id,
                "no": document_id,
                "mode": "del",
                "con_key": con_key,
                }
        header = Header.XML_HTTP_REQ_HEADERS.copy()
        header["Referer"] = url
        header["X-CSRF-TOKEN"] = csrf_token
        cookies = {
            "m_dcinside_" + board_id: board_id,
            "m_dcinside_lately": quote(board_id + "|" + board_name + ","),
            "_ga": "GA1.2.693521455.1588839880",
            }
        url = "https://m.dcinside.com/del/board"
        async with self.session.post(url, headers=header, data=payload, cookies=cookies) as res:
            res = await res.text()
        if res.find("true") < 0:
            raise Exception("Error while removing: " + unquote(str(res)))
        return True
    async def write_document(self, board_id, title="", contents="", name="", password="", is_minor=False):
        return await self.__write_or_modify_document(board_id, title, contents, name, password, is_minor=is_minor)
    async def __write_or_modify_document(self, board_id, title="", contents="", name="", password="", intermediate=None, intermediate_referer=None, document_id=None, is_minor=False):
        if not intermediate:
            url = "https://m.dcinside.com/write/{}".format(board_id)
            async with self.session.get(url) as res:
                parsed = lxml.html.fromstring(await res.text())
        else:
            parsed = lxml.html.fromstring(intermediate)
            url = intermediate_referer
        first_url = url
        rand_code = parsed.xpath("//input[@name='code']")
        rand_code = rand_code[0].get("value") if len(rand_code) else None
        user_id = parsed.xpath("//input[@name='user_id']")[0].get("value") if not name else None
        mobile_key = parsed.xpath("//input[@id='mobile_key']")[0].get("value")
        hide_robot = parsed.xpath("//input[@class='hide-robot']")[0].get("name")
        csrf_token = parsed.xpath("//meta[@name='csrf-token']")[0].get("content")
        con_key = await self.__access("dc_check2", url, require_conkey=False, csrf_token=csrf_token)
        board_name = parsed.xpath("//a[@class='gall-tit-lnk']")[0].text.strip()
        header = Header.XML_HTTP_REQ_HEADERS.copy()
        header["Referer"] = url
        header["X-CSRF-TOKEN"] = csrf_token
        url = "https://m.dcinside.com/ajax/w_filter"
        payload = {
                "subject": title,
                "memo": contents,
                "mode": "write",
                "id": board_id,
                }
        if rand_code:
            payload["code"] = rand_code
        async with self.session.post(url, headers=header, data=payload) as res:
            res = await res.text()
            res = json.loads(res)
        if not res["result"]:
            raise Exception("Erorr while write document: " + str(res))
        header = Header.POST_HEADERS.copy()
        url = "https://mupload.dcinside.com/write_new.php"
        header["Host"] = "mupload.dcinside.com"
        header["Referer"] = first_url
        payload = {
                "subject": title,
                "memo": contents,
                hide_robot: "1",
                "GEY3JWF": hide_robot,
                "id": board_id,
                "contentOrder": "order_memo",
                "mode": "write",
                "Block_key": con_key,
                "bgm":"",
                "iData":"",
                "yData":"",
                "tmp":"",
                "imgSize": "850",
                "is_minor": "1" if is_minor else "",
                "mobile_key": mobile_key,
                "GEY3JWF": hide_robot,
            }
        if rand_code:
            payload["code"] = rand_code
        if name:
            payload["name"] = name
            payload["password"] = password
        else:
            payload["user_id"] = user_id
        if intermediate:
            payload["mode"] = "modify"
            payload["delcheck"] = ""
            payload["t_ch2"] = ""
            payload["no"] = document_id
        cookies = {
            "m_dcinside_" + board_id: board_id,
            "m_dcinside_lately": quote(board_id + "|" + board_name + ","),
            "_ga": "GA1.2.693521455.1588839880",
            }
        async with self.session.post(url, headers=header, data=payload, cookies=cookies) as res:
            res = await res.text()
    async def __access(self, token_verify, target_url, require_conkey=True, csrf_token=None):
        if require_conkey:
            async with self.session.get(target_url) as res:
                parsed = lxml.html.fromstring(await res.text())
            con_key = parsed.xpath("//input[@id='con_key']")[0].get("value")
            payload = { "token_verify": token_verify, "con_key": con_key }
        else:
            payload = { "token_verify": token_verify, }
        url = "https://m.dcinside.com/ajax/access"
        headers = Header.XML_HTTP_REQ_HEADERS.copy()
        headers["Referer"] = target_url
        headers["X-CSRF-TOKEN"] = csrf_token
        async with self.session.post(url, headers=headers, data=payload) as res:
            return (await res.json())["Block_key"]
