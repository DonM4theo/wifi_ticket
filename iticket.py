from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import iticket_backend as ib
import string
from simple_zpl2 import ZPLDocument
import io
import os
from simple_zpl2 import NetworkPrinter
import shutil


counter = []
printer_buffer = []

arr = os.listdir('C:\\iticket\\printer_buffer')
for etykieta in arr:
    os.remove("\\iticket\\printer_buffer\\" + etykieta)
    
class App(Tk):
    
      
    def __init__(self):
        super(App, self).__init__()
       
        def on_tab_selected(event):
            
            selected_tab = event.widget.select()
            tab_text = event.widget.tab(selected_tab, "text")
            if tab_text == "HOME":
                labelFrame1 = LabelFrame(self.tab1, text = "Strona startowa", font="Verdana 12 bold italic")
                labelFrame1.grid(column = 0, row = 0, padx = 8, pady = 4)
                label1 = Label(labelFrame1, text = "Witaj w aplikacji iticket!\n\nAplikacja stworzona z myślą o szybszym oraz wygodniejszym korzystaniu\n z funcjonalności UniFi cotrollera.\nWybrane funkcjonaloności znajdują się w kolejnych zakładkach głównego okna aplikacji.",
                font="Tahoma 13 bold")
                label1.grid(column = 0, row = 1, pady = 50)
            elif tab_text == "AP INFO":
                labelFrame2 = LabelFrame(self.tab2, text = "AP info", font="Verdana 12 bold italic")
                labelFrame2.grid(column = 0, row = 0, padx = 8, pady = 4)
                ib.get_mac_ap()
                for el in ib.ap_mac_tab:
                    label2 = Label(labelFrame2, text = el, font="Tahoma 12")
                    label2.grid(column = 0, row = ib.ap_mac_tab.index(el), sticky = 'W', pady=4)
                    button2 = Button(labelFrame2, text = "R", font="Tahoma 10 bold", bg = "#eb4c34", command = lambda el=el: ib.reboot_on_click(el))
                    button2.grid(column = 1, row = ib.ap_mac_tab.index(el), sticky = 'W')
            elif tab_text == "CREATE VOUCHER":
                txt_color = "#eb4c34"
                pad_x = 2
                pad_y = 1
                labelFrame3 = LabelFrame(self.tab3, text = "Stwórz voucher", font="Verdana 12 bold italic")
                labelFrame3.place(relx = 0, rely = 0)
                l1 = Label(labelFrame3, text="Ilość voucherów:", font="Tahoma 10 bold", fg=txt_color)
                l2 = Label(labelFrame3, text="Ilość użyć:", font="Tahoma 10 bold", fg=txt_color)
                l3 = Label(labelFrame3, text="Czas dostępu:", font="Tahoma 10 bold", fg=txt_color)
                l5 = Label(labelFrame3, text="Opis:", font="Tahoma 10 bold", fg=txt_color)
                combo1 = ttk.Combobox(labelFrame3, width=14, values=[1,2,3,4,5,6,7,8,9,10])
                combo2 = ttk.Combobox(labelFrame3, width=12, values=["single","multi",2,3,4,5,6,7,8,9,10])
                entry0 = Entry(labelFrame3, width=6)
                combo4 = ttk.Combobox(labelFrame3, width=5, values=['min','godz', 'dni'])
                entry1 = Entry(labelFrame3, width=35)
                
                l1.grid(row=0, column=0, padx=pad_x, pady=pad_y)
                l2.grid(row=0, column=1, padx=pad_x, pady=pad_y)
                l3.grid(row=0, column=2, columnspan=3, padx=pad_x, pady=pad_y)
                l5.grid(row=0, column=5, columnspan=10, padx=pad_x, pady=pad_y)
                combo1.grid(row=1, column=0, padx=pad_x, pady=pad_y)
                combo2.grid(row=1, column=1, padx=pad_x, pady=pad_y)
                entry0.grid(row=1, column=2, padx=pad_x, pady=pad_y)
                combo4.grid(row=1, column=3, padx=pad_x, pady=pad_y)
                entry1.grid(row=1, column=5, padx=pad_x, pady=pad_y)
                def generate():
                    
                    print("COUNTER:", counter)
                    # print("Ilość voucherów:", combo1.get(),"\nTyp/ilość użyć:", combo2.get(), "\nCzas trwania:", entry0.get(), "\nJednostka czasu:", combo4.get(), "\nOpis:", entry1.get())
                    # stack = (combo1.get(), combo2.get(), entry0.get(), combo4.get(), entry1.get()) # nie wiem czy potrzebuje tego stacka i ładowania do tabeli
                    # ib.ticket_on_stack.append(stack)
                          
                    if (combo1.get()).isdigit() == True:
                        for c in range(0, int(combo1.get())):
                            counter.append(1)
                            
                    else:
                        messagebox.showerror("Brak podanej ilości", "Wpisz lub wybierz z listy żądaną ilość voucherów")
                        if len(counter) >= 1:
                            counter.remove(1)
                        return
                        
                    if (entry0.get()).isdigit() == False:
                        messagebox.showerror("Brak wartości czas", "Wpisz wartość liczbową w postaci liczby całkowitej w polu czas")
                        if len(counter) >= 1:
                            counter.remove(1)
                        return
                   
                    if combo4.get() == "godz":
                        time = int(entry0.get()) * 60
                        if time > 525600:
                            messagebox.showerror("Limit czasu", "Limit przedzielonego czasu vouchera wynosi 365 dni.")
                            if len(counter) >= 1:
                                counter.remove(1)
                            return
                        
                    elif combo4.get() == "dni":
                        time = int(entry0.get()) * 1440
                        if time > 525600:
                            messagebox.showerror("Limit czasu", "Limit przedzielonego czasu vouchera wynosi 365 dni.")
                            if len(counter) >= 1:
                                counter.remove(1)
                            return
                        
                    elif combo4.get() == "min":
                        time = int(entry0.get())
                        if time > 525600:
                            messagebox.showerror("Limit czasu", "Limit przedzielonego czasu vouchera wynosi 365 dni.")
                            if len(counter) >= 1:
                                counter.remove(1)
                            return
                        
                    elif combo4.get() != "godz" or "dni" or "min":
                        messagebox.showerror("Brak jednostki w polu jednostki", "Wybierz jednostkę czasu z listy")
                        if len(counter) >= 1:
                            counter.remove(1)
                        return 

                    if combo2.get() == "single":
                        typ = 1
                        
                    elif combo2.get() == "multi":
                        typ = 0
                        
                    elif (combo2.get()).isdigit() == False:
                        messagebox.showerror("Nieprawidłwoy typ", "Wybierz z listy ilość użyć dla vouchera\nnp. single, multi, 2, 3, ...")
                        if len(counter) >= 1:
                            counter.remove(1)
                        return
                    else:
                        typ = int(combo2.get())


                    ib.create_ticket(int(combo1.get()), typ, time, str(entry1.get()))
                    last_vouchers = ib.get_tickets(len(counter))
                    voucher_frame = LabelFrame(self.tab3, text = "Ostatnio stworzone:", font="Verdana 8 bold italic")
                    voucher_frame.place(relx = 0.01, rely = 0.12)
                    f = "Verdana 8 bold"
                    l_number = Label(voucher_frame, text = "Lp.", font=f, bd=0)
                    l_c_time = Label(voucher_frame, text = "Czas stworzenia:", font=f)
                    l_code = Label(voucher_frame, text = "Kod:", font=f)
                    l_duration = Label(voucher_frame, text = "Czas (min):", font=f)
                    l_note = Label(voucher_frame, text = "Opis:", font=f)

                    l_number.grid(row = 0, column = 0, sticky = W, pady=pad_y)
                    l_c_time.grid(row = 0, column = 1, sticky = W, padx=pad_x, pady=pad_y)
                    l_code.grid(row = 0, column = 2, sticky = W, padx=pad_x, pady=pad_y)
                    l_duration.grid(row = 0, column = 3, sticky = W, padx=pad_x, pady=pad_y)
                    l_note.grid(row = 0, column = 4, sticky = W, padx=pad_x, pady=pad_y)
                   
                    for voucher in last_vouchers:
                        for part in voucher.split(';'):
                            
                            l_current = Label(voucher_frame, text = part, font = "Tahoma 8")
                            l_current.grid(column=(voucher.split(';').index(part)), row=last_vouchers.index(voucher) + 1, sticky = W)
                            
                            # print("Z vouchera:", voucher)
                            # print("Element z:", part, "Na kolumnę:", (voucher.split(';').index(part)))

                    combo1.delete('0','end') 
                    combo2.delete('0','end')  
                    entry0.delete('0','end')  
                    combo4.delete('0','end')  
                    entry1.delete('0','end') 

                    return (print(len(counter)))
                
                def print_voucher():
                    c = 0
                    r = 0
                    last_vouchers = ib.get_tickets(len(counter))
                    to_print = LabelFrame(self.tab3, text = "Wybierz z listy:", font="Tahoma 8 bold italic", width=6)
                    to_print.place(relx=0.72, rely=0.15)
                    
                    def select(from_button):
                        b_text = int(from_button.split(";")[0])
                        print(b_text)
                        
                        if from_button in printer_buffer:
                            printer_buffer.remove(from_button)
                            btn_name_list[b_text].config(bg='SystemButtonFace', relief="raised")
                        else:
                            printer_buffer.append(from_button)
                            btn_name_list[b_text].config(bg="#eb4c34", relief="sunken")

                        return
                        
                    def select_all():
                        
                        if b01.cget('relief') == 'raised':
                            b01.config(relief="sunken", bg="#eb4c34")
                            printer_buffer.clear()
                            
                            for v in last_vouchers:
                                printer_buffer.append(v)

                                for g in range(1, int(len(last_vouchers) + 1), 1):
                                    btn_name_list[g].config(relief="sunken", bg="#eb4c34")
                            
                        elif b01.cget('relief') == 'sunken':
                            b01.config(relief="raised", bg="SystemButtonFace")
                            printer_buffer.clear()
                            for g in range(1, int(len(last_vouchers) + 1), 1):
                                btn_name_list[g].config(relief="raised", bg="SystemButtonFace")

                        return              

                    def send_to_printer():
                        if len(printer_buffer) < 1:
                            messagebox.showerror("Brak etykiety", "Wskaż co najmniej jedną etykietę")
                            return
                        else:
                            for vou in printer_buffer:
                                
                                with open("C:/iticket/default/voucher.zpl", "r") as main_f:
                                    try:
                                        with open("C:/iticket/printer_buffer/" + vou.split(';')[2] + ".zpl", "x", encoding='UTF8') as f: 
                                            for line in main_f:
                                                f.write(line)
                                    except:
                                        print("Plik", vou.split(';')[2], "\b.zpl już istnieje.")
                                        messagebox.showwarning("Wydruk biletu", "Wskazany przez Ciebie bilet, został już wydrukowany.")
                                        return
                                m_file = open("C:/iticket/printer_buffer/" + vou.split(';')[2] + ".zpl", "r", encoding='UTF8')
                                list_of_lines = m_file.readlines()
                                list_of_lines[13] = ("^FT144,258^A0N,43,45^FH\\^FD" + str(vou.split(';')[2]).strip() + "^FS\n")
                                
                                m_file = open("C:/iticket/printer_buffer/" + vou.split(';')[2] + ".zpl", "w", encoding='UTF8')
                                m_file.writelines(list_of_lines)
                                m_file.close()

                                raw = ''
                                                                
                                file = open("C:/iticket/printer_buffer/" + vou.split(';')[2] + ".zpl", "r", encoding='UTF8')
                                lines = file.readlines()
                        
                                for line in lines:
                                    raw = raw + line
                                zdoc = ZPLDocument()
                                zdoc.add_zpl_raw(raw)
                                print("Próba wysłania pliku:", vou.split(';')[2], "\b.zpl", "do drukarki:", ib.default_printer)
                                drukarka = NetworkPrinter(ib.default_printer)
                                drukarka.print_zpl(zdoc)
                                file.close()
                                
                        

                    btn_name_list = []

                    for k in last_vouchers:
                        ncv = int(k.split(";")[0])
                        for n in range(0, (len(last_vouchers) + 1)):
                            btn_name_list.append("btn" + str(n))
                        btn_name_list[ncv] = Button(to_print, text=ncv, font = "Tahoma 10 bold", width=2, command=lambda k=k : select(k))
                        btn_name_list[ncv].grid(column=c, row=r)
                        c += 1
                        if c == 4:
                            r += 1
                            c = 0
                    b01 = Button(self.tab3, text="ALL", font = "Tahoma 10 bold", width=7, command=select_all)
                    b01.place(relx=0.88, rely=0.17, anchor=NW)
                    b02 = Button(self.tab3, text="Drukuj", font = "Tahoma 10 bold", bg="#eb4c34", width=7, command=send_to_printer)
                    b02.place(relx=0.88, rely=0.24, anchor=NW)
                    
                    

                b1 = Button(self.tab3, text="Generuj", font="Tahoma 12 bold", fg='#eb4c34', bg='#474747', width=9, activebackground='#4768fe', border=3, command=generate)
                b1.place(relx=0.72, rely=0.05, anchor=NW)
                b1 = Button(self.tab3, text="Do druku", font="Tahoma 12 bold", fg='#eb4c34', bg='#474747',width=9, activebackground='#4768fe', border=3, command=print_voucher)
                b1.place(relx=0.86, rely=0.05, anchor=NW)

            elif tab_text == "LIST VOUCHERS":
                labelFrame4 = LabelFrame(self.tab4, text = "Lista voucherów", font="Verdana 12 bold italic")
                labelFrame4.place(relx = 0, rely = 0)
                
                def remove_voucher():
                   
                    ten = voucher_list.curselection()
                    for index in ten[::-1]:
                        voucher_list.delete(index)
                    ten = list(ten)
                    print("To jest ten:", ten)
                    for v in ten:
                        ib.rem_ticket(v, v)
                   
                    return
                
                def reprint_voucher():
                    reprint_buffer = []
                    current_list = voucher_list.curselection()
                    for ity in current_list:
                        vou = (str(voucher_list.get(ity)).split("         ")[2].strip())
                        reprint_buffer.append(vou)
                    
                    if len(reprint_buffer) < 1:
                        messagebox.showerror("Brak vouchera", "Wskaż co najmniej jedną pozycję!")
                        return
                    else:
                        for r_vou in reprint_buffer:
                                
                                with open("C:/iticket/default/voucher.zpl", "r") as main_f:
                                    try:
                                        with open("C:/iticket/printer_buffer/" + r_vou + ".zpl", "x", encoding='UTF8') as f: 
                                            for line in main_f:
                                                f.write(line)
                                    except:
                                        print("Plik", r_vou, "\b.zpl już istnieje.")
                                        
                                        
                                m_file = open("C:/iticket/printer_buffer/" + r_vou + ".zpl", "r", encoding='UTF8')
                                list_of_lines = m_file.readlines()
                                list_of_lines[13] = ("^FT144,258^A0N,43,45^FH\\^FD" + str(r_vou) + "^FS\n")
                                m_file = open("C:/iticket/printer_buffer/" + r_vou + ".zpl", "w", encoding='UTF8')
                                m_file.writelines(list_of_lines)
                                m_file.close()

                                raw = ''
                                                                
                                file = open("C:/iticket/printer_buffer/" + r_vou + ".zpl", "r", encoding='UTF8')
                                lines = file.readlines()
                        
                                for line in lines:
                                    raw = raw + line
                                zdoc = ZPLDocument()
                                zdoc.add_zpl_raw(raw)
                                print("Próba wysłania pliku:", r_vou, "\b.zpl", "do drukarki:", ib.default_printer)
                                drukarka = NetworkPrinter(ib.default_printer)
                                drukarka.print_zpl(zdoc)
                                file.close()
        
                        
                f = "Tahoma 10 bold"
                txt_color = "#eb4c34"
                pad_y = 1
                
                l_number = Label(labelFrame4, text = "Lp.", font=f, bd=0, fg=txt_color)
                l_c_time = Label(labelFrame4, text = "Czas stworzenia:", font=f, fg=txt_color)
                l_code = Label(labelFrame4, text = "Kod:", font=f, fg=txt_color)
                l_duration = Label(labelFrame4, text = "Czas:", font=f, fg=txt_color)
                l_note = Label(labelFrame4, text = "Opis:", font=f, fg=txt_color)
                l_fake = Label(labelFrame4)

                l_number.grid(row = 0, column = 0, sticky = W, pady=pad_y)
                l_c_time.grid(row = 0, column = 1, sticky = W, padx=25, pady=pad_y)
                l_code.grid(row = 0, column = 2, sticky = W, padx=21, pady=pad_y)
                l_duration.grid(row = 0, column = 3, sticky = W, padx=48, pady=pad_y)
                l_note.grid(row = 0, column = 4, sticky = W, pady=pad_y)
                l_fake.grid(row = 0, column = 5, sticky = W, pady=pad_y, padx=91)

                voucher_list = Listbox(self.tab4, width=90, height=32, bg="#f2e5dc", font="Tahoma 10 ", fg="BLACK", selectmode=EXTENDED)
                ib.get_tickets()
                for ticket in ib.tickets_to_label:
                    if len(ticket.split(";")[0]) == 1:
                        voucher_list.insert(ib.tickets_to_label.index(ticket), ("0" + ticket.replace(";", ("         "))))
                    else:
                        voucher_list.insert(ib.tickets_to_label.index(ticket), ticket.replace(";", ("         ")))
                voucher_list.place(relx=0, rely=0.07)

                remove_button = Button(self.tab4, text="USUŃ", font="Tahoma 12 bold", fg='#eb4c34', bg='#474747', width=9, activebackground='#4768fe', border=3, command=remove_voucher)
                print_button = Button(self.tab4, text="DRUKUJ", font="Tahoma 12 bold", fg='#eb4c34', bg='#474747', width=9, activebackground='#4768fe', border=3, command=reprint_voucher)

                remove_button.place(relx=0.82, rely=0.07)
                print_button.place(relx=0.82, rely=0.14)
    
            elif tab_text == "LIST ACTIVE GUESTS":

                def kick_out():
                    ib.unauthorize_guest(int(client_list.curselection()[0]))
                    client_list.delete(int(client_list.curselection()[0]))
                    return(print(client_list.curselection()))

                print(ib.get_connected_guest(1))
                labelFrame5 = LabelFrame(self.tab5, text = "Lista aktywnych gości", font="Verdana 12 bold italic")
                labelFrame5.place(relx = 0, rely = 0)   
                
                f = "Tahoma 10 bold"
                txt_color = "#eb4c34"
                pad_y = 1
                
                l_number = Label(labelFrame5, text = "Lp.", font=f, bd=0, fg=txt_color)
                l_name = Label(labelFrame5, text = "Nazwa:", font=f, fg=txt_color)
                l_mac = Label(labelFrame5, text = "MAC:", font=f, fg=txt_color)
                l_space = Label(labelFrame5)

                l_number.grid(row = 0, column = 0, sticky = W, pady=pad_y)
                l_name.grid(row = 0, column = 1, sticky = W, padx=23, pady=pad_y)
                l_mac.grid(row = 0, column = 2, sticky = W, padx=150, pady=pad_y)
                l_space.grid(row = 0, column = 3, sticky = W, pady=pad_y, padx=81)
                client_list = Listbox(self.tab5, width=90, height=32, bg="#f2e5dc", font="Tahoma 10 ", fg="BLACK", selectmode=SINGLE)
                
                             
                k = 1
                counter0 = 0
                for record in ib.guest_mac:
                    counter1 = len(str(record).strip("]").strip("[").replace("'", '').strip().split(',')[0])
                    print(str(record).strip("]").strip("[").replace("'", '').strip().split(',')[0], "---", counter1)

                    if counter1 > counter0:
                        counter0 = counter1
                        print("counter is changed on :", counter0)

                for user in ib.guest_mac:
                    user_to_list = str(user).strip("]").strip("[").replace("'", '').strip().split(',')

                    FORMAT = '%-9s  %-43s  %-12s'
                    print(FORMAT % (k, user_to_list[0], user_to_list[1]))                    
                    
                    client_list.insert(ib.guest_mac.index(user), FORMAT % (k, user_to_list[0], user_to_list[1]))
                    k += 1
                client_list.place(relx=0, rely=0.07)

                kick_client = Button(self.tab5, text="unieważnij", font="Tahoma 12 bold", fg='#eb4c34', bg='#474747', width=9, activebackground='#4768fe', border=3, command=kick_out)
                kick_client.place(relx=0.82, rely=0.07)

            elif tab_text == "ABOUT":
                labelFrame6 = LabelFrame(self.tab6, text = "O twórcy", font="Verdana 12 bold italic")
                labelFrame6.grid(column = 0, row = 0, padx = 8, pady = 4)
                label6 = Label(labelFrame6, text = "Cześć, dziękuję za skorzystanie z mojej aplikacji!\n\nIticket is created by\n Mateusz Sebastianowicz.",
                font="Tahoma 16 bold")
                label6.grid(column = 0, row = 1, pady = 50)


        self.title("iticket")
        self.geometry("800x600")
        self.resizable(0, 0)
        
        posR = int(self.winfo_screenwidth() / 2 - 400)
        posD = int(self.winfo_screenheight() / 2 - 400)
        self.geometry("+{}+{}".format(posR, posD))
        
        tabControl = ttk.Notebook(self)
        tabControl.bind("<<NotebookTabChanged>>", on_tab_selected)
        
        self.tab1 = ttk.Frame(tabControl)
        tabControl.add(self.tab1, text = "HOME")

        self.tab2 = ttk.Frame(tabControl)
        tabControl.add(self.tab2, text = "AP INFO")
        
        self.tab3 = ttk.Frame(tabControl)
        tabControl.add(self.tab3, text = "CREATE VOUCHER")

        self.tab4 = ttk.Frame(tabControl)
        tabControl.add(self.tab4, text = "LIST VOUCHERS")

        self.tab5 = ttk.Frame(tabControl)
        tabControl.add(self.tab5, text = "LIST ACTIVE GUESTS")

        self.tab6 = ttk.Frame(tabControl)
        tabControl.add(self.tab6, text = "ABOUT")
        
        tabControl.pack(expand = 1, fill = "both")

                

app = App()
app.mainloop()