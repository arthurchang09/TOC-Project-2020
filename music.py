"""
music_name=[
    "op48 no 1 by Chopin",
    "Symphony no.6 by Tchaikovsky",
    "BWV565 by Bach",
    "Chaconne by Bach",
    "Le Temps des cathedrales",
    "Violin Concerto in D major by Tchaikovsky",
    "op 55 no.1 by Chopin",
    "Der Erlkönig violin version",
]
composer_name=[
    "Chopin",
    "Tchaikovsky",
    "Bach",
    "Bach",
    "鐘樓怪人",
    "Tchaikovsky",
    "Chopin",
    "Schubert",
]
music_link=[
    "https://www.youtube.com/watch?v=-7mntyrW3HU",
    "https://www.youtube.com/watch?v=zIJiPlbJjs8",
    "https://www.youtube.com/watch?v=Nnuq9PXbywA",
    "https://www.youtube.com/watch?v=ngjEVKxQCWs",
    "https://www.youtube.com/watch?v=qT6Mpkj9Y8Q",
    "https://www.youtube.com/watch?v=CTE08SS8fNk",
    "https://www.youtube.com/watch?v=e3yrEEM5j_s",
    "https://www.youtube.com/watch?v=UWNCbpwC-PQ",
]
"""
music_name=[]
music_link=[]
composer_name=[]

f1=open("music_name.txt","r")
music_name=f1.readlines()
music_name[len(music_name)-1]+="\n"
f1.close()
f2=open("music_link.txt","r")
music_link=f2.readlines()
f2.close()
f3=open("music_composer.txt","r")
composer_name=f3.readlines()
f3.close()

def load_in_file():
    f1=open("music_name.txt","w")
    f1.writelines(music_name)
    f1.close()
    f2=open("music_link.txt","w")
    f2.writelines(music_link)
    f2.close()
    f3=open("music_composer.txt","w")
    f3.writelines(composer_name)
    f3.close()