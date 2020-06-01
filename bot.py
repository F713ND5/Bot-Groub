'''
File: Bot Auto Post Ke Semua Grub
Author: Pandas ID
Date: 28-05-2020

Description: Script ini open source jadi bisa kalian pelajari
meskipun begitu saya tidak rela jika script ini di upload ke github kalian tanpa
mencantumkan sumber nya (github saya).

Untuk yang suka recode karya orang, ingat!!! Recode tidak akan menjadikan kalian 
hebat.

Tolong hargai script orang meskipun kalian menganggap itu hanya script sampah

semoga bermanfaat...

'''

#Import Modul
from headerz import headerz
import requests
import time
import html
import os
import re

class Main:
    
    banner = '''
      > ---------------------- <
        > Bot Group Facebook <
        |                    |
        >     Pandas ID      <
      > ---------------------- <
    '''
    def __init__(self):
        self.banner = Main.banner
        self.head = 'https://mbasic.facebook.com'
        self.req = requests.Session()
        self.confirmation = False
        #Login
        os.system('clear')
        file = []
        print(self.banner)
        for c in os.listdir('.'):
            if '.log' in c:
                file.append(c)
        if len(file) != 0:
            for s in file:
                print(f'      [{file.index(s)+1}] '+s)
        print()
        select_file = int(input('      -•> '))
        open_file = open(file[select_file-1], 'r').read()
        header = headerz().parser(open_file)
        cookie = headerz().cookie_builder(header["cookie"])
        self.kuki = {'Cookies':cookie}
        test_cookie = self.req.get(self.head+'/me', cookies=self.kuki).text
        self.username = re.search(r'<title>(.*?)</title>', test_cookie).group(1)
        if 'Masuk ke Facebook' in test_cookie:
            os.system('rm -rf '+file[select_file-1])
            exit('      -!> Invalid Cookies')
        self.menu()
    
    def menu(self):
        os.system('clear')
        print(self.banner)
        print('      [•] User: '+self.username)
        print()
        print('      [1] Kirim pesan ke semua grub dengan konfirmasi')
        print('      [2] Kirim pesan ke semua grub tanpa konfirmasi')
        print('      [3] Lihat daftar grub')
        print('      [4] Info')
        print('      [0] Exit')
        print()
        pilih = input('      -•> ')
        if pilih == '1':
            self.confirmation = True
            self.inputData()
        elif pilih == '2':
            self.confirmation = False
            self.inputData()
        elif pilih == '3':
            self.listGroup()
        elif pilih == '4':
            self.info()
        elif pilih == '0':
            exit('      -!> Exit')
        else:
            print('      -!> Pilihan tidak tersedia')
            time.sleep(1)
            self.menu()
            
    def inputData(self):
        input_message = input('      [•] Pesan: ')
        get_url = self.req.get(self.head+'/groups', cookies=self.kuki).text
        url_all = re.search(r'\<a\ href\=\"\/groups\/\?seemore(.*?)\"\>\<span\>Tampilkan\ Semua\<\/span\>\<\/a\>', get_url).group(1)
        get_list_group = self.req.get(self.head+'/groups/?seemore'+url_all, cookies=self.kuki).text
        self.list_group = re.findall(r'\<a\ href\=\"(.*?)\"\>(.*?)\<\/a\>', get_list_group)
        for s in self.list_group:
            try:
                self.getData(s[0], input_message)
            except AttributeError:
                pass
                
    def getData(self, rel, message):
        get_url = self.req.get(self.head+rel, cookies=self.kuki).text
        name_group = re.search(r'<title>(.*?)</title>', get_url).group(1)
        url_action = re.search(r'\<form\ method\=\"post\"\ action\=\"(.*?)\"\ class\=\"(.*?)\"\ id\=\"mbasic\-composer\-form\"\>', get_url).group(1)
        action = html.unescape(url_action)
        fb_dtsg = re.search(r'\<input\ type\=\"hidden\"\ name\=\"fb_dtsg\"\ value\=\"(.*?)\"\ autocomplete\=\"off\"\ \/\>', get_url).group(1)
        jazoest = re.search(r'\<input\ type\=\"hidden\"\ name\=\"jazoest\"\ value\=\"(.*?)\"\ autocomplete\=\"off\"\ \/\>', get_url).group(1)
        target = re.search(r'\<input\ type\=\"hidden\"\ name\=\"target\"\ value\=\"(.*?)\"\ \/\>', get_url).group(1)
        c_src = re.search(r'\<input\ type\=\"hidden\"\ name\=\"c_src\"\ value\=\"(.*?)\"\ \/\>', get_url).group(1)
        cwevent = re.search(r'\<input\ type\=\"hidden\"\ name\=\"cwevent\"\ value\=\"(.*?)\"\ \/\>', get_url).group(1)
        referrer = re.search(r'\<input\ type\=\"hidden\"\ name\=\"referrer\"\ value\=\"(.*?)\"\ \/\>', get_url).group(1)
        ctype = re.search(r'\<input\ type\=\"hidden\"\ name\=\"ctype\"\ value\=\"(.*?)\"\ \/\>', get_url).group(1)
        cver = re.search(r'\<input\ type\=\"hidden\"\ name\=\"cver\"\ value\=\"(.*?)\"\ \/\>', get_url).group(1)
        
        if name_group == 'Facebook' or name_group == self.username:
            pass
        else:
            data = {
                'fb_dtsg':fb_dtsg,
                'jazoest':jazoest,
                'target':target,
                'c_src':c_src,
                'cwevent':cwevent,
                'referrer':referrer,
                'ctype':ctype,
                'cver':cver,
                'rst_icv':'',
                'xc_message':message,
                'view_post':'Posting'
                }
            self.sendPostingan(action, name_group, data)
    
    def sendPostingan(self, action, name_group, data):
        print()
        try:
            if self.confirmation:
                print('      --> Mengirim postingan ke grub: '+name_group)
                konfirmasi = input('      -?> Lanjut kirim [y/t]: ')
                if konfirmasi == 'y' or konfirmasi == 'Y':
                    send_postingan = self.req.post(self.head+action, data=data, cookies=self.kuki)
                    print('      --> Berhasil terkirim ke grub: '+name_group)
                elif konfirmasi == 't' or konfirmasi == 'T':
                    print('      --> Postingan tidak terkirim ke grub: '+name_group)
            else:
                send_postingan = self.req.post(self.head+action, data=data, cookies=self.kuki)
                print('      --> Berhasil terkirim ke grub: '+name_group)
        except KeyboardInterrupt:
            pass
            exit()
        
    #Menampilkan daftar group
    def listGroup(self):
        os.system('clear')
        print(self.banner)
        print()
        get_url = self.req.get(self.head+'/groups', cookies=self.kuki).text
        url_all = re.search(r'\<a\ href\=\"\/groups\/\?seemore(.*?)\"\>\<span\>Tampilkan\ Semua\<\/span\>\<\/a\>', get_url).group(1)
        get_list_group = self.req.get(self.head+'/groups/?seemore'+url_all, cookies=self.kuki).text
        list_group = re.findall(r'\<a\ href\=\"(.*?)\"\>(.*?)\<\/a\>', get_list_group)
        count = 1
        for s in list_group:
            if '/groups/' in s[0] and 'refid' in s[0]:
                print(f'      [{str(count)}] {s[1]}')
                count += 1
        print()
        input('      > Kembali <')
        self.menu()
                
    #Info
    def info(self):
        os.system('clear')
        print(self.banner)
        print('              [ Info ]')
        print('      ----------------------')
        print('       Author: Pandas ID')
        print()
        print('       Kontak: WA > 082250223147')
        print('               FB > Pandas ID')
        print('               TL > https://t.me/PandasID')
        print()
        print('       Blog: https://pandasid.blogspot.com')
        print('      ----------------------')
        print('       Jika ada masalah pada Botnya,silahkan')
        print('       tanyakan pada saya.')
        print()
        input('      > Kembali <')
        self.menu()
try:
    Main()
except KeyboardInterrupt:
    exit('      -!> Exit')
except requests.ConnectionError:
    exit('      -!> Koneksi error')
except ValueError:
    exit('      -!> Masukan angka')
