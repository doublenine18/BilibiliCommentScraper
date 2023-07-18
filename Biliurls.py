
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime
date_format = "%Y-%m-%d"

# https://search.bilibili.com/all?keyword=&page=2&o=24
base_url = 'https://search.bilibili.com/all?keyword={keyword}'

keywords = ['阿里被罚',
            '阿里集团被罚',
            '阿里巴巴被罚',
            '阿里巴巴集团被罚',
            '蚂蚁被罚',
            '蚂蚁集团被罚',
            '蚂蚁金服被罚']
urls = []
for keyword in keywords:
    url = base_url.format(keyword=keyword)
    urls.append((url,keyword))

all_urls = []
for url in urls:
    all_urls.append(url)
    for i in range(2, 43):
        temp = url[0] + '&page=' + str(i) + str('&o=') + str((i-1)*24)
        all_urls.append((temp,url[1]))

browser = webdriver.Chrome()


def get_details(df, url, browser):
    url,keyword = url[0],url[1]
    browser.get(url)
    time.sleep(2)
    html = BeautifulSoup(browser.page_source, features="html.parser")
    video_details = html.find_all('div', attrs={'class':'bili-video-card__wrap __scale-wrap'})
    
    link_infos = []
    for video_detail in video_details:
        link_info = {}
        href = video_detail.find('a').get('href')
        link_info['video_href'] = 'https:' + href if href else ''
        link_info['视频ID'] = href[-13:-1] if href else ''
        link_info['keyword'] = keyword
        link_info['video_list_urls'] = url
        title = video_detail.find('h3', class_='bili-video-card__info--tit').get('title')
        link_info['视频标题'] = title
        author = video_detail.find('span', class_='bili-video-card__info--author').text
        link_info['author'] = author
        date = video_detail.find('span', class_='bili-video-card__info--date').text
        if date: 
            date = date.split(' ')[-1]
            date = date if len(date) > 6 else '2023-' + date
            # date = datetime.strptime(date, date_format)
        link_info['date'] = date
        # print(link_info)
        link_infos.append(link_info)

    df = df.append(link_infos,ignore_index=True)
    return df


# create pandas to save data
df = pd.DataFrame(
    columns=['视频标题', '视频ID','keyword','video_href','video_list_urls','author', 'date'])

for url in all_urls:
    df = get_details(df, url, browser)
    print(df.shape)

browser.close()

print("原始urls的个数{shape}\n".format(shape=df.shape))

# filter 视频标题 contains '罚'
df = df[df['视频标题'].str.contains('罚')]
print("原始 视频标题 的包含 '罚' 个数{shape}\n".format(shape=df.shape))

# remove distinct 视频ID
df = df.drop_duplicates(subset=['视频ID'])
print("视频ID去重后的个数 {shape}\n".format(shape=df.shape))


# save data to csv
df.to_csv("./BiliVideoUrls.csv", index=False, encoding='utf-8-sig')





