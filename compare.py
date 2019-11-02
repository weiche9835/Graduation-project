import tkinter as tk
import cv2
import numpy
import time
import imagehash
import hashlib
import web3

from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
from PIL import Image
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract

class Application(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		
	def createWidgets(self):	
		self.label = tk.Label(self)
		self.label["text"] = "Welcome to compare program"
		#self.label["bg"] = "#a6ffff"
		self.label["font"] = ('Times New Roman bold', 30)
		self.label.pack(fill='x',pady=20)
	
		self.label1 = tk.Label(self)
		self.label1["text"] = "Step 1. : Input your account"
		self.label1["bg"] = "#FFE4C4"
		self.label1["font"] = ('Arial bold', 18)
		self.label1.pack(fill='x',padx=10)
		
		self.Combo1 = ttk.Combobox(self)
		self.Combo1["values"]=["",w3.eth.accounts[0],w3.eth.accounts[1],w3.eth.accounts[2]]
		self.Combo1["font"] = ('Arial', 18)
		self.Combo1.current(3)
		self.Combo1.pack(fill='x',padx=10,pady=10)
		
		'''
		self.text1 = tk.Text(self)
		self.text1["height"] = 1
		self.text1["width"] = 50
		self.text1["font"] = ('Arial', 18)
		self.text1.insert(1.0,w3.eth.accounts[2])
		self.text1.pack(fill='x',padx=10,pady=10)
		'''
		
		self.label2 = tk.Label(self)
		self.label2["text"] = "Step 2. : Input your video(e.g.1567163656)"
		self.label2["bg"] = "#FFE4C4"
		self.label2["font"] = ('Arial bold', 18)
		self.label2.pack(fill='x',padx=10)
		
		fm0 =  tk.Frame(self)
		fm0.pack(fill='x',expand='yes',padx=10,pady=10)
		
		self.text2 = tk.Text(fm0)
		self.text2["height"] = 1
		self.text2["width"] = 50
		self.text2["font"] = ('Arial', 18)
		self.text2.insert(1.0,'1567163656')
		self.text2.pack(fill='x',side='left',padx=10,pady=10)
		
		self.button0 = tk.Button(fm0)
		self.button0["text"] = "Select File"
		self.button0["command"] = self.selectFile
		self.button0.pack(fill='x',side='left',ipadx=10,padx=10)
		
		fm1 = tk.Frame(self)
		fm1.pack(fill='x',expand='yes',padx=10,pady=10)
		
		self.button1 = tk.Button(fm1)
		self.button1["text"] = "Compare"
		self.button1["command"] = self.compare
		self.button1.pack(fill='x',side='left',ipadx=160,padx=10)
		
		self.button2 = tk.Button(fm1)
		self.button2["text"] = "Cancel"
		self.button2["command"] = self.cancel
		self.button2.pack(fill='x',side='left',ipadx=160,padx=10)
		
		fm2 = tk.Frame(self)
		fm2.pack(fill='x',expand='yes',padx=10,pady=10)
		
		self.label2 = tk.Label(fm2)
		self.label2["text"] = "video"
		self.label2["bg"] = "#FFE4C4"
		self.label2["font"] = ('Arial bold', 18)
		self.label2.pack(fill='x',side='left',ipadx=155,padx=10)
		
		self.label2 = tk.Label(fm2)
		self.label2["text"] = "block"
		self.label2["bg"] = "#FFE4C4"
		self.label2["font"] = ('Arial bold', 18)
		self.label2.pack(fill='x',side='left',ipadx=155,padx=10)
		
		fm3 = tk.Frame(self)
		fm3.pack(fill='x',expand='yes',padx=10,pady=10)
		
		self.text3 = tk.Text(fm3)
		self.text3["height"] = 8
		self.text3["width"] = 25
		self.text3["font"] = ('Arial', 18)
		self.text3.pack(fill='x',side='left',padx=30,pady=10)
		
		self.text4 = tk.Text(fm3)
		self.text4["height"] = 8
		self.text4["width"] = 25
		self.text4["font"] = ('Arial', 18)
		self.text4.pack(fill='x',side='left',padx=30,pady=10)
		
	def selectFile(self):
		filepath =  filedialog.askopenfilename(initialdir = "C:/Users/USER/Desktop/畢業專題/demo/finish",title = "Select file",filetypes = (("avi files","*.avi"),("all files","*.*")))
		filename = filepath[37:-4]
		empty = ""
		if filename != empty:
			self.text2.delete(1.0,tk.END)
			self.text2.insert(tk.END,filename)
	def cancel(self):
		#self.text1.delete(1.0,tk.END)
		self.text2.delete(1.0,tk.END)
		self.text3.delete(1.0,tk.END)
		self.text4.delete(1.0,tk.END)
		self.Combo1.current(0)
	def showstr(self,string):
		self.text3.insert(tk.END,string)
	def compare(self):
		counttext3 = 1
		counttext4 = 1
		def showStrInText3(string):
			self.text3.insert(tk.END,string)
		def showStrInText4(string):
			self.text4.insert(tk.END,string)
		#var3 = self.text1.get(1.0,tk.END)
		var = self.Combo1.get()
		var2 = self.text2.get(1.0,tk.END)
		# text get 會抓到換行符號,strip() 去除特殊符號
		print(var.strip() + " " + var2.strip())
		a1 = var.strip()
		try:
			Vname = str(var2.strip()) + '.avi'
			now = int(Vname[0:10])
			blockNumber = int(Vname[11:-4])
			flag = False
			i=1
			# 開啟網路攝影機
			cap = cv2.VideoCapture(Vname)

			# 初始化
			x=0
			ret, frame = cap.read()

			# 創建一個黑屏
			e = numpy.zeros(frame.shape,numpy.uint8)
			e.fill(0)
			gray2 = cv2.cvtColor(e, cv2.COLOR_BGR2GRAY)
			avg = cv2.blur(frame, (5, 5))
			
			# 找到對應開始的區塊
			if w3.eth.getBlock(blockNumber):
				if w3.eth.getBlockTransactionCount(blockNumber) != 0:
					block=w3.eth.getTransactionByBlock(blockNumber,0)
					blockFromAddr = block['from']
					if blockFromAddr == accountname:
						#print("block " + str(i) + " : "  + str(contract.functions.getInfo().call(block_identifier = i)))
						if contract.functions.getInfo().call(block_identifier = blockNumber)[1]==now:
							pass
			blockNumber=blockNumber+1
			# 比較第一幀是否相同
			
			image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
			hash = imagehash.average_hash(image,hash_size=8)
			showStrInText3(str(counttext3) + " : " + str(hash)+"\n")
			counttext3 = counttext3 + 1
			if w3.eth.getBlock(blockNumber):
				blockinfo = str(contract.functions.getInfo().call(block_identifier = blockNumber)[0])
				showStrInText4(str(counttext4) + " : " + blockinfo+"\n")
				counttext4 = counttext4 + 1
				if contract.functions.getInfo().call(block_identifier = blockNumber)[0]==str(hash):
					flag=True
				else:
					flag=False
			blockNumber=blockNumber+1
			# 比較第二幀以後的每一幀
			while(cap.isOpened()):
				if not flag:
					break
				# 讀取一幅影格
				ret, frame = cap.read()
				x=x+1
				# 若讀取至影片結尾，則跳出
				if ret == False:
					break

				# 模糊處理
				blur = cv2.blur(frame, (5, 5))
			  
				# 計算目前影格與平均影像的差異值
				diff = cv2.absdiff(avg, blur)

				# 將圖片轉為灰階
				gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

				# 閥值處理 25以下為0 25以上為255
				ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

				kernel = numpy.ones((10, 10), numpy.uint8)
				
				# 型態轉換
				thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
				thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
				
				# 顯示
				cv2.imshow('show',diff)
				
				# 使用幀差法比較是否相同
				if not(gray2==thresh).all():
					image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
					hash = imagehash.average_hash(image,hash_size=8)
					showStrInText3(str(counttext3) + " : " + str(hash)+"\n")
					counttext3 = counttext3 + 1
					
					if w3.eth.getBlock(i,0):
						blockinfo = str(contract.functions.getInfo().call(block_identifier = blockNumber)[0])
						showStrInText4(str(counttext4) + " : " + blockinfo + "\n")
						counttext4 = counttext4 + 1
						
						if contract.functions.getInfo().call(block_identifier = blockNumber)[0]==str(hash):
							flag=True
						else:
							flag=False
					else:
						blockNumber=blockNumber-1
						showStrInText4(str(counttext3) + " : " + str(contract.functions.getInfo().call(block_identifier = i)[0]) + "\n")
						counttext4 = counttext4 + 1
						
						if contract.functions.getInfo().call(block_identifier = blockNumber)[0]==str(hash):
							flag=True
						else:
							flag=False
					blockNumber=blockNumber+1
			  # 顯示偵測結果影像
			  #cv2.imshow('frame', frame)
				now=now+1
				if cv2.waitKey(1) and 0xFF == ord('q'):
					break
			if flag==True:
				showinfo("Result","This video did not be changed.")
			else:
				showinfo("Result","Oops , This video have been changed.")
			cap.release()
			cv2.destroyAllWindows()
		except:
			showinfo("Error","Oops , an error has occurred")


# 連結 Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
# 合約內容
abi = [
	{
		"constant": False,
		"inputs": [
			{
				"name": "_pichash",
				"type": "string"
			},
			{
				"name": "_time",
				"type": "uint256"
			}
		],
		"name": "setInfo",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"name": "pichash",
				"type": "string"
			},
			{
				"indexed": False,
				"name": "time",
				"type": "uint256"
			}
		],
		"name": "Instructor",
		"type": "event"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getInfo",
		"outputs": [
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
]

address = '0x0a5Af3AAc9699E8FEC9C17B6a3006680dEe20eb6'
contract = w3.eth.contract(address = address,abi=abi)

accountname = w3.eth.accounts[2]
		
root = tk.Tk()
root.title("Compare GUI")
root.geometry('800x600')
root.resizable(0,0)
app = Application(root)
root.mainloop()