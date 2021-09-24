import json
import functools
import boto3
from wordcloud import WordCloud


def highlight_word(
    target_word, word, font_size, position, orientation, font_path, random_state
):
    if word in target_word:
        return (244, 172, 154)
    else:
        return (229, 219, 206)


def handler(event, context):
    print(event)
    payload = event["body"]
    print(payload)

    data = json.loads(payload)

    proceed_dict = data["quests"]
    user_name = data["user_name"]

    freq_dict = {k: int(v * 100) for k, v in proceed_dict.items()}
    color_func = functools.partial(highlight_word, data["highlight"])

    wc = WordCloud(
        background_color=(251, 251, 245),
        max_words=100,
        font_path="KleeOne-Regular.ttf",
        width=1200,
        height=630,
        color_func=color_func,
    )
    wc.generate_from_frequencies(freq_dict)

    wc.to_file("/tmp/out.png")

    s3 = boto3.client("s3")  # S3オブジェクトを取得
    s3.upload_file(
        "/tmp/out.png",
        "study-share",
        f"{user_name}/all.png",
        ExtraArgs={"ACL": "public-read"},
    )

    url = f"https://study-share.s3.ap-northeast-1.amazonaws.com/{user_name}/all.png"

    return {"statusCode": 200, "body": url}


if __name__ == "__main__":
    handler("", "")
