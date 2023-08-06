import re


class SimpleRuleSntenceTokenizer(object):
    """
    Devide Japanese text into a list of sentences.
    """

    def __init__(self,
            delimiters=['.', '．', '。'],
            brackets=(
                ('「', '」'),
                ('『', '』'),
                ('【', '】'),
                ('〈', '〉'),
                ('\'', '\''),
                ('’', '’'),
                ('"', '"'),
                ('”', '”'),
                )
            ):
        """
        input:
            delimiters (list<str>)    : Symbols which indicate sentence devider
            brackets (list<list<str>>): Symbols list of brackets. Delimiters in a bracket will be ignored.

        output:
            void
        """

        self.delimiters = delimiters
        self.brackets   = brackets



    def tokenize(self, text):
        """
        return a list of sentences given text

        example
        ```python
        text = '「君の名は。」という映画作品がある。めっちゃ良い。'
        tokenizer = SimpleRuleSntenceTokenizer()
        tokenizer.tokenize(text) # -> ['「君の名は。」という映画作品がある。', 'めっちゃ良い。']
        ```

        input:
            text (str): string which you want to devide into a list of sentences

        output:
            sentences (list<str>): a list of sentences
        """

        delimiter2placeholder = {}
        placeholder2delimiter = {}
        placeholder_stem = '<neos_{}>'

        for idx, delimiter in enumerate(self.delimiters):
            _placeholder = placeholder_stem.format(idx)

            delimiter2placeholder[delimiter] = _placeholder
            placeholder2delimiter[_placeholder] = delimiter


        for lbracket, rbracket in self.brackets:
            query_string = r'{}(.*?){}'.format(lbracket, rbracket)

            for res in re.finditer(query_string, text):
                from_pattern = res.group(0)
                target_pattern = res.group(0)

                for delimiter in self.delimiters:
                    target_pattern = re.sub('\{}'.format(delimiter), delimiter2placeholder[delimiter], target_pattern)

                # add 'PLACEHOLDER<del>
                text = re.sub(from_pattern, target_pattern, text)

        query_string = '(' +  '|'.join('\{}'.format(delimiter) for delimiter in self.delimiters) + ')'
        text = re.sub(query_string, r'\1<delimiter>', text)

        for _placeholder, _delimiter in placeholder2delimiter.items():
            text = re.sub(_placeholder, _delimiter, text)

        sentences = text.split('<delimiter>')

        if sentences[-1] == '':
            return sentences[:-1]

        else:
            return sentences
