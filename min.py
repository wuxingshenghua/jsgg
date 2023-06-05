import requests
from bs4 import BeautifulSoup
import re

# 定义总页面链接
main_page_url = "http://www.jsgg.com.cn/Index/TopicList.asp?TopicNameID=176"

# 发送HTTP请求获取总页面内容
main_page_response = requests.get(main_page_url)

# 检查响应状态码，确保请求成功
if main_page_response.status_code == 200:
    # 使用BeautifulSoup解析页面内容
    soup = BeautifulSoup(main_page_response.text, "html.parser")

    # 获取所有公告的链接
    announcement_links = soup.find_all("a", href=re.compile(r"Index/Display\.asp\?NewsID=\d+"))

    for link in announcement_links:
        announcement_url = link["href"]

        # 构建公告页面的完整链接
        full_announcement_url = f"http://www.jsgg.com.cn/{announcement_url}"

        # 发送HTTP请求获取公告页面内容
        announcement_response = requests.get(full_announcement_url)

        # 检查响应状态码，确保请求成功
        if announcement_response.status_code == 200:
            # 使用BeautifulSoup解析公告页面内容
            announcement_soup = BeautifulSoup(announcement_response.text, "html.parser")

            # 提取下载链接
            download_link = announcement_soup.find("a", href=re.compile(r"Files/PictureDocument/\d+\.pdf"))

            if download_link:
                download_url = download_link["href"]

                # 构建附件下载链接的完整链接
                if not download_url.startswith("http://www.jsgg.com.cn/"):
                    download_url = f"http://www.jsgg.com.cn/{download_url}"

                # 发送HTTP请求下载文件
                file_response = requests.get(download_url)

                # 检查响应状态码，确保请求成功
                if file_response.status_code == 200:
                    # 提取文件名
                    attachment_name = download_link.text.strip()
                    # 替换文件名中的非法字符
                    filename = re.sub(r'[\\/:*?"<>|]', '_', attachment_name) + ".pdf"

                    # 保存文件到本地
                    with open(filename, "wb") as file:
                        file.write(file_response.content)

                    print(f"文件 {filename} 下载完成")
                else:
                    print(f"请求附件下载链接 {download_url} 失败")
            else:
                print(f"在公告 {full_announcement_url} 中未找到下载链接")
        else:
            print(f"请求公告页面 {full_announcement_url} 失败")
else:
    print("请求总页面失败")
