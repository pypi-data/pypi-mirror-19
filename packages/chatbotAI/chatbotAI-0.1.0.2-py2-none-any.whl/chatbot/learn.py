import re

class Learn:

    def __init__(self,statements):
        self.regex = {}
        for context in statements:
            self.regex[context] = self.getRegex(statements[context])


    def getRegex(self,statements):
        stripper = re.compile("(^[^a-z0-9]+|[^a-z0-9]+$)")
        sentenceToWords = [[stripper.sub("",word) for word in s.split()] for s in statements]
        if not len(sentenceToWords):
            raise ValueError("Should pass atleast 1 statement as parameter value for 'statements'")
        commonWords = set(sentenceToWords[0])
        for words in sentenceToWords[1:]:
            commonWords = commonWords.intersection(words)
        orderdCW = [word for word in sentenceToWords[1] if word in commonWords]
        regex = ""
        N = len(sentenceToWords)
        prev=[-1 for i in range(N)]
        first = True
        regexchar = re.compile("([?.\[\]()\\\+])")
        for word in orderdCW:
            cur = [sentence.index(word) for sentence in sentenceToWords]
            word = regexchar.sub("\\\\\\1",word)
            conditions = [(prev[i]+1)!=cur[i] for i in range(N)]
            if any(conditions):
                if all(conditions):regex += ("" if first else "[^a-z0-9]+") + "(.+)[^a-z0-9]+"+word
                elif first:regex += "(.*)"+word
                else:regex += "(.*)[^a-z0-9]+"+word
            else:regex += ("(.*)" if first else "[^a-z0-9]+")+word
            prev = cur
            first = False
        regex += "(.*)" 
        return regex
            
