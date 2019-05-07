import requests
import pandas as pd
import lxml.html


def get_baidu_tie(kw,pl=10):
    kwutf8 = str(kw.encode("utf-8"))[1:].replace('\\x','%').replace('\'','')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
    page = 0
    contentall = []
    maxpn = 100
    while page < pl:
        pn = page * 50
        if pn > maxpn:
            break
        url = 'https://tieba.baidu.com/f?kw='+kwutf8+'&ie=utf-8&pn='+str(pn)
        r = requests.get(url,headers=headers)
        print('getting',url,r)
        html = lxml.html.fromstring(r.text)

        a = lxml.html.fromstring(html.xpath('//code[@id="pagelet_html_frs-list/pagelet/thread_list"]/node()')[0].text)
        if page ==0:
            maxpn = int(a.xpath('//a[@class="last pagination-item "]/@href')[0].split('pn=')[-1])
            print('maxpn=',maxpn)

        hf = a.xpath('.//div[@class="col2_left j_threadlist_li_left"]/span//text()')
        z = a.xpath('.//div[@class="col2_right j_threadlist_li_right "]//a[@class="j_th_tit "]/text()')
        tieurllist = a.xpath('.//div[@class="col2_right j_threadlist_li_right "]//a[@class="j_th_tit "]/@href')
        tieurl = ['https://tieba.baidu.com'+ x for x in tieurllist]
        x = a.xpath('.//div[@class="col2_right j_threadlist_li_right "]/div[@class="threadlist_lz clearfix"]//span[starts-with(@class, "tb_icon_author")]/@title')
        c = a.xpath('.//div[@class="col2_right j_threadlist_li_right "]//div[@class="threadlist_abs threadlist_abs_onlyline "]/text()')
        c = [x.replace('\r\n','').replace(' ','').replace('\n','') for x in c]
        v = a.xpath('.//div[@class="col2_right j_threadlist_li_right "]//span[@class="threadlist_reply_date pull_right j_reply_data"]/text()')
        v = [x.replace('\r\n','').replace(' ','') for x in v]
        k = {'hf':hf,'title':z,'author':x,'content':c,'time':v,'url':tieurl}
        bb = pd.DataFrame(k)
        contentall.append(bb)
        page += 1
    ff = pd.concat(contentall,ignore_index=True)
    ff.to_csv('C:/Users/Administrator/Desktop/baidutb-'+kw+'.csv',encoding='utf-8-sig',index=False)
    print('finishprogress')


kw = '红魔手机'
get_baidu_tie(kw)
