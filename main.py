import pytesseract
import pyautogui
import keyboard
import time
from PIL import Image, ImageEnhance
from fuzzywuzzy import fuzz
from threading import Thread
import os
act = False
last_time = 0
crates = 0

def click():
	pyautogui.mouseDown()
	time.sleep(0.01)
	pyautogui.mouseUp()


def take_screen():
	pressed = False
	while True:
		# if not pressed and act:
		# 	time.sleep(3)
		# 	pyautogui.moveTo(x=(1920/2)-1, y=1080/2+170)
		# 	click()
		# 	pressed = True
		if act:
			m_pos = pyautogui.position()
			try:
				pyautogui.screenshot('screenshot.png', region=(m_pos[0]-100, m_pos[1]-75, 200, 50))
			except PermissionError:
				continue
			Thread(target=word_detect).start()
		time.sleep(0.15)


def word_detect():
	global last_time, crates
	# img = ImageEnhance.Contrast(ImageEnhance.Brightness(Image.open("screenshot.png").convert("L")).enhance(0.2)).enhance(1 + (100 / 100))
	img = ImageEnhance.Brightness(Image.open("screenshot.png").convert("L")).enhance(0.2)
	# word_psm7 = pytesseract.image_to_string(img, config="--psm 7")
	psm = " ".join(pytesseract.image_to_string(img,lang="eng", config="--psm 6").splitlines())
	# print(psm)
	# if (fuzz.partial_ratio(word_psm6.lower(), 'crate') > 66 and fuzz.WRatio(word_psm6, 'crate') > 10) or (fuzz.partial_ratio(word_psm7.lower(), 'crate') > 66  and fuzz.WRatio(word_psm7, 'crate') > 10):
	for word in psm.split()[::-1]:
		if fuzz.ratio(word.lower(), 'create') > 70 and time.time() - last_time > 2:
			last_time = time.time()
			crates+=1
			print('Crate has been found')
			for i in range(2):
				click()
				time.sleep(0.5)
				pyautogui.moveTo(x=(1920/2)-1, y=1080/2+170)
			print("Rod has been dropped")
			os.remove("screenshot.png")
			return
	if fuzz.ratio(psm.lower(), 'create') > 75 and time.time() - last_time > 2:
		last_time = time.time()
		crates+=1
		for i in range(2):
			click()
			time.sleep(0.5)
			pyautogui.moveTo(x=(1920/2)-1, y=1080/2+170)


def check_sonar():
	while True:
		if act:
			sonar = pyautogui.locateOnScreen('Sonar.png', confidence=0.4, region=(38, 100, 500, 50))
			# print(f"{sonar=}")
			if sonar == None:
				dynamic_jobs.append(drink_potion_sonar)
		time.sleep(10)


def check_fishing():
	while True:
		if act:
			fishing = pyautogui.locateOnScreen('Fishing.png', confidence=0.4, region=(38, 100, 500, 50))
			# print(f"{fishing=}")
			if fishing == None:
				dynamic_jobs.append(drink_potion_fishing)
		time.sleep(11)


def drink_potion_sonar():
	pyautogui.keyDown('8')
	time.sleep(0.01)
	pyautogui.keyUp('8')
	pyautogui.moveTo(x=(1920/2)-1, y=1080/2+170)
	print("Sonar potion has been drunk")
	click()


def drink_potion_fishing():
	pyautogui.keyDown('9')
	time.sleep(0.01)
	pyautogui.keyUp('9')
	pyautogui.moveTo(x=(1920/2)-1, y=1080/2+170)
	print("Fishing potion has been drunk")
	click()


def take_rod():
	pyautogui.keyDown('7')
	time.sleep(0.01)
	pyautogui.keyUp('7')
	pyautogui.moveTo(x=(1920/2)-1, y=1080/2+170)
	print("Rod has been taken and dropped!")
	click()

		
def crates_counter():
	while True: 
		if act:
			print("Crates were caught: ", crates)
			time.sleep(14)
		time.sleep(1)


dynamic_jobs=[]
first_rod = True
def new_job_finder():
	time.sleep(1)
	global dynamic_jobs, first_rod
	while True:
		if act and dynamic_jobs:
			for i in dynamic_jobs:
				i()
				time.sleep(0.5)
				dynamic_jobs.remove(i)
			take_rod()
			first_rod=False
		if act and first_rod:
			take_rod()
			first_rod=False
		time.sleep(1)


def pause():
	global act
	if act:
		act = False
		print("Paused")
	else:
		act = True
		print("Started")


def main():
	global act
	jobs = [take_screen, check_sonar, crates_counter, check_fishing, new_job_finder]
	# jobs = [check_sonar]
	for i in jobs:
		Thread(target=i).start()
	keyboard.add_hotkey("ctrl+alt+j", pause)
	input()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		os._exit(0)