import googletrans 
from googletrans import Translator
t = Translator()
a = t.translate("em đẹp quá",src = "vi", dest = "en")
print(a.text)