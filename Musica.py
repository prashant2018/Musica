#! user/bin/python3
import bs4,requests,pyperclip,time,os

err_count = 0
os.makedirs("Musica", exist_ok=True)
location = ""
while 1:
    try:
        print('Initialising...')
        resi=requests.get('https://mp3skull.la')
        init = bs4.BeautifulSoup(resi.text,"html.parser")
        val = init.select('input[name]')[1].get('value')
        break
    except:
        if err_count<5:
            print("Connection failed! Trying Again")
            err_count+=1
            time.sleep(3)
        else:
            print("Exititng. No Connection")
            exit()

more = 'y'

def search():
    try:
        url1 = "https://mp3skull.la/search_db.php?q="+'+'.join(l)+"&fckh="+val
        print("Searching...")
        global res
        res = requests.get(url1)
    except:
    	print("Connection failed: 1.Try Again 2.Exit")
    	search_ch=int(input())
    	if(search_ch == 1):
    	    search()
    	else:
    	    exit()
			
	

def scraper():
    global title,song
    scrap = bs4.BeautifulSoup(res.text,"html.parser")
    song = scrap.select('.download_button a')    
    title = scrap.select('.mp3_title b')
    k=1

    

while more == 'y' or more == 'Y': 
    
    k = 0
    s=input("Search Song\n")
    l=s.split()
    search()
    scraper()
    

    if len(title) == 0:
        print('No song Found')
        continue

    for i in range(min(8,len(title))):
        print(str(k)+'. '+str(title[i].getText()))
        k=k+1
    
    ch = int(input('Enter Choice\n'))
    song_link = song[ch].get('href')
    location = title[ch].getText()
    
    res = requests.get(song_link, stream = True)
    
    pyperclip.copy(song_link)
    
    print("Link copied to clipboard. Starting Download")
    print("\nDonwloading...")
    
    with open(os.path.join("Musica",location),"wb") as down_file:
    	for chunks in res.iter_content(100000):
    		down_file.write(chunks)
    
    down_file.close()
    
    print("Finished Downloadind !")
    print("\nDownload More : Y-Yes N-No")
    more = input()
   
print('Thanks for using me !')
