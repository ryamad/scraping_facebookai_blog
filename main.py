import requests
import json
import os
from bs4 import BeautifulSoup
import argparse
import datetime


def get_request():
    target_url = "https://ai.facebook.com/blog/"
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


def check_update(slack_id: str) -> None:
    basetime = datetime.time(00, 00, 00)
    soup = get_request()

    url_classes = ["[class='_8xc5 _8x97 _8w61 _913i']", "[class='_8wrb']"]
    title_classes = ["[class='_8w6a _8w6c _8w61']", "[class='_8w6a _8w6e _8w61']"]
    date_classes = [
        "[class='_8w6f _8xm4 _8wl0 _8w6h']",
        "[class='_8w6f _8xm4 _8w60 _8w6h']",
    ]
    for link_, title_, date_ in zip(url_classes, title_classes, date_classes):
        link__ = soup.select(link_)
        title__ = soup.select(title_)
        date__ = soup.select(date_)
        for link, title, date in zip(link__, title__, date__):
            print(link.get("href"))
            print(title.get_text())
            print(date.get_text())
            tdatetime = datetime.datetime.strptime(date.get_text(), "%B %d, %Y")
            today = datetime.datetime.combine(datetime.date.today(), basetime)
            print(today)
            print(tdatetime)
            if (today - tdatetime).days < 2:
                lst_text = [
                    link.get("href"),
                    title.get_text(),
                ]
                text = "\n".join(lst_text)
                if slack_id is not None:
                    requests.post(
                        slack_id,
                        data=json.dumps(
                            {"text": text},
                        ),
                    )


def main():
    parser = argparse.ArgumentParser(description="slack bot")
    parser.add_argument("--slack_id", type=str, help="incoming webhook url")
    args = parser.parse_args()

    slack_id = os.getenv("SLACK_ID") or args.slack_id

    check_update(slack_id)


if __name__ == "__main__":
    main()
