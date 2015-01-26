import wget

url = 'https://github.com/comp-journalism/commentIQ/blob/master/data/vocab.csv'
filename = wget.download(url)

print filename