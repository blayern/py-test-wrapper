#!/usr/bin/python2
import unittest
import time, hashlib, base64
from datetime import datetime
from pyvirtualdisplay import Display 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import MySQLdb as db	
from init import *

class Cases(unittest.TestCase):
	@unittest.skipIf(system!="test", "Web system not supported")
	def setUp(self):
		global visibleBrowser
		self.testPassed = False
		self.testStep = 1
		self.display = Display(visible = visibleBrowser, size = (1920, 1080))
		self.display.start()
		self.browser = \
		    webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
		self.browser.set_window_size(1920, 1080)
		self.conn = db.connect(host = dutIp, user = 'root', passwd = 'root', db='test')
		self.cur = self.conn.cursor()
		self.cur.execute('TRUNCATE users')
		self.conn.commit()
	
	def test_1_logIn(self):
		"""Check for empty fields, incorrect login and correct login"""
		browser = self.browser
		conn = self.conn
		cur = self.cur
		# connect to dut's web with 
		#    dutProt://dutIp:dutPort
		browser.get('%s://%s:%d' % (dutProt, dutIp, dutPort))
		self.assertIn("Login", browser.title, "%d: Not promped to LogIn" %self.testStep)

		self.testStep = 2
		# find froms: form_email, form_password, form_submit
		usernameForm = browser.find_element_by_id('form_email')
		passwordForm = browser.find_element_by_id('form_password')
		submitButton = browser.find_element_by_id('form_submit')
		# clear usernameForm and passwordForm, and click submitButton
		usernameForm.clear()
		passwordForm.clear()
		submitButton.click()
		# check if still on login page
		self.assertIn("Login", browser.title, "%d: Not on login page" %self.testStep)

		self.testStep = 3
		# check for has-error
		try: hasError = browser.find_element_by_class_name('has-error')
		except NoSuchElementException:
			self.fail("%d: No error on empty user and password" %self.testStep)

		self.testStep = 4
		# find froms: form_email, form_password, form_submit
		usernameForm = browser.find_element_by_id('form_email')
		passwordForm = browser.find_element_by_id('form_password')
		submitButton = browser.find_element_by_id('form_submit')
		# clear usernameForm and passwordForm, type 'test' in user and click submitButton
		usernameForm.clear()
		usernameForm.send_keys('test')
		passwordForm.clear()
		submitButton.click()
		# check if still on login page
		self.assertIn("Login", browser.title, "%d: Not on login page" %self.testStep)

		self.testStep = 5
		# check for has-error
		try: hasError = browser.find_element_by_class_name('has-error')
		except NoSuchElementException:
			self.fail("%d: No error on empty password" %self.testStep)

		self.testStep = 6
		# find froms: form_email, form_password, form_submit
		usernameForm = browser.find_element_by_id('form_email')
		passwordForm = browser.find_element_by_id('form_password')
		submitButton = browser.find_element_by_id('form_submit')
		# clear usernameForm and passwordForm, type 'test' in password and click submitButton
		usernameForm.clear()
		passwordForm.clear()
		passwordForm.send_keys('test')
		submitButton.click()
		# check if still on login page
		self.assertIn("Login", browser.title, "%d: Not on login page" %self.testStep)

		self.testStep = 7
		# check for has-error
		try: hasError = browser.find_element_by_class_name('has-error')
		except NoSuchElementException:
			self.fail("%d: No error on empty user" %self.testStep)

		self.testStep = 8
		# find froms: form_email, form_password, form_submit
		usernameForm = browser.find_element_by_id('form_email')
		passwordForm = browser.find_element_by_id('form_password')
		submitButton = browser.find_element_by_id('form_submit')
		# clear usernameForm and passwordForm, type 'test' in user and password and click submitButton
		usernameForm.clear()
		usernameForm.send_keys('test')
		passwordForm.clear()
		passwordForm.send_keys('test')
		submitButton.click()
		# check if still on login page
		self.assertIn("Login", browser.title, "%d: Not on login page" %self.testStep)

		self.testStep = 9
		# check if password has error
		try: hasError = browser.find_element_by_class_name('error')
		except NoSuchElementException:
			self.fail("%d: No error on invalid user pass combination" %self.testStep)

		self.testStep = 10
		# insert new user in db with name test and password test
		# gen password hash like it's generated by fuelPHP framwork
		# base64 encoded pbkdf2 encripted with sha254 password string 'admin' with salt 'salt[system]' and 10000 iterations
		password = base64.b64encode(hashlib.pbkdf2_hmac('sha256', b'test', b'' + salt[system] + '', 10000))
		cur.execute("INSERT INTO users VALUES ('1','test','"+ password +"','100','t@t.t',0,0,0,0,0,0,0,0)")
		conn.commit()

		usernameForm = browser.find_element_by_id('form_email')
		passwordForm = browser.find_element_by_id('form_password')
		submitButton = browser.find_element_by_id('form_submit')
		usernameForm.clear()
		usernameForm.send_keys('test')
		passwordForm.clear()
		passwordForm.send_keys('test')
		submitButton.click()
		# check if redirected to Measurements
		self.assertIn("Measurements", browser.title, "%d: Not on Measurements page" %self.testStep)
		self.assertIn("measurements", browser.current_url, "%d: Not on Measurements page" %self.testStep)
		self.testPassed = True

	def test_2_logOut(self):
		"""LogOut"""
		browser = self.browser
		conn = self.conn
		cur = self.cur
		# connect to dut's web with 
		#    dutProt://dutIp:dutPort
		browser.get('%s://%s:%d' % (dutProt, dutIp, dutPort))
		self.assertIn("Login", browser.title, "%d: Not promped to LogIn" %self.testStep)
		# insert new user in db with name test and password test
		# gen password hash like it's generated by fuelPHP framwork
		# base64 encoded pbkdf2 encripted with sha254 password string 'admin' with salt 'salt[system]' and 10000 iterations
		password = base64.b64encode(hashlib.pbkdf2_hmac('sha256', b'Password', b'' + salt[system] + '', 10000))
		cur.execute("INSERT INTO users VALUES ('1','Username','"+ password +"','100','t@t.t',0,0,0,0,0,0,0,0)")
		conn.commit()
		self.testStep = 2
		usernameForm = browser.find_element_by_id('form_email')
		passwordForm = browser.find_element_by_id('form_password')
		submitButton = browser.find_element_by_id('form_submit')
		usernameForm.clear()
		usernameForm.send_keys('Username')
		passwordForm.clear()
		passwordForm.send_keys('Password')
		submitButton.click()
		# check if redirected to Measurements
		self.assertIn("Measurements", browser.title, "%d: Not on Measurements page" %self.testStep)
		self.assertIn("measurements", browser.current_url, "%d: Not on Measurements page" %self.testStep)
		try: hasSuccess = browser.find_element_by_class_name('alert-success')
		except NoSuchElementException:
			self.fail("%d: No alert-success e.g no Welcome msg" %self.testStep)
		
		self.testStep = 3
		# find user button
		usernameButton = browser.find_element_by_partial_link_text('Username')
		usernameButton.click()
		# find logout button
		logoutButton = browser.find_element_by_partial_link_text('Logout')
		logoutButton.click()
		self.assertIn("Login", browser.title, "%d: Not prompted to LogIn" %self.testStep)

		self.testPassed = True

	def tearDown(self):
		if not self.testPassed:
			self.browser.get_screenshot_as_file('results/' + self.id()+ '_' + str(datetime.now()).replace(' ', '_') + '.png')
		self.cur.execute('TRUNCATE users')
		self.conn.commit()
		self.conn.close()
		self.browser.quit()
		self.display.stop()

if __name__ == "__main__":
	unittest.main()
