class Header:
    # 페이지 당 문서 수
    DOCS_PER_PAGE = 200
    # User-Agenet를 모바일 사용자로 지정했기 때문에 데스크톱 웹페이지가 아니라 모바일 웹페이지를 받는다.
    GET_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36"
        }
    # GET 리퀘스트 시 응답이 XML 형식으로 돌아오도록 한다.
    XML_HTTP_REQ_HEADERS = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
    # POST 리퀘스트 시 전송하는 데이터의 형식을 지정한다.
    POST_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36",
        }
    # The "__gat_mobile_search" value appears to be related to Google Analytics, specifically to tracking and managing analytics data for mobile searches.
    # The "_gat" prefix is commonly used in Google Analytics cookies and indicates that it is an internal Google Analytics cookie.
    # The specific part "mobile_search" likely suggests that this cookie is associated with tracking analytics data specifically related to mobile searches on a website.
    # Google Analytics uses cookies to track various aspects of user behavior, including the source of traffic, browsing patterns, and interactions on a website.
    # The "__gat_mobile_search" cookie, in particular, may be used to differentiate and analyze data specifically related to mobile search activity.
    # It's important to note that the exact meaning and purpose of "__gat_mobile_search" may vary depending on the specific implementation and configuration of 
    # Google Analytics on a particular website. Google Analytics cookies are often associated with unique identifiers and timestamps that assist in tracking and analyzing user behavior.
    GALLERY_POSTS_COOKIES = {
        "__gat_mobile_search": 1,
        "list_count": DOCS_PER_PAGE,
        }
    # The "_ga" cookie is used by Google Analytics to distinguish unique users by assigning a unique identifier to each user's browser.
    # The value "GA1.2.693521455.1588839880" consists of multiple components separated by periods:
    # "GA1" indicates the version of the cookie.
    # "2" represents the domain depth. In this case, it indicates that the cookie is associated with the second level domain.
    # "693521455" is the unique client identifier.
    # "1588839880" represents the timestamp or expiration date of the cookie.
    GOOGLE_ANALYTIC_COOKIES = {
        "_ga": "GA1.2.693521455.1588839880"
    }
