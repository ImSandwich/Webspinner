import re 

dictionary = {}
with open("dict/pg29765.txt", "r") as fileOpen:
    txt = ""
    line = fileOpen.read()
    matches = re.finditer('[A-Z]+(?=\n)', line)
    matches2 = re.finditer('(?<=Defn: )(.+(\n))*', line)
    while True:
        try:
            word = next(matches).group(0)
            definition = next(matches2).group(0)
            if word not in dictionary:
                dictionary[word] = definition
            else:
                dictionary[word] += definition
        except StopIteration:
            break
        
        
print(dictionary)