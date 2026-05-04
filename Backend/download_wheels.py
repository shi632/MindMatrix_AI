import urllib.request
import os

print("Downloading textblob...")
urllib.request.urlretrieve("https://files.pythonhosted.org/packages/19/22/e09e1e2d7ba486dd6e9695d122d10fbf97dd052d91bb358390bbec206b05/textblob-0.20.0-py3-none-any.whl", "textblob-0.20.0-py3-none-any.whl")
print("Textblob downloaded.")

print("Downloading nltk...")
urllib.request.urlretrieve("https://files.pythonhosted.org/packages/a6/0a/f47e645bf3bb9f0d7e447936a5c13bafdbb96dc36de2f5c1a7d65561a0b3/nltk-3.9.1-py3-none-any.whl", "nltk-3.9.1-py3-none-any.whl")
print("nltk downloaded.")
