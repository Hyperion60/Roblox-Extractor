import os, sys, requests, time

DIR_IN = 'C:\\Users\Hyperion\\AppData\\Local\\Temp\\Roblox\\http\\'
DIR_OUT = 'C:\\Users\\Hyperion\\Documents\\Final\\'

def check_file(dossier, fichier):
    file = open(dossier + fichier, "rb")
    byte = file.read(1)
    file.close()
    if byte == b'O':#Header of OGG file
        name = fichier.split('.')
        if not os.path.exists(dossier + name[0] + ".ogg"):
            os.rename(dossier + fichier, dossier + name[0] + ".ogg")

def audio(path, file): #Download and check audio file (mp3 or ogg)
    if not os.path.exists(DIR_OUT + "mp3\\" + file + ".mp3"):
        #Load URL in roblox temp file
        brut = open(path + file, "rb")
        lines = brut.readlines()
        url = ""
        i = 0
        while lines[0][i] != 104:
            i += 1
        while lines[0][i]:
            url += chr(lines[0][i])
            i += 1
        #Download the audio file
        r = requests.get(url, allow_redirects=False)
        out_file = open(DIR_OUT + "mp3\\" + file + ".mp3", 'wb+')
        out_file.write(r.content)
        out_file.close()
    #Check the extension file
    check_file(DIR_OUT + "mp3\\", file + ".mp3")

def png(path, file):#Download the picture files
    if not os.path.exists(DIR_OUT + "png\\" + file + ".png"):
        #Load the URL in Roblox temp file
        brut = open(path + file, "rb")
        lines = brut.readlines()
        url = ""
        i = 0
        while lines[0][i] != 104:
            i += 1
        while lines[0][i]:
            url += chr(lines[0][i])
            i += 1
        #Download the picture
        r = requests.get(url, allow_redirects=False)
        out_file = open(DIR_OUT + "png\\" + file + ".png", 'wb+')
        out_file.write(r.content)
        out_file.close()

def detect(file): #Detect the format file(music or picture)
    #Load the Roblox temp file
    brut = open(file, "rb")
    lines = brut.readlines()
    brut.close()

    long = len(lines)
    isOK = False
    if long > 7 and lines[7][0] == 67 and len(lines[7]) == 26:
        isOK = True
        return "mp3"
    if not isOK and long > 17 and len(lines[17]) > 1 and lines[17][1] == 80:
        return "png"
    else:
        return "None"

def main():
    list_file = os.listdir(DIR_IN)
    form = ""
    if not os.path.isdir(DIR_OUT):
        os.makedirs(DIR_OUT)
    if not os.path.isdir(DIR_OUT + "mp3\\"):
        os.makedirs(DIR_OUT + "mp3\\")
    if not os.path.isdir(DIR_OUT + "png\\"):
        os.makedirs(DIR_OUT + "png\\")
    number = len(list_file)
    acc = 1
    for file in list_file:
        print(((acc * 1000) // number) / 10, '%')
        time.sleep(0.02)
        if os.stat(DIR_IN + file).st_size > 1000:
            form = detect(DIR_IN + file)
            if form == "png":
                png(DIR_IN, file)
            if form == "mp3":
                audio(DIR_IN, file)
        acc += 1

main()