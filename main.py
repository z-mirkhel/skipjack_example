# https://csrc.nist.gov/csrc/media/projects/cryptographic-algorithm-validation-program/documents/skipjack/skipjack.pdf

from tkinter import *
from tkinter import ttk
import random

class SkipJack:
	def __init__(self):
		# F is an 8-bit S-box
		self.F = []
		self.defineF()
		# w1, w2, w3, w4 are 16-bit integers
		self.w1 = 0
		self.w2 = 0
		self.w3 = 0
		self.w4 = 0


	# plaintext is a 64-bit integer
	# key is a list of 10-bytes
	def encrypt(self, plaintext, key):
		self.splitWord(plaintext)

		for round in range (1, 33):
			if (1 <= round <= 8) or (17 <= round <= 24):
				self.A(round, key)
				self.printStatus(round)
			if (9 <= round <= 16) or (25 <= round <= 32):
				self.B(round, key)
				self.printStatus(round)

		return self.appendWords()


	# ciphertext is a 64-bit integer
	# key is a list of 10-bytes
	def decrypt(self, ciphertext, key):
		self.splitWord(ciphertext)

		for round in reversed(range(1, 33)):
			if (25 <= round <= 32) or (9 <= round <= 16):
				self.Binv(round, key)
			if (17 <= round <= 24) or (1 <= round <= 8):
				self.Ainv(round, key)

		return self.appendWords()


	def A(self, round, key):
		c1 = self.w1
		c2 = self.w2
		c3 = self.w3
		self.w1 = self.G(round, key, c1) ^ self.w4 ^ round
		self.w2 = self.G(round, key, c1)
		self.w3 = c2
		self.w4 = c3


	def Ainv(self, round, key):
		c1 = self.w1
		c2 = self.w2
		self.w1 = self.Ginv(round, key, c2)
		self.w2 = self.w3
		self.w3 = self.w4
		self.w4 = c1 ^ c2 ^ round


	def B(self, round, key):
		c1 = self.w1
		c2 = self.w2
		c3 = self.w3
		self.w1 = self.w4
		self.w2 = self.G(round, key, c1)
		self.w3 = c1 ^ c2 ^ round
		self.w4 = c3


	def Binv(self, round, key):
		c1 = self.w1
		self.w1 = self.Ginv(round, key, self.w2)
		self.w2 = self.Ginv(round, key, self.w2) ^ self.w3 ^ round
		self.w3 = self.w4
		self.w4 = c1


	# w is a 16-bit integer
	def G(self, round, key, w):
		g = [0] * 6
		g[0] = (w >> 8 ) & 0xff
		g[1] = w & 0xff
		j = (4 * (round - 1)) % 10

		for i in range(2, 6): # gives i = 2,3,4,5
			g[i] = self.F[g[i - 1] ^ key[j]] ^ g[i - 2]
			j = (j + 1) % 10

		return (g[4] << 8) | g[5]


	# w is a 16-bit integer
	def Ginv(self, round, key, w):
		g = [0] * 6
		g[4] = (w >> 8) & 0xff
		g[5] = w & 0xff
		j = (4 * (round - 1) + 3) % 10

		for i in reversed(range(4)): # gives i=3,2,1,0
			g[i] = self.F[g[i + 1] ^ key[j]] ^ g[i + 2]
			j = (j - 1) % 10

		return (g[0] << 8) | g[1]


	# append the four 16-bit words w1,w2,w3,w4 to return a 64-bit word
	def appendWords(self):
		x1 = self.w1 << 3 * 16
		x2 = self.w2 << 2 * 16
		x3 = self.w3 << 1 * 16
		x4 = self.w4
		return x1 | x2 | x3 | x4


	# w is a 64-bit word. This function splits w into
	# four 16-bit words which are stored in w1, w2, w3, w4
	def splitWord(self, w):
		self.w1 = (w >> (16 * 3)) & 0xffff
		self.w2 = (w >> (16 * 2)) & 0xffff
		self.w3 = (w >> (16 * 1)) & 0xffff
		self.w4 = w & 0xffff


	# print the round number and the current values of w1,w2,w3,w4
	def printStatus(self, round):
		w = self.appendWords()
		print("round=" + str(round) + "  " + hex(w))


	def defineF(self):
		self.F = [0xa3, 0xd7, 0x09, 0x83, 0xf8, 0x48, 0xf6, 0xf4, 0xb3, 0x21, 0x15, 0x78, 0x99, 0xb1, 0xaf, 0xf9,
			0xe7, 0x2d, 0x4d, 0x8a, 0xce, 0x4c, 0xca, 0x2e, 0x52, 0x95, 0xd9, 0x1e, 0x4e, 0x38, 0x44, 0x28,
			0x0a, 0xdf, 0x02, 0xa0, 0x17, 0xf1, 0x60, 0x68, 0x12, 0xb7, 0x7a, 0xc3, 0xc9, 0xfa, 0x3d, 0x53,
			0x96, 0x84, 0x6b, 0xba, 0xf2, 0x63, 0x9a, 0x19, 0x7c, 0xae, 0xe5, 0xf5, 0xf7, 0x16, 0x6a, 0xa2,
			0x39, 0xb6, 0x7b, 0x0f, 0xc1, 0x93, 0x81, 0x1b, 0xee, 0xb4, 0x1a, 0xea, 0xd0, 0x91, 0x2f, 0xb8,
			0x55, 0xb9, 0xda, 0x85, 0x3f, 0x41, 0xbf, 0xe0, 0x5a, 0x58, 0x80, 0x5f, 0x66, 0x0b, 0xd8, 0x90,
			0x35, 0xd5, 0xc0, 0xa7, 0x33, 0x06, 0x65, 0x69, 0x45, 0x00, 0x94, 0x56, 0x6d, 0x98, 0x9b, 0x76,
			0x97, 0xfc, 0xb2, 0xc2, 0xb0, 0xfe, 0xdb, 0x20, 0xe1, 0xeb, 0xd6, 0xe4, 0xdd, 0x47, 0x4a, 0x1d,
			0x42, 0xed, 0x9e, 0x6e, 0x49, 0x3c, 0xcd, 0x43, 0x27, 0xd2, 0x07, 0xd4, 0xde, 0xc7, 0x67, 0x18,
			0x89, 0xcb, 0x30, 0x1f, 0x8d, 0xc6, 0x8f, 0xaa, 0xc8, 0x74, 0xdc, 0xc9, 0x5d, 0x5c, 0x31, 0xa4,
			0x70, 0x88, 0x61, 0x2c, 0x9f, 0x0d, 0x2b, 0x87, 0x50, 0x82, 0x54, 0x64, 0x26, 0x7d, 0x03, 0x40,
			0x34, 0x4b, 0x1c, 0x73, 0xd1, 0xc4, 0xfd, 0x3b, 0xcc, 0xfb, 0x7f, 0xab, 0xe6, 0x3e, 0x5b, 0xa5,
			0xad, 0x04, 0x23, 0x9c, 0x14, 0x51, 0x22, 0xf0, 0x29, 0x79, 0x71, 0x7e, 0xff, 0x8c, 0x0e, 0xe2,
			0x0c, 0xef, 0xbc, 0x72, 0x75, 0x6f, 0x37, 0xa1, 0xec, 0xd3, 0x8e, 0x62, 0x8b, 0x86, 0x10, 0xe8,
			0x08, 0x77, 0x11, 0xbe, 0x92, 0x4f, 0x24, 0xc5, 0x32, 0x36, 0x9d, 0xcf, 0xf3, 0xa6, 0xbb, 0xac,
			0x5e, 0x6c, 0xa9, 0x13, 0x57, 0x25, 0xb5, 0xe3, 0xbd, 0xa8, 0x3a, 0x01, 0x05, 0x59, 0x2a, 0x46]


root = Tk()
root['bg'] = '#ffccde'
root.title("Алгоритм SKIPJACK")
root.geometry('650x270')
root.resizable(width=False, height=False)

# message = "Проверка работы программы"

def create_frame(label_text, yes_no_entry):
	frame = ttk.Frame(root, borderwidth=1, relief=SOLID, padding=[8, 10])
	# добавляем на фрейм метку
	label = Label(frame, text=label_text, foreground='#700038')
	label.pack(anchor=NW)
	# возвращаем фрейм из функции
	return frame

def on_change(entry):
	global message
	message = entry.widget.get()
	PT_messsage()


# example
# PT = 0x33221100ddccbbaa
# KEY = [0x00, 0x99, 0x88, 0x77, 0x66, 0x55, 0x44, 0x33, 0x22, 0x11]
sj = SkipJack()
# CT = sj.encrypt(PT, KEY)
# DT = sj.decrypt(CT, KEY)
#
# print("Plain text:" + hex(PT))
# print("Cipher text:" + hex(CT))
# print("Decrypted text:" + hex(DT)) # should match the plain text


# генерация случайного ключа
random_KEY =[]
print('KEY:', end=' ')
for i in range(0, 10):
	random_KEY.append(random.getrandbits(8))
	print(hex(random_KEY[i]), end=' ')
print('')
# получение сообщения
# разделение сообщения на символы, добавление символов в список и перевод в 64-разрядное целое число
def PT_messsage():
	global pt_message

	pt_message = []
	for x in message:
		pt_message.append(int(format(ord(x), '064b')))

def CT_message():
	global ct

	ct = []
	for mess in pt_message:
		ct.append(sj.encrypt(mess, random_KEY))

	str_ct = ''
	for c in ct:
		str_ct += hex(c)

	label1['text'] = str_ct

def DT_message():
	global str_dt

	dt = []
	for ct_mess in ct:
		dt.append(sj.decrypt(ct_mess, random_KEY))

	# перевод списка из 64-разрядных чисел в список букв и построение строки из символов полученного списка
	dt_message = []
	str_dt = ''
	for dt_mess in dt:
		dt_message.append(chr(int(str(dt_mess), 2)))

	for m in dt_message:
		str_dt += m

	label2['text'] = str_dt


# print("Plain text:", message)
# print("Cipher text:", str_ct)
# print("Decrypted text:", str_dt)

plain_frame = create_frame("Введите сообщение:", True)
entry = Entry(plain_frame)
entry.pack(anchor=NW, fill=X)
entry.bind("<Return>", on_change)
plain_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

btn = Button(root, text="Зашифровать сообщение", background='#700038', foreground='white', command=CT_message)
btn.pack()

cipher_frame = create_frame("Полученное зашифрованное сообщение:", False)
label1 = Label(cipher_frame, background='white', anchor=W, borderwidth=1, relief="sunken")
label1.pack(anchor=NW, fill=X)
cipher_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

btn = Button(root, text="Дешифровать сообщение", background='white', foreground='#700038', command=DT_message)
btn.pack()

decrypted_frame = create_frame("Полученное дешифрованное сообщение:", False)
label2 = Label(decrypted_frame, background='white', anchor=W, borderwidth=1, relief="sunken")
label2.pack(anchor=NW, fill=X)
decrypted_frame.pack(anchor=NW, fill=X, padx=5, pady=5)

root.mainloop()
