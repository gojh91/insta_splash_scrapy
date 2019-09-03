# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import *
import json
from scrapy.http import FormRequest
from instagram.items import InstagramItem
import time
import re
import urllib.parse
from datetime import datetime as dt

class InstagramcrawlSpider(scrapy.Spider):
    name = 'instagramCrawl'
    allowed_domains = ['www.instagram.com']
    start_urls = [
        'https://www.instagram.com/ajax/bz'
        ]
    first = 100


    # 키워드 변경
    keyword = ""
    # accID
    accId = ""


    hashKey = "174a5243287c5f3a7de741089750ab3b"
    postHashKey: '6ff3f5c474a240353993056428fb851e'



    def start_requests(self):
        timestamp = time.time()
        s = str(timestamp)
        qid = s.split(".")
        # 1522049204.295597
        for url in self.start_urls:
            yield SplashFormRequest(
                            url=url, callback=self.parse,
                            headers = {
                                'cookie': 'mid=XUPd8wABAAEAhfjAaBu9HIsUHK_g; shbid=3399; shbts=1566777977.951645; ig_direct_region_hint=PRN; csrftoken=nV4vyZc6g0cMk3M3O1kDeuwqUczWQCsL; ds_user_id={}; sessionid={}%3AGCFsB0dJqmQ5iM%3A27; rur=VLL; urlgen="{\"223.62.188.180\": 9644\054 \"222.107.238.125\": 4766}:1i2n8A:QaIjJ0n6YT5um6ydb9qoe8OV_qk"'.format(self.accId, self.accId),
                                'origin': 'https://www.instagram.com',
                                'referer': 'https://www.instagram.com/explore/tags/%ED%9E%90%EB%A7%81/',
                                'sec-fetch-mode': 'cors',
                                "sec-fetch-site": 'same-origin',
                                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Whale/1.6.81.8 Safari/537.36',
                                'x-csrftoken': 'nV4vyZc6g0cMk3M3O1kDeuwqUczWQCsL',
                                'x-ig-app-id': '936619743392459',
                                'x-ig-www-claim': 'hmac.AR34X-B2OSZnvGza5u7NloV8W-DZO4-fbIwTcXUBq2uGp0Xa',
                                'x-instagram-ajax': 'fcdbd4a00f5a',
                                'x-requested-with': 'XMLHttpRequest'
                            },
                            formdata={
                                'q': '[{"user":"{}","page_id":"xnbstc","app_id":"936619743392459","device_id":"XUPD8WABAAEAHFJAABU9HISUHK_G","posts":[["qex:expose",{"universe_id":"25","device_id":"XUPD8WABAAEAHFJAABU9HISUHK_G"},1567125318263,0],["qex:expose",{"universe_id":"2","device_id":"XUPD8WABAAEAHFJAABU9HISUHK_G"},1567125319276,0]],"trigger":"qex:expose","send_method":"ajax"}]'.format(self.accId),
                                'ts': '{}'.format(qid),
                                },
                        )

    def parse(self, response):
        print(response.url)
        yield SplashRequest("https://www.instagram.com/explore/tags/%ED%9E%90%EB%A7%81/", self.realRealParse,
            endpoint = 'render.html',
            args={'wait': 2.5}
        )



    def realRealParse(self, response):
        try:
            js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
            js = js[0].replace("window._sharedData = ", "")
            jscleaned = js[:-1]

            locations = json.loads(jscleaned)
            jsonResult = locations['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']
        except:
            locations = json.loads(response.body_as_unicode())
            jsonResult = locations['data']['hashtag']['edge_hashtag_to_media']

        for edge in jsonResult['edges']:
            item = InstagramItem()
            try:
                item['text'] = edge['node']['edge_media_to_caption']['edges'][0]['node']['text']
            except:
                item['text'] = ''

            timestamp = edge['node']['taken_at_timestamp']
            item['date'] = dt.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            shortcode = edge['node']['shortcode']
            item['shortcode'] = shortcode
            # item['each_url'] = 'https://www.instagram.com/graphql/query/?query_hash=477b65a610463740ccdb83135b2014db&variables={"shortcode":"' + shortcode + '"}'

            # shortcode = edge['node']['shortcode']
            item['each_url'] = 'https://www.instagram.com/graphql/query/?query_hash=477b65a610463740ccdb83135b2014db&variables={"shortcode":"' + edge['node']['shortcode'] + '","child_comment_count":3,"fetch_comment_count":40,"parent_comment_count":24,"has_threaded_comments":true}'

            ###숫자 형식으로 가져옴
            item['like_count'] = edge['node']['edge_liked_by']['count']


            if edge['node']["is_video"]:
                item["video_view_count"] = edge['node']["video_view_count"]
                item['explain'] = 'Video'
            else:
                item["video_view_count"] = -1
                item['explain'] = edge['node']['accessibility_caption']

            yield item

            # yield SplashRequest(each_url, self.realRealRealParse,
            #     headers= {
            #         # 'cookie': 'mid=XUPd8wABAAEAhfjAaBu9HIsUHK_g; shbid=3399; ig_direct_region_hint=PRN; csrftoken=nV4vyZc6g0cMk3M3O1kDeuwqUczWQCsL; ds_user_id=2905070466; sessionid=2905070466%3AGCFsB0dJqmQ5iM%3A27; shbts=1567053757.062416; rur=VLL; urlgen="{\"223.38.23.110\": 9644\054 \"222.107.238.125\": 4766}:1i3X5Y:mYd-4kQGJ7dlVJWfLs7pQvktegQ"',
            #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Whale/1.6.81.8 Safari/537.36'
            #     },
            #     endpoint = 'render.html',
            #     args={'wait': 2.5}
            # ) 

            
        hasNext = jsonResult['page_info']['has_next_page']
        afterKey = jsonResult['page_info']['end_cursor']
        if hasNext is not None:
            # self.first += 1
            params = {'tag_name':self.keyword,'first':self.first,'after':afterKey}

            # testUrl = 'https://www.instagram.com/graphql/query/?query_hash={}&variables={}'.format(response.meta['queryKey'], urllib.parse.quote_plus(str(params)))
            testUrl = 'https://www.instagram.com/graphql/query/?query_hash={}&variables={}'.format(self.hashKey, urllib.parse.quote_plus(str(params)))
            testUrl = re.sub(r"\+","", testUrl)
            testUrl = re.sub(r'%27','\"',testUrl)

            yield response.follow(
                url = testUrl, callback=self.realRealParse,
                meta = {
                    'queryKey' : self.hashKey#response.meta['queryKey']
                }
            )

    def realRealRealParse(self, response):
        print("*"*100)
        print("*"*100)
        print("*"*100)
        print(json.loads(response.css("pre::text").get()))
        post = json.loads(response.css("pre::text").get())['data']['shortcode_media']
        item = InstagramItem()
        try:
            item['text'] = post['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            item['text'] = ''

        timestamp = post['taken_at_timestamp']
        item['date'] = dt.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        shortcode = post['shortcode']
        item['shortcode'] = shortcode
        item['each_url'] = response.url

        item['like_count'] = post['edge_media_preview_like']['count']

        if post['location']:
            locDic = {}
            locDic[post['location']['id']] = post['location']['name']
            item['location'] = locDic
            item['address_json'] = post['location']['address_json']
        else:
            item['location'] = ''
            item['address_json'] = ''

        mediaList = []
        if post['__typename'] == 'GraphSidecar':
            for edge in post['edge_sidecar_to_children']['edges']:
                edgeDic = {}
                is_video = edge['node']['is_video']
                edgeDic['is_video'] = is_video
                edgeDic['media_url'] = edge['node']['display_url']
                if is_video:
                    edgeDic["video_view_count"] = edge['node']["video_view_count"]
                    edgeDic['explain'] = 'Video'
                else:
                    edgeDic["video_view_count"] = -1
                    edgeDic['explain'] = edge['node']['accessibility_caption']
                mediaList.append(edgeDic)
        else:
            mediaList = []
            edgeDic = {}
            is_video = post['is_video']
            edgeDic['is_video'] = is_video
            edgeDic['media_url'] = post['display_url']
            if is_video:
                edgeDic["video_view_count"] = post["video_view_count"]
                edgeDic['explain'] = 'Video'
            else:
                edgeDic["video_view_count"] = -1
                edgeDic['explain'] = post['accessibility_caption']
            mediaList.append(edgeDic)
        item['mediaList'] = mediaList



        yield item