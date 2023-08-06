import nltk
import MeCab


__all__ = ["tokenize", "LANGUAGES"]


LANGUAGES = {"english", "japanese"}

japanese_tagger = MeCab.Tagger()
japanese_tagger.parse("")  # prevent UnicodeDecodeError

japanese_sentence_tokenizer = nltk.RegexpTokenizer(
    "[^{0}]+(?:[{0}]+|$)".format("!?.！？。．"))


def tokenize(document, language="english"):
    if language not in LANGUAGES:
        raise ValueError("The language, {} is not supported.".format(language))

    return {
        "english": tokenize_in_english,
        "japanese": tokenize_in_japanese,
    }[language](document)


def tokenize_in_english(document):
    return [nltk.tokenize.word_tokenize(sentence.strip())
            for sentence in nltk.tokenize.sent_tokenize(document.strip())]


def tokenize_in_japanese(document):
    return [list(sentence_to_words_in_japanese(sentence.strip()))
            for sentence
            in japanese_sentence_tokenizer.tokenize(document.strip())]


def sentence_to_words_in_japanese(sentence):
    node = japanese_tagger.parseToNode(sentence)

    while node != None:
        if node.surface != "":
            yield node.surface

        node = node.next
