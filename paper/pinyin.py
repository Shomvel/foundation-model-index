import re


def is_capitalized_pinyin(text):
    # 定义拼音声母（不区分大小写）
    initials = r"(?i:b|p|m|f|d|t|n|l|g|k|h|j|q|x|zh|ch|sh|r|z|c|s|w|y|hs)"
    # 定义拼音韵母（不区分大小写）
    finals = r"(?i:a|o|e|i|u|ü|ai|ei|ui|ao|ou|iu|ie|üe|an|ian|en|in|un|ün|ang|eng|ing|ong|uang|iang|uan|ian|iao|uo|ue|ua|yu)"

    # 将拼音声母和韵母组合成一个拼音的正则表达式
    pinyin_pattern = f"({initials}{finals})|Er"

    # 匹配一个或3个拼音
    pinyin_regex = f"({pinyin_pattern}){{1,3}}"

    text = text.replace('-', '')
    return bool(re.fullmatch(pinyin_regex, text))


if __name__ == '__main__':
    test_data = {
        "Zhongwen": True,
        "Zhangsan": True,
        "Liming": True,
        "Wangfei": True,
        "Liuxiang": True,
        "John": False,
        "Jane": False,
        "Smith": False,
        "Xiaoming": True,
        "Guojing": True,
        "Zhaoyun": True,
        "Huangrong": True,
        "Nianci": True,
        "Yangguo": True,
        "Zhuge": True,
        "Nan": True,
        "Jiang": True,
        "Yi": True,
        "Gu": True, "Yexiang": True, "Xue": True,
        "Er": True,
    }

    for name, value in test_data.items():
        print(f"{name} expected: {value}, in reality {is_capitalized_pinyin(name)}")
