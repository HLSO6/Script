import re

str1 = 'https://pixelmaster.io/?ref=dappreview'
str2 = 'dappreview'
if  str1.find(str2) != -1:
    pattern = re.compile(r'(\/\#|\/\?|\/dappreview|\?ref).*')
    print(pattern.findall(str1))
    content = re.sub(pattern, '', str1)
    print(content)
else:
    print('+++++')
