"""2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования
в последовательность кодов (не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных."""


def convert_to_bytes(words):
    if len(words) > 0:
        for word in words:
            word_length = len(word)
            b = bytes(word, 'utf-8')
            if word_length == len(b):
                print(type(b))
                print(b)
                print(len(b))
            else:
                b = str(b, encoding='utf-8')
                print(f"Слово '{b}' не входит в ASCII формат")


if __name__ == '__main__':
    words_list = ["class", "function", "method"]
    convert_to_bytes(words_list)
