#  Copyright (c) 2024. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import time
import httpx
import re


def get_dispose_comments2(alldata):
    comments = alldata['comments']  # 评论全部数据
    results = []
    for data in comments:
        if "location" in data:
            content = data['content']  # 评论
            creationtime = data['creationTime']  # 时间
            location = data['location']  # ip
            productcolor = data['productColor']  # 商品款式
            results.append((content, creationtime, location, productcolor))  # 这里可以方便大家保存数据
            print('评价:' + content, '时间:' + creationtime, 'IP:' + location, '商品款式:' + productcolor)
        else:
            content = data['content']  # 评论
            creationtime = data['creationTime']  # 时间
            productcolor = data['productColor']  # 商品款式
            location = '无'
            results.append((content, creationtime, location, productcolor))  # 这里可以方便大家保存数据
            print('评价:' + content, '时间:' + creationtime, 'IP:' + location, '商品款式:' + productcolor)


def get_forms_comments2(productid, client, i):
    # 这里这段代码是为了完成翻页操作
    url = 'https://api.m.jd.com/?appid=item-v3'
    timestamp = int(time.time() * 1000)  # 获取时间戳
    data = {
        'functionId': 'pc_club_productPageComments',
        'client': 'pc',
        'clientVersion': '1.0.0',
        't': timestamp,  # 时间戳
        'loginType': '3',
        'uuid': '181111935.1706791191786871307752.1706791191.1712766948.1712794165.2',
        'productId': productid,  # 商品编码
        'score': '0',
        'sortType': '5',
        'page': i,  # 翻页
        'pageSize': '10',
        'isShadowSku': '0',
        'rid': '0',
        'fold': '1',
        'bbtf': '',
        'shield': ''
    }
    resp = client.get(url, params=data)
    if resp.status_code == 200:
        alldata = resp.json()
        get_dispose_comments2(alldata)
    else:
        get_forms_comments2(productid, client, i)


def get_dispose_comments(alldata):
    # 通过接受到的json数据
    comments = alldata['comments']  # 评论全部数据
    results = []
    for data in comments:
        if "location" in data:
            content = data['content']  # 评论
            creationtime = data['creationTime']  # 时间
            location = data['location']  # ip
            productcolor = data['productColor']  # 商品款式
            results.append((content, creationtime, location, productcolor))  # 这里可以方便大家保存数据
            print('评价:' + content, '时间:' + creationtime, 'IP:' + location, '商品款式:' + productcolor)
        else:
            content = data['content']  # 评论
            creationtime = data['creationTime']  # 时间
            productcolor = data['productColor']  # 商品款式
            location = '无'
            results.append((content, creationtime, location, productcolor))  # 这里可以方便大家保存数据
            print('评价:' + content, '时间:' + creationtime, 'IP:'+location, '商品款式:' + productcolor)


def get_forms_comments(productid, client):
    url = 'https://api.m.jd.com/?appid=item-v3'
    # 获取时间戳(毫秒)
    timestamp = int(time.time() * 1000)
    # 构造新的表单
    data = {
        'functionId': 'pc_club_productPageComments',
        'client': 'pc',
        'clientVersion': '1.0.0',
        't': timestamp,  # 时间戳
        'loginType': '3',
        'uuid': '181111935.1706791191786871307752.1706791191.1712766948.1712794165.2',
        'productId': productid,  # 商品编码
        'score': '0',
        'sortType': '5',
        'page': '0',
        'pageSize': '10',
        'isShadowSku': '0',
        'fold': '1',
        'bbtf': '',
        'shield': ''
    }
    resp = client.get(url, params=data)
    # 判断状态吗是否为200是则返回json数据和页面最大数,否则重新请求
    if resp.status_code == 200:
        alldata = resp.json()
        maxpage = alldata['maxPage']
        return alldata, maxpage
    else:
        get_forms_comments(productid, client)


def get_crawling_homepage(client, name):
    url = f'https://search.jd.com/Search?'
    # 构造表单
    data = {
        'keyword': name,
        'enc': 'utf - 8',
        'spm': 'a.0.0',
        'pvid': '1de57a0845254674b2e422004fccbf59'
    }
    resp = client.get(url, params=data)
    html_data = resp.text
    if resp.status_code == 200:
        obj = re.compile(r'<div class="p-name p-name-type-2">.*?href="(?P<url>.*?)".*?<em>.*?<font class="skcolor_ljg">(?P<name>.*?)</font>.*?</em>',re.S)
        page = obj.finditer(html_data)
        results = []
        for item in page:
            url_homepage = 'https' + item.group('url')
            commodity = item.group('name')
            productid_1 = url_homepage.split('/')[3]
            productid_2 = productid_1.split('.')[0]
            results.append((url_homepage, commodity, productid_2))

        return results  # 返回所有匹配结果的列表
    else:
        print("请求失败正在为您重新请求,请求状态码:", resp)
        time.sleep(1)
        get_crawling_homepage(client, name)


def get_cerebrum():
    name = input('请输入你要查询商品评论的商品名称:')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Cookie': '__jdv=76161171|www.bing.com|-|referral|-|1712766948339; __jdu=1706791191786871307752; areaId=52993; PCSYCityID=CN_810000_813000_0; shshshfpa=6be79adc-8400-d705-2896-1b952aad5d44-1712766953; shshshfpx=6be79adc-8400-d705-2896-1b952aad5d44-1712766953; jsavif=1; ipLoc-djd=52993-52994-146614-146647; unick=jd_nIFdPRHxWkxk; pin=jd_nIFdPRHxWkxk; thor=E3B3A043C8B2A57BE2837A102479BE8459F4FE54B0CBB33487B7945E4BD34A04497F2D2ACD4B6896A579B9D9DAA4E879F0340FBF2FFA8541D23503E139EC1D12D8106BD987704FD3E16091AD24FD0C69B9F36D998AA9C2FBB499137ED0411CD561E39539BD5001EEEB49D10D39E331417BF29CBA166FEB6CBFC68EFB5B8A59731E7656C2C1242B519BE0D406354CC3DFA834313AC078AC0967678FC7519EFD7F; flash=2_JfHCeLvFQcb0TeRT-8Zaxkk2VJUKFJTqcrtTUsJyTa31mdcWXjf9ON3tWqUVbGIrjQ80zgJ4foJVpLJ668u9Wo4evBXYd-NDuMc7D2urfGD*; _tp=Yi05Tx2V0TpZ93Lx3BNEpg%3D%3D; pinId=5E87Jnot-H8K3Dh_Vea_ig; avif=1; jsavif=1; rkv=1.0; token=e4c343ae15de6bf917eb9a45739e9bc6,3,951538; __tk=cebc25dad78303178d70773abe871bdd,3,951538; shshshfpb=BApXeuObwy-tAETTMdkc5sZpfcuKRa-yeBlA3bnxh9xJ1MlCEC4C2; xapieid=jdd033S3HUGUO3E52LIJHINQ4JT62PZBQQICJF7AUVH4U6MN72V5G6IOHBHNFJCARHQLSW3PANN7QI6HQUK6SNPXFDANR3EAAAAMOZD4FZMQAAAAADADQEMXNGNXRCAX; __jda=143920055.1706791191786871307752.1706791191.1706791191.1712766948.1; __jdb=143920055.23.1706791191786871307752|1.1712766948; __jdc=143920055; qrsc=3; 3AB9D23F7A4B3CSS=jdd033S3HUGUO3E52LIJHINQ4JT62PZBQQICJF7AUVH4U6MN72V5G6IOHBHNFJCARHQLSW3PANN7QI6HQUK6SNPXFDANR3EAAAAMOZECYJVYAAAAACN4CFQ3FUKV4KUX; 3AB9D23F7A4B3C9B=3S3HUGUO3E52LIJHINQ4JT62PZBQQICJF7AUVH4U6MN72V5G6IOHBHNFJCARHQLSW3PANN7QI6HQUK6SNPXFDANR3E',
        'Referer': 'https://www.jd.com/'
    }
    client = httpx.Client(http2=True, headers=headers, timeout=15)
    # 发送请求获取返回的京东主页html,然后进行re处理天气出需要的数据
    results = get_crawling_homepage(client=client, name=name)
    # 循环results获取商品名称页面地址和productId
    for result in results:
        url_homepage = result[0]
        commodity = result[1]
        productid = result[2]
        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print('商品名称:' + commodity, '页面地址:' + url_homepage)
        # 发送请求获取返回的json数据和页面最大数
        alldata, maxpage = get_forms_comments(productid=productid, client=client)
        # 判断页面最大数
        if maxpage == 1:
            # 发送json数据
            get_dispose_comments(alldata)

        elif maxpage >= 1:
            # 发送json数据
            get_dispose_comments(alldata)
            maxpage += 1
            # 使用for循环完成翻页操作
            for maxpage2 in range(1, maxpage):
                get_forms_comments2(i=maxpage2, client=client, productid=productid)

        elif maxpage == 0:
            print('没有评论哦~')


if __name__ == '__main__':
    get_cerebrum()
