from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import json, urllib.request, time, os, sys, shutil
path = os.getcwd()
#titledetails_url = "https://raw.githubusercontent.com/blawar/nut/master/titledb/US.en.json"
#version_url = "https://raw.githubusercontent.com/blawar/nut/master/titledb/versions.txt"
#urllib.request.urlretrieve(version_url, filename="versions.txt")
#urllib.request.urlretrieve(titledetails_url, filename="titledata.json")

try:
	os.mkdir("cache")
except(FileExistsError):
	pass

with open('titledata.json') as titlejson_file:  
    titledata = json.load(titlejson_file)
print("Grabbing Latest VersionList")
time.sleep(1)
print("Ready!")
versionlist = (open(os.path.join(os.getcwd(), 'versions.txt'), "r", encoding="utf8")).readlines()
version_data = {}
for item in versionlist:
	version_data[item.split('|')[0]] = (item.split('|')[2])[:-1]

def write_to_JSON(data, name):
	json_fpath = name + '.json'
	with open(json_fpath, 'w') as fp:
		json.dump(data, fp)

def getJSON(filePathAndName):
	with open(filePathAndName, 'r') as fp:
		return json.load(fp)
try:
	my_titles = getJSON('./titles.json')
except:
	x = {}
	write_to_JSON(x, "titles")
	my_titles = getJSON('./titles.json')

def update_tree():
	tree.insert('', 'end', values=(e1.get(), e2.get(), e3.get(), "tba"))
	my_titles[e2.get()] = {'Title': e1.get(), 'Current_Version': e3.get()}
	e1.delete(0, 'end')
	e2.delete(0, 'end')
	e3.delete(0, 'end')

def showImage(tid):
	global icon
	iconsrc=(path + "\\cache\\" + tid + ".jpg")
	image = Image.open(iconsrc)
	image = image.resize((131, 131), Image.ANTIALIAS)
	icon = ImageTk.PhotoImage(image)
	canvas.create_image(1, 1, image=icon, anchor=NW)
	canvas.update()

def selectItem(event):
	global selected_tid
	curItem = tree.item(tree.focus())
	selected_tid = (curItem['values'][1])
	for key, value in titledata.items():
		try:
			if (value['id']) == (selected_tid).upper():
				rdate = str(value['releaseDate'])[-2:] + "/" + str(value['releaseDate'])[4:-2] + "/" + str(value['releaseDate'])[:4]
				if os.path.isfile(path + "\\cache\\" + value['id'] + ".jpg"):
					pass
				else:
					urllib.request.urlretrieve((value['iconUrl']), filename=path + "\\cache\\" + value['id'] + ".jpg")
				showImage(value['id'])
				release_date.set(rdate)
				if len(value['name']) >= 60:
					game_title.set((value['name'])[0:58]+"....")
				else:
					game_title.set(value['name'])
				publisher_var.set(value['publisher'])
		except(AttributeError):
			if str(selected_tid) in str(value['id']):
				rdate = str(value['releaseDate'])[-2:] + "/" + str(value['releaseDate'])[4:-2] + "/" + str(value['releaseDate'])[:4]
				if os.path.isfile(path + "\\cache\\" + value['id'] + ".jpg"):
					pass
				else:
					urllib.request.urlretrieve((value['iconUrl']), filename=path + "\\cache\\" + value['id'] + ".jpg")
				showImage(value['id'])
				release_date.set(rdate)
				game_title.set(value['name'])
				publisher_var.set(value['publisher'])
				

def delete_entry():
	global selected_tid
	my_titles.pop(selected_tid)
	print("Title Deleted!")
	all_titles()

def update_ver():
	global selected_tid
	my_titles[selected_tid]['Current_Version'] = e4.get()
	print("Updated!")
	have_updates()
	e4.delete(0, 'end')

def all_titles():
	tree.delete(*tree.get_children())
	for key, value in my_titles.items():
		for item in (my_titles[key].items()):
			gtitle = my_titles[key]['Title']
			cversion = my_titles[key]['Current_Version']
			try:
				if version_data[key.upper()]:
					if cversion == version_data[(key[:-3] + '800').upper()]:
						tree.insert('', 'end', values=(gtitle, key, cversion, version_data[(key[:-3] + '800').upper()]), tags = ('green'))
					else:
						tree.insert('', 'end', values=(gtitle, key, cversion, version_data[(key[:-3] + '800').upper()]), tags = ('red'))
				break
			except:
				tree.insert('', 'end', values=(gtitle, key, cversion, '0'), tags = ('green'))
				break

def have_updates():
	tree.delete(*tree.get_children())
	for key, value in my_titles.items():
		for item in (my_titles[key].items()):
			gtitle = my_titles[key]['Title']
			cversion = my_titles[key]['Current_Version']
			try:
				if version_data[key.upper()]:
					if cversion == version_data[(key[:-3] + '800').upper()]:
						pass
					else:
						tree.insert('', 'end', values=(gtitle, key, cversion, version_data[(key[:-3] + '800').upper()]), tags = ('red'))
				break
			except:
				pass
				break

def save_json():
	print("Saving!")
	write_to_JSON(my_titles,'titles')


pgrm=Tk()
window_width = 625
window_height = 550
screen_width = pgrm.winfo_screenwidth()
screen_height = pgrm.winfo_screenheight()
x_coord = (screen_width/2)-(window_width/2)
y_coord = ((screen_height/2)-100)-(window_height/2)
pgrm.geometry("%dx%d+%d+%d" % (window_width,window_height,x_coord,y_coord))
pgrm.title("Switch Update Manager")

menubar = Menu(pgrm)
menubar.add_command(label="Save All", command=save_json)
pgrm.config(menu=menubar)

tree=ttk.Treeview()
tree["columns"]=("Title","TitleID","Current Version","Latest Version")
tree.column("Title", width=230)
tree.column("TitleID", width=120)
tree.column("Current Version", width=80)
tree.column("Latest Version", width=90)
tree.column("#0", width=0)
tree.heading("Title", text = "Title")
tree.heading("TitleID", text = "TitleID")
tree.heading("Current Version", text = "Current Ver.")
tree.heading("Latest Version", text = "Latest Ver.")
tree.tag_configure('green', background='#00cc99')
tree.tag_configure('red', background='#cd5c5c')
tree.bind('<ButtonRelease-1>', selectItem)



canvas = Canvas(width=130, height=130, bg='gray')

ltitle = Label(pgrm, text="Titles:", font='Helvetica 11 bold', padx=16)
lappend = Label(pgrm, text="Append A New Title:", font='Helvetica 11 bold', padx=16)
ledit = Label(pgrm, text="Data Manipulation:", font='Helvetica 11 bold', padx=16)
l1 = Label(pgrm, text="Title:", font='Helvetica 10', padx=16)
e1 = Entry(pgrm)
l2 = Label(pgrm, text="TitleID:", font='Helvetica 10')
e2 = Entry(pgrm)
l3 = Label(pgrm, text="Version:", font='Helvetica 10')
e3 = Entry(pgrm)
btn1 = Button(pgrm, text= "Append Title")
btn1.config(command=update_tree)
btnall = Button(pgrm, text= "All Titles")
btnall.config(command=all_titles)
btnupdate = Button(pgrm, text= "Have Updates")
btnupdate.config(command=have_updates)
btncrnt = Button(pgrm, text= "Update Version")
btncrnt.config(command=update_ver)
l4 = Label(pgrm, text="Update Current Ver:", font='Helvetica 10', padx=16)
e4 = Entry(pgrm)
l5 = Label(pgrm, text="Delete Entry:", font='Helvetica 10')
btndelete = Button(pgrm, text= "Delete!")
btndelete.config(command=delete_entry)
game_title = StringVar(pgrm)
game_title.set('Game Titles')
l6 = Label(pgrm, textvariable=game_title, font='Helvetica 11 bold')
release_date = StringVar(pgrm)
release_date.set('Release Date')
l7 = Label(pgrm, textvariable=release_date, font='Helvetica 10')
publisher_var = StringVar(pgrm)
publisher_var.set('Publisher')
l8 = Label(pgrm, textvariable=publisher_var, font='Helvetica 10')

ltitle.grid(column=0, columnspan=2, row=0, sticky=W, pady=8)
btnall.grid(column=3, row=0, pady=4, sticky=E)
btnupdate.grid(column=4, row=0, pady=4, padx=(0,16), sticky=E)
tree.grid(column=0, row=1, columnspan=5, padx=16, pady=4, sticky=W+E)

lappend.grid(column=0, columnspan=2, row=3, sticky=W)

l1.grid(column=0, row=5, sticky=W)
e1.grid(column=0, row=6, padx=(16,0))
l2.grid(column=1, row=5, sticky=W, padx=(16,0))
e2.grid(column=1, row=6, sticky=W, padx=(16,0))
l3.grid(column=2, row=5, sticky=W, padx=(16,0))
e3.grid(column=2, row=6, sticky=W, padx=(16,0))
btn1.grid(column=4, row=6, padx=16, sticky=E)
ledit.grid(column=0, columnspan=8, row=7, sticky=W)
l4.grid(column=0, row=8, sticky=W)
e4.grid(column=1, row=8, padx=(16,0))
btncrnt.grid(column=2, row=8)
l5.grid(column=3, row=8, sticky=E)
btndelete.grid(column=4, row=8, padx=16, sticky=E)

canvas.grid(column=0, row=9, rowspan=11, padx=(16,0), pady=8, sticky=W)
l6.grid(column=1, columnspan=6, row=9, sticky=W+S, padx=(8,0))
l7.grid(column=1, columnspan=6, row=10, sticky=W+N, padx=(8,0))
l8.grid(column=1, columnspan=6, row=11, sticky=W+N, padx=(8,0))

all_titles()

pgrm.mainloop()

