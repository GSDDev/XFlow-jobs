# <!---------------------------
# Name: tToolkit
# File: tToolkit.py
# -----------------------------
# Author: Gabo
# Data:   7/7/2023, 12:17:16
# ---------------------------->
import csv
import datetime, os, re
from PIL import Image
from sys import platform
from chardet import detect
import openpyxl
from pynput.keyboard import Controller
import glob, subprocess, psutil, win32gui
import sys
import urllib.request
import pyperclip
import win32com.client
import time, clipboard
import xlwings as xw
import pandas as pd
# sys.path.insert(1, r'C:\Users\rgdirlea\PycharmProjects\pyAutomation\Tools')
sys.path.insert(1, r'..\Tools')
from tFiles import *
from tImageSearch import *
from tSql import *
#from win32gui import GetWindowText,GetForegroundWindow,GetCursorInfo

hotKeys2 = ['shift up','shift down','ctrl up','ctrl down','alt up','alt down']
hotKeys = ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']

def get_encoding_type(file):
    with open(file, 'rb') as f:
        rawdata = f.read()
    return detect(rawdata)['encoding']

def csv_to_dataFrame(csv_file,encoding=None,on_bad_lines=None,engine=None):
	s_time_chunk = time.time()
	if (encoding is None):
		encoding = get_encoding_type(csv_file)
	chunk = pd.read_csv(csv_file, encoding=encoding, sep=";", engine=engine, on_bad_lines=on_bad_lines)
	e_time_chunk = time.time()
	print("with chunks: ", (e_time_chunk-s_time_chunk), " sec..")
	return chunk

def CsvToExcel(csv_file,dtype=None):
	try:
		xlsx_path = os.path.split(csv_file)
		xlsx_path = str(xlsx_path[0]) + "\\" + str(xlsx_path[1]).replace(".csv",".xlsx")
		wb = xw.Book(csv_file)  # Open an existing Workbook
		wb.save(xlsx_path)
		killProcess(["Excel.exe"])

		# xlsx_path = os.path.split(csv_file)
		# xlsx_path = str(xlsx_path[0]) + "\\" + str(xlsx_path[1]).replace(".csv",".xlsx")
		# data = pd.read_csv(csv_file, encoding=get_encoding_type(csv_file), sep=";") 
		# data = data.groupby(lambda x: data['research_id'][x]).first() 
		# writer = pd.ExcelWriter(xlsx_path,engine='xlsxwriter')
		# data.to_excel(writer) 
		# writer.save()

		# read_file = pd.read_csv(csv_file, encoding=get_encoding_type(csv_file), sep=";", dtype=dtype)
		# print(read_file.dtypes)
		# xlsx_path = os.path.split(csv_file)
		# xlsx_path = str(xlsx_path[0]) + "\\" + str(xlsx_path[1]).replace(".csv",".xlsx")
		# read_file.to_excel(xlsx_path, index = None)
		return xlsx_path
	except Exception as e:
		raise Exception('No se ha podido convertir el fichero csv a excel.')

def runExe(path, param=None, timeout=5):
	path = str(path).strip()
	if isFile(path):
		if param:
			subprocess.Popen([path,param], shell=False, stdout=subprocess.PIPE, cwd=getFileDirName(path))
		else:
			subprocess.Popen([path], shell=False, stdout=subprocess.PIPE, cwd=getFileDirName(path))
		 ## Wait for date to terminate.##
		if not waitProcess(processName=getFileName(path), time_out=timeout):
			raise Exception('El proceso ', getFileName(path) ,' no se ha iniciado durante el tiempo de espera:', timeout)
	else:
		raise Exception('El fichero', path ,'no existe o no es un fichero.')
   
def runExeShell(path, timeout=5, args=None):
	path = str(path).strip()
	## Wait for date to terminate.##
	if isFile(path):
		 
		file_path = getFileDirName(path).replace("\\", "\\\\")
		file_name = getFileName(path)
		
		myCmd = 'cd ' + file_path + ' && start ' + file_name

		# si hay algun argumento lo vamos a lanzar con argumento en caso contrario se lanzara normal
		if args:
			os.system(myCmd + " " + args)
		else:
			os.system(myCmd)
		
		## Wait for date to terminate.##
		if not waitProcess(getFileName(path), timeout):
			raise Exception('El proceso ', getFileName(path) ,' no se ha iniciado durante el tiempo de espera:', timeout)
	else:
		raise Exception('El fichero', path ,'no existe o no es un fichero.')

def runCmd(path, timeout=5):
	path = str(path).strip()
	# run the path in cmd
	os.system(path)

# enviamos palabras o especiales
def sendKeys(keys, delay_between_sends=0, repeated=1, mode="pegando"):
	if not isinstance(keys, list):
		raise Exception('Error: Send Keys: la lista de keys se tiene que pasar como lista.')
	shell = win32com.client.Dispatch("WScript.Shell")
	for key in keys:
		if (str(key).strip().upper() == 'NONE'):
			continue
		elif key in hotKeys:
			for i in range(repeated):
				pyautogui.hotkey(key)
				if delay_between_sends > 0:
					time.sleep(delay_between_sends)
		elif key in hotKeys2:
			if "up" in key:
				pyautogui.keyUp(str(key).split()[0])
			elif "down" in key:
				pyautogui.keyDown(str(key).split()[0])
			
			if delay_between_sends > 0:
				time.sleep(delay_between_sends)
		else:
			for i in range(repeated):
				# no acceptan accentos!
				# shell.SendKeys(key)
				# pyautogui.write(key)
				if "pegando" in mode:
					pyperclip.copy(key)
					time.sleep(2)
					pyautogui.hotkey("ctrl", "v")
					time.sleep(1.5)
					pyperclip.copy("")
				else:
					pyautogui.write(key)
				# Controller().type(key)
				if delay_between_sends > 0:
					time.sleep(delay_between_sends)

# esperar proceso en memoria
def waitProcess(processName,time_out = 5):
	timeout = time.time() + time_out
	while time.time() < timeout:
		if processExist(processName):
			return True
	return False

# se comrueba si el proceso existe
def processExist(processName):
	#Iterate over the all the running process
	for proc in psutil.process_iter():
		# Check if process name contains the given name string.
		if processName.lower() in proc.name().lower():
			return True
	return False

def killProcess(processes=[]):
	for process in processes:
		try:
			os.system("taskkill /f /im " + process)
		except Exception as e:
			print(e)
		
def clickButton(offset_X, offset_Y, type_click_button, clicks):
	if (pyautogui.position() == (offset_X,offset_Y)):
		pyautogui.click(x=offset_X+1,y=offset_Y+1,button=type_click_button, clicks=clicks, interval=0.25)
	else:
		pyautogui.click(x=offset_X,y=offset_Y,button=type_click_button, clicks=clicks, interval=0.25)  ## triple-click the right mouse button with a quarter second pause in between clicks

def imageClick(images, image_folder, init_X=0, init_Y=0, offset_X=0, offset_Y=0, clicks=1, action="left", time_out=5):
	
	# se buscan la/s imagenes devolviendo la posicion, nombre de la imagen encontrada
	res = image_search(images=images, image_folder=image_folder, init_x=init_X, init_y=init_Y, time_out=time_out)

	if res:
		# ponemos un tiempo antes de hacer el clic
		time.sleep(3)
		click_image(image_location=res, timestamp=1,action=action, offsetX=offset_X, offsetY=offset_Y, num_of_click=clicks)
		return True
	else:
		return False

def colorClick(color, region=None, init_X=0, init_Y=0, offset_X=0, offset_Y=0, clicks=1, action="left", time_out=5):
	res = buscar_pixel_color(color,region)

	if res:
		click_image(image_location=res, timestamp=0.1,action=action, offsetX=offset_X, offsetY=offset_Y, num_of_click=clicks)
		return True
	else:
		return False

def colorWait(color, region=None):
	res = buscar_pixel_color(color,region)

	if res:
		return True
	else:
		return False

def imageWait(images,image_folder, init_x=0, init_y=0, fin_x=None, fin_y=None, time_out=5, grayscale=False):
	# se buscan la/s imagenes devolviendo la posicion, nombre de la imagen encontrada
	res = image_search(images=images, image_folder=image_folder, init_x=init_x, init_y=init_y, fin_x=fin_x, fin_y=fin_y, time_out=time_out, grayscale=grayscale)
	if res:
		return True
	else:
		return False

def buscar_pixel_color(color_objetivo, region=None):
    # 255, 150, 50 (Naranja busqueda)
    if region is None:
        # Captura la pantalla completa si no se proporciona una región específica
        captura = pyautogui.screenshot()
    else:
        # Captura la región específica de la pantalla
        captura = pyautogui.screenshot(region=region)

    imagen = Image.frombytes('RGB', captura.size, captura.tobytes())

    # Busca el píxel de color_objetivo en la imagen
    for x in range(imagen.width):
        for y in range(imagen.height):
            pixel = imagen.getpixel((x, y))
            if pixel == color_objetivo:
                return [x,y]

    # Si no se encuentra el color objetivo, retorna False
    return False

# esperamos la ventana 
def waitWindow(win_title = [], time_out=5, moveMouse=False):
   
	start_time = time.time()
    
	while time.time() - start_time < time_out:
		for text in win_title:
			active_window_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

			if active_window_title in text:
				return active_window_title
			
			if (moveMouse):
				iniX, iniY = pyautogui.position()
				clickButton(1,1,"LEFT",0)	#; mueve el ratón arriba izquierda pantalla
				clickButton(iniX,iniY,"LEFT",0)	#; devuelve el ratón a su posición original
			time.sleep(1)  # Esperar un segundo antes de verificar nuevamente
    
	return False
#Doc : https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-loadcursora
def waitCursor(time_out=1):
	timeout = time.time() + time_out
	
	#while time.time() < timeout:
		# la posicion 1 del get curosr info nos indica el estado del curosr el 32514 indica que el estado del curosr es IDC_WAIT (Hourglass)
	#    if GetCursorInfo()[1] != 32514:
	#        break


# devuleve todos los ficheros que coincida con la/s extensiones pasadas por parametros
# por defecto devuleve todos los ficheros que tienen una extension 
def getFiles_Extension(dir_path, extencion=['']):
	if not isinstance(extencion, list):
		raise Exception('Extencion: Los criterios se tiene/n que pasar como una lista.')
	list_extencion = []
	if not isDir(dir_path):
			raise Exception('La ruta', dir_path ,'no es un directorio.')
		
	for filename in os.listdir(dir_path):
		for ext in extencion:
			if filename.endswith(ext) and isFile(os.path.join(dir_path, filename)): 
				list_extencion.append(os.path.join(dir_path, filename))
	return list_extencion

# devuleve todos los ficheros que coincida con los criterios pasadas por parametros
def getFiles_FileName(dir_path, criterials=['*.*']):
	if not isinstance(criterials, list):
		raise Exception('Criterials: Los criterios se tiene/n que pasar como una lista.')
	list_files = []
	for citerial in criterials:
		list_files.append(glob.glob(os.path.join(dir_path, citerial)))
	return list_files

# pasamos el string y devolvemos una lista de los valores separados segun el criterio
def splitString(string_to_split, criterial):
	return string_to_split.split(criterial)

def writeLog(text,log_file):
	if isFile(log_file) and fileExists(log_file):
		with open(log_file, 'a+') as f:
			f.write(text + '\n')
			print(text)
			f.close
	else:
		pathFileLog = os.path.split(log_file)[0]
		if (not os.path.isdir(pathFileLog)):
			os.makedirs(pathFileLog)
		with open(log_file, 'x') as f:
			f.write(text + '\n')
			print(text)
			f.close

def copyToClipboard():
	retries = 1
	while (retries < 50):
		shell = win32com.client.Dispatch("WScript.Shell")
		shell.SendKeys("^c")
		time.sleep(0.3)
		string_copied = clipboard.paste()
		if string_copied.strip():
			return string_copied
		retries += 1
	return

def TimeStamp(format = "%d/%m/%Y %H:%M:%S"):
	now = datetime.datetime.now()
	return now.strftime(format)

def screenShoot(parameters = ""):
	dirScreenShoot = parameters['snapFolder'] if 'snapFolder' in parameters else os.getcwd() + "\\snapshots"
	fileName = parameters['fileName'] if 'fileName' in parameters else ""
	
	if (not os.path.isdir(dirScreenShoot)):
		os.makedirs(dirScreenShoot)

	myScreenshot = pyautogui.screenshot()
	image = dirScreenShoot + "\\" + TimeStamp("%d%m%Y%H%M%S") + "_" + fileName + ".png"
	myScreenshot.save(image)
	myScreenshot.save(dirScreenShoot + "\\..\\..\\..\\screenshot.png")
	
	#hacemos una vista en miniatura para jenkins
	img = Image.open(dirScreenShoot + "\\..\\..\\..\\screenshot.png")
	SIZE = (25, 25)
	img.thumbnail(SIZE)
	img.save(dirScreenShoot + "\\..\\..\\..\\screenshot-thumb.png")
	print("Se ha guardado la imagen:", image)
	return image
	
def actualizarScreenShoot(parameters = ""):
	dirScreenShoot = parameters['snapFolder'] if 'snapFolder' in parameters else os.getcwd() + "\\snapshots"
	myScreenshot = pyautogui.screenshot()
	myScreenshot.save(dirScreenShoot + "\\..\\..\\..\\screenshot.png")
	
	#hacemos una vista en miniatura para jenkins
	img = Image.open(dirScreenShoot + "\\..\\..\\..\\screenshot.png")
	SIZE = (25, 25)
	img.thumbnail(SIZE)
	img.save(dirScreenShoot + "\\..\\..\\..\\screenshot-thumb.png")

def ChangeResolution(parameters = ""):
	pass
	# ; Comprueba la resoluci�n de la pantalla y la cambia si no se corresponde
	# ;
	# ; Ejemplo:
	# ; 	ChangeResolution({screenWidth:800, screenHeight:600})
	# ;
	# ; Par�metros:
	# ; screenWidth: ancho de la pantalla
	# ; screenHeight: alto de la pantalla

	# if (not 'screenWidth' in parameters or not 'screenHeight' in parameters):
	# 	raise Exception('screenWidth y screenHeight tienen que estar rellenos.')

	# devmode = pywintypes.DEVMODEType()
	# devmode.PelsWidth = parameters['screenWidth']
	# devmode.PelsHeight = parameters['screenHeight']

	# devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

	# win32api.ChangeDisplaySettings(devmode, 0)

def parseBoolean(value):
# ; devuelve true / false seg�n el valor de la variable pasada por par�metro
# ; si no es ninguno de los valores contemplados, devuelve vac�o
	boolValue = {}

	boolValue['True'] = True
	boolValue['true'] = True
	boolValue['verdadero'] = True
	boolValue['si'] = True
	boolValue['sí'] = True
	boolValue['yes'] = True
	boolValue['1'] = True
	boolValue['ok'] = True
	boolValue['vale'] = True
	boolValue['venga'] = True

	boolValue['None'] = False
	boolValue['false'] = False
	boolValue['falso'] = False
	boolValue['no'] = False
	boolValue['nop'] = False
	boolValue['nein'] = False
	boolValue['0'] = False
	
	if (value in boolValue):
		return boolValue[value]
	else:
		raise Exception("No se encuentra " + value)

def extract_version_registry(output):
    try:
        google_version = ''
        for letter in output[output.rindex('DisplayVersion    REG_SZ') + 24:]:
            if letter != '\n':
                google_version += letter
            else:
                break
        return(google_version.strip())
    except TypeError:
        return

def extract_version_folder():
    # Check if the Chrome folder exists in the x32 or x64 Program Files folders.
    for i in range(2):
        path = 'C:\\Program Files' + (' (x86)' if i else '') +'\\Google\\Chrome\\Application'
        if os.path.isdir(path):
            paths = [f.path for f in os.scandir(path) if f.is_dir()]
            for path in paths:
                filename = os.path.basename(path)
                pattern = '\d+\.\d+\.\d+\.\d+'
                match = re.search(pattern, filename)
                if match and match.group():
                    # Found a Chrome version.
                    return match.group(0)

    return None

def get_chrome_version():
    version = None
    install_path = None

    try:
        if platform == "linux" or platform == "linux2":
            # linux
            install_path = "/usr/bin/google-chrome"
        elif platform == "darwin":
            # OS X
            install_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
        elif platform == "win32":
            # Windows...
            try:
                # Try registry key.
                stream = os.popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
                output = stream.read()
                version = extract_version_folder()
            except Exception as ex:
                # Try folder path.
                version = extract_version_registry(output)
    except Exception as ex:
        print(ex)
    version = os.popen(f"{install_path} --version").read().strip('Google Chrome ').strip() if install_path else version
    return version

def get_chromeDrive_version():
	version = str(get_chrome_version()).split(".")
	return urllib.request.urlopen("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + version[0] +"."+ version[1] +"."+ version[2]).read().decode()

def FolderFromFile(fileFullPath):
	# ; Obtiene el directorio a partir de un la ruta completa de un fichero pasado como parámetro añadiéndole / en caso de no ser el último carácter del directorio
	# ;
	# ; Parámetros:
	# ; - fileFullPath: Ruta y nombre del fichero

	# ;Se realizan las comprobaciones necesarias y se pasan los parámetros a variables
	if (not isinstance(fileFullPath,str)):
		raise Exception("No se ha especificado el parámetro [fileFullPath] necesario para obtener el directorio")

	dir = os.path.dirname(fileFullPath)
	if (not dir.endswith("\\")):
		dir += "\\"

	return dir

def CalculateBusinessDay(server="BARPPVGNUFSQL1N\SQLEXPRESS",database="VIKING",port="1433",user="User_AutoHotKey",passw="VkHku_22ow",gapDays=0,baseDate=datetime.datetime.now(),loc=False,processCode=""):
# ; Calcula el anterior/siguiente día laborable en relación a una fecha
# ;
# ; Ejemplo:
# ; 	CalculateBusinessDay({baseDate: 20181130, gapDays: -3, loc: 1})
# ;
# ; Parámetros:
# ; baseDate: fecha base en relación a la que realizar el cálculo (por defecto día en curso)
# ; gapDays: desfase en días (integer) a retroceder (negativo) o avanzar (positivo) para buscar el día laborable
# ; loc: localidad (1 -> Barcelona, 2 -> Madrid)
	if (gapDays == 0):
		raise Exception("Debe de especificarse la cantidad de días a avanzar o retroceder","CalculateBusinessDay","Parameters")

	if (not isinstance(baseDate,datetime.datetime)):
		raise Exception("Formato de fecha '" + str(baseDate) + "' no válido.","CalculateBusinessDay","Parameters")
	
	if (processCode == ""):
		raise Exception("El processCode no puede estar vacio.","CalculateBusinessDay","Parameters")

	# ;Creamos la conexión a base de datos y la query
	objSql = SQL(user=user,passw=passw,server=server,port=port,database=database,processCode=processCode)
	query = "EXEC [LocalizacionesCalendarioObtenerFestivos] " + str(loc) + "," + str(baseDate.year)
	objSql.runQuery(query)
	holidays = objSql.getCursor()
	
	# ;Quitamos los festivos locales si no se ha especificado localidad
	if (not isinstance(loc,int)):
		for key, holiday in holidays:
			if (holiday[4] != 0):
				holidays.remove(key)

	outDate = baseDate
	moveDay = -1 if gapDays < 0 else 1 # ;Comprobamos si hay que retroceder o avanzar días
	gapDays = abs(gapDays) # ;Quitamos el signo
	businessDays = 0

	while (gapDays > businessDays): # ;Hasta que se hayan avanzado/retrocedido los días laborables indicados
		outDate = outDate + datetime.timedelta(moveDay)
		if (outDate.weekday() == 5 or outDate.weekday() == 6):
			continue # ;Avanzamos/retrocedemos sin aumentar el contador de días laborables

		for holyday in holidays:
			if (outDate.strftime("%Y%m%d") == holyday[0]):
				continue

		businessDays += 1
	
	return outDate
