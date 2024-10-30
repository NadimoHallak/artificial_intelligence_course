
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tabulate import tabulate

# ===========================================================

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")
# chrome_options.add_argument("--headless")

# ===========================================================


def get_youtube_channel_data():
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get("https://www.youtube.com/@HsoubAcademy/videos")
        time.sleep(10)
        page = driver.find_element(By.TAG_NAME, "html")
        for i in range(3):
            time.sleep(3)
            page.send_keys(Keys.END)
        try:
            contents = driver.find_element(By.ID, "contents")

            # contents = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "contents"))
            # )
            video_titles = contents.find_elements(By.ID, "video-title-link")

            videos = []
            for title in video_titles:
                video_text = title.text if title.text else "No title"
                videos.append([video_text, title.get_property('href')])
            # print(videos)

            videos_metadata = []
            video_metadata = contents.find_elements(By.ID, "metadata-line")

            for matadata in video_metadata:
                span_tags = matadata.find_elements(By.TAG_NAME, "span")

                span_data = []
                for span in span_tags:
                    span_content = span.text
                    span_data.append(span_content)
                videos_metadata.append(span_data)
            results = []
            for item in zip(videos, videos_metadata):
                results.append(
                    [item[0], item[1]])

            with open("videos_data.txt", "w") as f:
                f.write("videos :\n")
                table = tabulate(
                    results,
                    headers=["Title", "Link", "Viewers", "Date"],
                    tablefmt="fancy_grid",
                )
                f.write(table)

        except Exception as e:
            print("-----------لم يتم العثور على الصفحة-----------")
            print(e)
            return


if __name__ == "__main__":
    get_youtube_channel_data()


# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys


# # ===========================================================

# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# # chrome_options.add_argument("--headless")

# # ===========================================================


# def get_youtube_channel_data():
#     # channel = input("what channel are you looking for ?")
#     with webdriver.Chrome(chrome_options) as driver:
#         driver.get("https://www.youtube.com/@HsoubAcademy/videos")
#         # time.sleep(3)
#         try:
#             contents = driver.find_element(By.ID, "contents")
#             vedio_title = contents.find_elements(By.ID, "video-title-link")

#             videos = []
#             for title in vedio_title:
#                 videos.append(title.get_property('href'))
#             print(videos)

#             # vedio_metadata = contents.find_elements(By.ID, 'metadata-line')
#             # print(vedio_metadata[0].find_elements(By.TAG_NAME, 'span'))


#             # for metadata in vedio_metadata:

#             #     span_tags = metadata.find_elements(By.TAG_NAME, 'span')
#             # span_data = []

#             # for span in span_tags:
#             #     span_data.append(span.text)

#             #     videos_metadata.append(span_data)

#             # results = []
#             # for item in zip(videos, videos_metadata):
#             #     results.append(item[0], item[1])

#             # print(results)

#         except Exception as e:
#             print("-----------The page not found-----------")
#             print(e)
#             return


# if __name__ == "__main__":
#     get_youtube_channel_data()
