from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrapping(channel_url):
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
    time.sleep(5)
    channel_name_list = list(channel_url.split('/'))
    channel_name = channel_name_list[-2]
    channel_name = channel_name.replace('@','')

    print(f'Channel Name: {channel_name}')

    driver.get(channel_url)

    print('Scrolling')
    while True:
        old_video_count = len(driver.find_elements(By.CLASS_NAME, "style-scope ytd-rich-grid-media"))
        print(f'Total videos Scrolled: {old_video_count}')
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        video_count = len(driver.find_elements(By.CLASS_NAME, "style-scope ytd-rich-grid-media"))

        if video_count == old_video_count:
            break

    print(f'Video Count {video_count}')

    video_data = []
    print('Scrapping Channel')
    try:
        videos = driver.find_elements(By.CLASS_NAME, "style-scope ytd-rich-grid-media")
        for index,video in enumerate(videos):
            print(f'{index+1} videos Done!')
            title_link = video.find_element(By.ID, "video-title-link")
            title = title_link.get_attribute("title")

            duration_element = video.find_element(By.XPATH, ".//ytd-thumbnail-overlay-time-status-renderer//span[@id='text']")
            duration_el = duration_element.get_attribute("aria-label")

            hour,minutes,seconds = 0,0,0

            str1 = list(duration_el.replace(',', '').split())

            ihour = (str1.index('hours') if 'hours' in str1 else (str1.index('hour') if 'hour' in str1 else -1))
            if ihour!=-1:
                hour=int(str1[ihour-1])
            else:
                hour=0
                
            imin = (str1.index('minutes') if 'minutes' in str1 else (str1.index('minute') if 'minute' in str1 else -1))
            if imin!=-1:
                minutes=int(str1[imin-1])
            else:
                minutes=0
                
            isec = (str1.index('seconds') if 'seconds' in str1 else (str1.index('second') if 'second' in str1 else -1))
            if isec!=-1:
                seconds=int(str1[isec-1])
            else:
                seconds=0

            duration = f'{hour:02d}:{minutes:02d}:{seconds:02d}'

            upload_time = video.find_element(By.XPATH, ".//div[@id='metadata-line']//span[contains(@class, 'inline-metadata-item')][2]").text

            video_url = title_link.get_attribute("href")
            
            video_info_1 = {
                'Index': (index+1),
                'Title': title,
                'Link':video_url,
                'Duration': duration,
                'Upload Time': upload_time
            }
            video_data.append(video_info_1)
        
    except Exception as e:
        print(f'Scrapping 1 error: {e}')
        video_info_1 = {
                'Index': (index+1),
                'Title': '-',
                'Link':'-',
                'Duration': '-',
                'Upload Time': '-'
            }
        video_data.append(video_info_1)
        

    df1 = pd.DataFrame(video_data)

    video_info = []
    pressm = 0
    print('Scrapping Videos')
    video_test_count = 0
    for index, row in df1.iterrows():
        try:
            if video_test_count == 5:
                break
            url = row['Link']
            name = row['Title']
            print(f'{index+1}. Opening "{name}"')
            driver.get(url)
            try:
                if pressm==0:
                    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'ytp-mute-button')))
                    button.click()
                    pressm+=1
            except:
                print('Mute button Failure')
            
            expand_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="expand"]')))
            expand_button.click()
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

            try:
                likes_el = driver.find_element(By.XPATH,'//*[@id="top-level-buttons-computed"]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button/div[2]').text
                if likes_el[-1]=='K':
                    likes_el = float(likes_el.replace('K',''))
                    likes=int(likes_el*1000)

                elif likes_el[-1]=='M':
                    likes_el = float(likes_el.replace('M',''))
                    likes=int(likes_el*1000000)
                else:
                    likes=likes_el
            except:
                print('Likes Failure')
                likes='-' 
                
            try: 
                views_el = driver.find_element(By.XPATH,'//*[@id="info"]/span[1]').text
                views_el = views_el.replace(',','')
                views = int(views_el.split()[0])
            except:
                print('Views Failure')
                views='-'
                
            try:
                date_el = driver.find_element(By.XPATH,'//*[@id="info"]/span[3]').text
                date_object = datetime.strptime(date_el, '%b %d, %Y')
                date = date_object.strftime('%d/%m/%Y')
            except:
                print('Date Failure')
                date = '-'
                
            try:
                tags = driver.find_element(By.XPATH,'//*[@id="info"]/a').text
            except:
                print('Tags Failure')
                tags='-'
                
            try:
                comments_el = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="count"]/yt-formatted-string/span[1]'))).text 
                comments_el = comments_el.replace(',','')
                comments = int(comments_el)
            except:
                print('Comment Failure')
                comments='-'
            
            video_info_2={
                'Likes':likes,
                'Views':views,
                'Upload Date':date,
                'Tags':tags,
                'Comments':comments
            }
        except :
            print(f'Error in Scrapping "{name}"')
            video_info_2={
                'Likes':'-',
                'Views':'-',
                'Upload Date':'-',
                'Tags':'-',
                'Comments':'-'
            }
            
        finally:
            video_info.append(video_info_2)
            # driver.close()
            # video_test_count+=1
            

    df2 = pd.DataFrame(video_info)

    print('Saving to Excel')
    
    df = pd.concat([df1,df2],axis=1)

    excel_filename = f"{channel_name}_videos.xlsx"
    df.to_excel(excel_filename,index=False)

    print(f"saved to {excel_filename}")
 
if __name__=='__main__':
    scrapping('http://www.youtube.com/@souravjoshivlogs7028/videos') 