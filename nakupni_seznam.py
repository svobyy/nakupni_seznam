import os
from typing import List
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

seznam = []

soubor = "seznam.txt"


def clear_console():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')


def ukaz_napovedu(seznam):
	clear_console()
	# ovládání programu
	print("Co potřebujeme nakoupit?")
	print("""
Máš {} položek na tvém nákupním seznamu.

Zadej POMOC pro zobrazení nápovědy.
Zadej UKAŽ pro zobrazení tvého nákupního seznamu.
Zadej SMAZAT POLOŽKU pro odstranění položky z tvého nákupního seznamu.
Zadej SMAZAT SEZNAM pro vymazání tvého nákupního seznamu.
Zadej ULOŽ pro uložení tvého nákupního seznamu a ukončení programu.
Zadej KONEC pro ukončení programu bez uložení.""".format(len(seznam)))


def ukaz_nakupni_seznam(seznam):
	# ukáže nákupní seznam
	clear_console()
	if len(seznam) == 0:
		print('Nemáš žádnou položku ve svém nákupním seznamu.')
	else:
		print('Tvůj nákupní seznam:\n')
		for item in seznam:
			print(item)


def pridat_na_nakupni_seznam(nova_polozka, seznam):
	clear_console()
	# přidá novou položku na nakupni_seznam
	seznam.append(nova_polozka)
	print("Přidáno {}. Seznam teď má {} položek.".format(nova_polozka, len(seznam)))


def odstranit_polozku(seznam):
	clear_console()
	print("Jakou položku chceš odstranit?\n")
	# zadání jakou položku odstranit
	odpoved = input("Smaž: ")
	if odpoved in seznam:
		# odstraní položku z nákupního seznamu
		seznam.remove(odpoved)
		clear_console()
		print("{} vymazáno z nákupního seznamu!".format(odpoved))
	else:
		clear_console()
		print("{} Tato položka není na tvém nákupním seznamu.".format(odpoved))


def otevrit_nakupni_seznam(soubor, seznam):
	try:
		# otevření souboru
		with open(soubor) as file:
			# čtení obsahu souboru
			data: List[str] = file.read().splitlines()
			seznam.extend(data)
	except FileNotFoundError:
		pass


def uloz_nakupni_seznam(soubor, seznam):
	# uložit seznam do souboru
	with open(soubor, "w") as file:
		for item in seznam:
			file.write(item + "\n")
	print('Tvůj seznam byl uložen do souboru', soubor, 'a poslán na tvůj email.')
	print('Pěkný nákup :-)')


def vymaz_nakupni_seznam(soubor, seznam):
	clear_console()
	# vymazat nakupni_seznam

	seznam.clear()
	try:
		# vymazat uložený nakupni_seznam
		os.remove(soubor)
		print("Seznam úspěšně smazán.")
	except FileNotFoundError:
		print("Seznam úspěšně smazán.")


# ----------------------------------------------------
# poslání emailu z smtp.gmail.com
def send_an_email():
	toaddr = 'komu@adresa'
	me = 'moje@adresa'
	subject = "jmeno_souboru.txt"

	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = toaddr
	msg.preamble = "test "

	part = MIMEBase('application', "octet-stream")
	part.set_payload(open("C:/cesta/k/souboru", "rb").read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="jmeno_souboru.txt"')
	msg.attach(part)

	try:
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(user='nekdo@gmail.com', password='nejakeheslo')
		s.sendmail(me, toaddr, msg.as_string())
		s.quit()

	# výjimka:
	except SMTPException as error:
		print("Chyba! Neodesláno!")

# spustit funkce nákupního seznamu
otevrit_nakupni_seznam(soubor, seznam)
ukaz_napovedu(seznam)

while True:
	# ovládání programu
	program = input('\nPřidej na nákupní seznam: ')

	if program == "KONEC" or program == 'konec':
		ukaz_nakupni_seznam(seznam)
		print('\nKonec programu. měj se fajn :-)\n')
		break
	elif program == "POMOC" or program == 'pomoc':
		ukaz_napovedu(seznam)
		continue
	elif program == "UKAŽ" or program == 'ukaž':
		ukaz_nakupni_seznam(seznam)
		continue
	elif program == "ULOŽ" or program == 'ulož':
		ukaz_nakupni_seznam(seznam)
		uloz_nakupni_seznam(soubor, seznam)
		break
	elif program == "SMAZAT SEZNAM" or program == 'smazat seznam':
		vymaz_nakupni_seznam(soubor, seznam)
		continue
	elif program == "SMAZAT POLOŽKU" or program == 'smazat položku':
		odstranit_polozku(seznam)
		continue
	else:
		pridat_na_nakupni_seznam(program, seznam)

# poslání emailu
send_an_email()
