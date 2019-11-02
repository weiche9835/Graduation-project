import cv2
import numpy
import time
import imagehash
import hashlib
import json
import web3

from PIL import Image
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract


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
w3.eth.defaultAccount = w3.eth.accounts[2]
contract = w3.eth.contract(address = address,abi=abi)

blocknumber = w3.eth.blockNumber

# 選擇第一隻攝影機
cap = cv2.VideoCapture(0)


# 抓取攝像頭的基本資料

width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fourcc = cv2.VideoWriter_fourcc(*'HFYU')

ret, frame = cap.read()
time.sleep(2)

#創建一個黑屏
e = numpy.zeros(frame.shape,numpy.uint8)
e.fill(0)
gray2 = cv2.cvtColor(e, cv2.COLOR_BGR2GRAY)


while(True):
	x=0

	name = int(time.time())
	vedioName = str(name) + "_" + str(blocknumber) + '.avi'
	out = cv2.VideoWriter(vedioName, fourcc, 1.0, (int(width), int(height)))
	
	ret, frame = cap.read()
	avg = cv2.blur(frame, (5, 5))
	out.write(frame)
	image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
	hash = imagehash.average_hash(image,hash_size=8)
	print("hash = " + str(hash) + '	' + str(int(name)))
	tx_hash = contract.functions.setInfo(str(hash),int(name)).transact()
	# 從攝影機擷取一張影像
	try:
		while(x<3600):
			start = time.time()
			ret, frame = cap.read()
			x=x+1
			out.write(frame)

			if ret == False:
				break
		
	  # 模糊處理
			blur = cv2.blur(frame, (5, 5))
	  
	  # 計算目前影格與平均影像的差異值
			diff = cv2.absdiff(avg, blur)
			
			cv2.imshow("show",frame)
	  # 將圖片轉為灰階
			gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

			ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
			kernel = numpy.ones((10, 10), numpy.uint8)
	  
			thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
			thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
	  #cv2.imshow('asdasdasd',thresh)
			if not(gray2==thresh).all():
		# numpy 轉換成 PIL 對象
				image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
		# PIL 圖片 hash
				hash = imagehash.average_hash(image,hash_size=8)
				print("hash = " + str(hash) + '	' + str(int(start)))
				tx_hash = contract.functions.setInfo(str(hash),int(start)).transact()
	  
			end = time.time()
			delay = 1 - (end - start)
			if delay>0:
				time.sleep(delay)
	  # 若按下 q 鍵則離開迴圈
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
	except:
		print("Exceptions : Ctrl+C ")
		break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()