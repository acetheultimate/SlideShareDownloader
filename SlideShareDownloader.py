import os
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SlideShareDownloader:
    """
    SlideShareDownloader, as the name depicts, is an application which lets you to download your favourite slides.
    Just mention the opening link of the Slide Show and it will take care of the rest. Optionally, You can mention the
    quality in which you want to download.
    """
    def __init__(self, browser):
        """
        When object is being created, it takes webdriver/browser as parameter. Make sure to create a webdriver first.
        :param [selenium.webdriver] browser: A selenium webdriver instance

        """
        self.browser = browser

    def download_links(self, link, quality):
        """
        This function fetches the downloadable slides' urls from the given starting url.
        :param [str] link: Opening slide's link
        :param [int] quality: quality to be downloaded
                0: low
                1: normal -> default
                2: high
        :return List[tuple] names_and_links: List of tuples containing name and downloadable link
        """
        names_and_links = []
        self.browser.get(link)
        slide_container = WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, slide_container)]"))
        )

        folder_name = " ".join(i.capitalize() for i in link.split("/")[-1].split("-"))
        links = slide_container.find_elements_by_xpath("//img")

        quality_strs = ["data-small", "data-normal", "data-full"]

        for i in links:
            url = None
            q = quality
            while not url and q > -1:
                url = i.get_attribute(quality_strs[q])
                q -= 1

            if not url: continue

            name = " ".join(i.capitalize() for i in url.split("/")[-1].split("?cb")[0].split("-"))
            ext = name.split(".")[-1]
            name = " ".join(name.split()[:-1]) + "." + ext
            names_and_links.append((folder_name+"/"+name, url))
        return names_and_links

    @staticmethod
    def downloader(names_and_links):
        """
        This is downloader function. Takes inputs as list of tuples containing name and respective downloadable link.
        :param List[tuple] names_and_links:
        :return bool: True when it has done downloading.
        """

        for i in names_and_links:
            print(i[0])
            os.system('curl -# --create-dirs -o "%s" "%s"' % i)
        return True


if __name__ == "__main__":
    options = FirefoxOptions()
    options.add_argument("--headless")
    browser = webdriver.Firefox(executable_path="./geckodriver", firefox_options=options)

    try:
        obj = SlideShareDownloader(browser)
        entry_link = input("Enter the link: ")
        if not entry_link.startswith("http"):
            print("WARNING: Protocol not mentioned, defaulting to http.")
            entry_link = "http://" + entry_link

        quality = int(input("Enter the quality (0: low, 1: normal -> default, 2: high): ") or 1)

        n_l_tuple = obj.download_links(entry_link, quality)
        obj.downloader(n_l_tuple)

    except Exception as e:
        print("Error ", e)
    finally:
        browser.quit()
