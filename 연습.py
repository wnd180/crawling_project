from requests.api import request
from requests.models import Response


string = 'California Gold Nutrition, Omega 800 제약 등급 피쉬 오일, EPA/DHA 80%, 트라이글리세라이드 형태, 1,000mg, 피쉬 젤라틴 소프트젤 90정'
characters = "\/*[]:?"

for x in range(len(characters)):
    string = string.replace(characters[x],"")

print(string)

a = 'abc'
print(len(a))