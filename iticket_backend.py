from pyunifi.controller import Controller
import fnmatch
import subprocess
import os
import sys
import psutil
from datetime import datetime
from tkinter import messagebox

connect_config = []
ticket_dm = []
tickets_list_gui = []
guest_mac = []
ticket_on_stack = []
ap_mac_tab = []
tickets_to_label = []

with open("C:/iticket/ini.cfg", "r", encoding="utf8") as config:
    for line in config:
        settings = line.split(";\n")
        connect_config.append(settings[0])

host = str(fnmatch.filter(connect_config, 'host*')).replace('host = ', '').strip("['']")
username = str(fnmatch.filter(connect_config, 'username*')).replace('username = ', '').strip("['']")
password = str(fnmatch.filter(connect_config, 'password*')).replace('password = ', '').strip("['']")
port = str(fnmatch.filter(connect_config, 'port*')).replace('port = ', '').strip("['']")
port = int(port)
version = str(fnmatch.filter(connect_config, 'version*')).replace('version = ', '').strip("['']")
site_id = str(fnmatch.filter(connect_config, 'site_id*')).replace('site_id = ', '').strip("['']")
ssl_verify = str(fnmatch.filter(connect_config, 'ssl_verify*')).replace('ssl_verify = ', '').strip("['']")
default_printer = str(fnmatch.filter(connect_config, 'default_printer*')).replace('default_printer = ', '').strip("['']")

if "False" in ssl_verify:
    ssl_verify = False
elif "True" in ssl_verify:
    ssl_verify = True


c = Controller(host, username, password, port, version, site_id, ssl_verify)


def get_mac_ap():
    for ap in c.get_aps():
        z=('AP named %s with MAC %s' % (ap.get('name'), ap['mac']))
        print(z)
        ap_mac_tab.append(z)
    return(print(ap_mac_tab))


def reboot_on_click(el):
    el = el.split('MAC')[1].strip()
    print('Reboot urządzenia o adresie = ', el)
    c.restart_ap(el)

def create_ticket(amount, amount_to_use, expire_time, comment):
    voucher = c.create_voucher(amount, amount_to_use, expire_time, note = comment)
    code = voucher[0].get('code')
    return print(code)


def get_tickets(amount = None):
    tickets_to_label.clear()
    tickets_list_gui.clear()
    ticket_dm.clear()
    tickets = c.list_vouchers()
    for n in range(0, len(tickets)):
        t_id = str(tickets[n]).split(",")[0][1::]
        t_create_time = str(tickets[n]).split(",")[2]
        t_code = str(tickets[n]).split(",")[3]
        t_admin_name = str(tickets[n]).split(",")[5]
        t_duration = str(tickets[n]).split(",")[7]
        t_note = str(tickets[n]).split(",")[10]
        tickets_list_gui.append((t_id.split(':')[1] + "," + t_create_time.split(':')[1] + "," + t_code.split(':')[1] + "," + t_admin_name.split(':')[1] + "," + t_duration.split(':')[1] + "," + t_note.split(':')[1]))
        
        date_from_timestamp = datetime.fromtimestamp(int(t_create_time.split(':')[1]))
        
        tickets_to_label.append((str(n + 1)) + ";" + str(date_from_timestamp) + ";" + t_code.split(':')[1].replace("'", "") + ";" + t_duration.split(':')[1] + ";" + t_note.split(':')[1].replace("'", "")) 
    
    if amount == None:
        how_many = len(tickets_list_gui)
    else:
        how_many = amount
    
    for n in range(0, how_many, 1):
        # print("Ticket [", n,"] ------->", tickets_list[n])
        # print("Dry data for gui: --- ticket [", n, "]:", tickets_list_gui[n])
        data_tuple = list(map(str, tickets_list_gui[n].split(', ')))
        ticket_dm.append(data_tuple)
    # print(ticket_dm[-1][2]) ------wyświetlanie wartości z macierzy ticketów
    return (tickets_to_label[0:amount])

def rem_ticket(ticket_id_number_start, ticket_id_number_stop = None):
    id_ticket = str(ticket_dm[ticket_id_number_start][0]).replace("'", '').strip()
    
    if ticket_id_number_stop != None and ticket_id_number_stop >= ticket_id_number_start:
        for k in range(ticket_id_number_start, (ticket_id_number_stop + 1)):

            try:
                c.delete_voucher(str(ticket_dm[k][0]).replace("'", '').strip())
                print("Wyjebawszy ticket : ", str(ticket_dm[k][0]).replace("'", '').strip())
            except:
                print("Błąd, przy usuwaniu")
                return
    elif ticket_id_number_stop == None:
        try:
            c.delete_voucher(id_ticket)
            print("Wyjebawszy ticket : ", id_ticket)
        except:
            print("Błąd, przy usuwaniu")
            return


def get_connected_guest(only_guest = 0):
    guest_mac.clear()
    aps = c.get_aps()
    clients = c.get_clients() #get_users
    ap_names = dict([(ap['mac'], ap.get('name', '????')) for ap in aps])
    client_id = 0    
    FORMAT = '%-25s  %-18s  %-12s  %-12s'
    print(FORMAT % ('NAME', 'MAC', 'AP', 'SSID'))
    if only_guest == 0:
        for client in clients:
            ap_name = ap_names.get(client.get('ap_mac', '????'))
            ssid = client.get('essid', '????')
            name = client.get('hostname') or client.get('ip', '????')
            mac = client.get('mac', '????')
            print(FORMAT % (name, mac, ap_name, ssid))
    elif only_guest == 1:
        for client in clients:
            ap_name = ap_names.get(client.get('ap_mac', '????'))
            ssid = client.get('essid', '????')
            name = client.get('hostname') or client.get('ip', '????')
            mac = client.get('mac', '????')
            if ssid == "EPNS_GUEST":
                print(FORMAT % (name, mac, ap_name, ssid))
                guest = str(name +'---'+ mac) 
                guest_mac.append(list(map(str, guest.split('---'))))
        print('*' * 100)
        for el in guest_mac:
            print("Client & MAC: --- [", client_id, "]:", el)
            client_id += 1

#U nas to nie działa
def disconnect_client(id_client):
    mac = guest_mac[id_client][1].replace("'", '').strip()
    name_client = guest_mac[id_client][0]
    c.disconnect_client(mac)
    return(print(name_client, "is disconnected"))

#U nas to działa
def unauthorize_guest(id_client):
    mac = guest_mac[id_client][1].strip()
    name_client = guest_mac[id_client][0]
    c.unauthorize_guest(mac)
    return(print(name_client, "is unauthorized"))
####################################################################################################################
####################################################################################################################
####################################################################################################################
# get_tickets(param1) - to metoda, która zwraca istniejące tickety z zakładki "Kupony" na kontrolerze.
# Można wywołać z parametrem w postaci int, np. get_tickets(5), żeby yświetlić tylko 5 najświeższych rekordór.
####################################################################################################################
# rem_ticket(param1, param2) - to metoda, która usuwa ticket o zadanym przez nas id jako param1 
# !!!UWAGA!!! - metodę wykonywać zawsze po metodzie get_ticket(). Param1 jest obowiązkowy.
# Przykład wywyołania:
# get_tickets()   --- wyświetli wszystkie rekordy, wraz z numerem id
# rem_tickets(0)  --- usunie tylko jeden rekord, który jest pierwszy
# opcjonalnie:
# get_tickets()
# rem_tickets(0, 5) --- usunie 5 rekordów od najświeższych tj. 0-5
# get_tickets()     --- wyświetli ponownie listę ticketów, już po usunięciu
######################################################################################################################
#get_mac_ap() - zwraca mac adresy acces pointów
######################################################################################################################
#create_ticket(amount, amount_to_use, expire_time, comment) - służy do tworzenia ticketów.
#Wszystkie parametry są obowiązkowe, gdzie:
#amount - to ilość tworzonych ticketów, np. 5
#amount_to_use - to ilość możliwych razy wykorzystania pojedynczego biletu,
# podczas jego trwania przez unikalne adresy mac. Wartość 1 - pojedyncze użycie, wartość 0 - nieskończona ilość użyć.
#expire_time - to czas trwania ticketu, wyrażony w minutach.
#comment - to opis ticketu, który należy podać w "", np. "to jest opis"
#Przykład wywyołania:
#create_ticket(3, 1, 120, "Przykład tzech biletów jednokrotknego użycia na okres 2 godzin")
#get_connected_guest(only_guest = 0) - to metoda, która zwraca listę zalogowanych do sieci wi-fi klientów,
# wraz z ich mac adresami,, nazwą acces pointa oraz nazwą ssid. Możliwe jest wywołanie z paramterem tj.:
#get_connected_guest(1) --- spowoduje wyświetlenie listy klientów tylko z sieci ssid = EPNS_GUEST oraz
#stworzona zostanie tabela, którą wykorzystuje metoda disconnect_client('mac_address'), unauthorize_guest('mac_address')


