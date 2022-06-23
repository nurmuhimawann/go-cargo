import tkinter as tk
from tkinter import messagebox, StringVar
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

url = "https://go-cargo.herokuapp.com"


class Auth(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.resizable(False, False)
        self.title("Go Cargo")
        self.geometry("1305x780")

        container = tk.Frame(self)
        container.pack(side="left", fill="both", expand=True)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        self.frames["Login"] = Login(parent=container, controller=self)
        self.frames["Register"] = Register(parent=container, controller=self)

        self.frames["Login"].grid(row=0, column=0, sticky="nsew")
        self.frames["Register"].grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def backgroundImg(self):
        urlImage = requests.get(
            "https://firebasestorage.googleapis.com/v0/b/go-cargo-12c47.appspot.com/o/login.jpg?alt=media&token=2b0be545-df36-4e4f-bda1-86bd6427a5ea")
        img_data = urlImage.content
        img_resize = Image.open(BytesIO(img_data)).resize(
            (1305, 780), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(img_resize)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def handleLogin(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        response = requests.get(f"{url}/login/{email}/{password}")

        if response.status_code == 200:
            messagebox.showinfo("Informasi", "Login berhasil")

            user = response.json()

            global userName
            global userEmail

            userName = user["name"]
            userEmail = user["email"]

            self.controller.destroy()

            if user["role"] == "customer":
                UserMenu()
            elif user["role"] == "shipper":
                AdminMenu()

        else:
            messagebox.showerror("Informasi", "Login gagal")

    def handleRegister(self, role):
        name = self.entry_name.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        gender = self.var_gender.get()
        age = int(self.entry_age.get())

        response1 = requests.get(f"{url}/users/{email}")

        if response1.status_code == 200:
            messagebox.showerror("Informasi", "Email sudah digunakan")
        else:
            userData = {
                "name": name,
                "email": email,
                "password": password,
                "gender": gender,
                "age": age,
                "role": role,
            }

            response2 = requests.post(f"{url}/users", userData)

            if response2.status_code == 200:
                messagebox.showinfo("Informasi", "Akun berhasil didaftarkan")
                self.entry_name.delete(0, "end")
                self.entry_email.delete(0, "end")
                self.entry_password.delete(0, "end")
                self.entry_age.delete(0, "end")
            else:
                messagebox.showerror("Informasi", "Akun gagal didaftarkan")


class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Auth.backgroundImg(self)

        tk.Label(self, text="Email", width=20,
                font=("bold", 10)).place(x=150, y=350)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=280, y=350)

        tk.Label(self, text="Password", width=20,
                font=("bold", 10)).place(x=150, y=400)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.place(x=280, y=400)

        tk.Button(
            self, text="Login", bg="dodger blue", fg="white", command=lambda: Auth.handleLogin(self)
        ).place(x=250, y=450, height=50, width=100)
        tk.Button(
            self, text="Register", command=lambda: controller.show_frame("Register")
        ).place(x=320, y=520, height=50, width=100)
        tk.Button(
            self,
            text="Exit",
            bg="brown",
            fg="white",
            command=lambda: controller.destroy(),
        ).place(x=200, y=520, height=50, width=100)


class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        Auth.backgroundImg(self)

        tk.Label(self, text="Daftar Akun Baru",
                width=20, font=("bold", 20)).place(x=150, y=280)

        tk.Label(self, text="Nama Lengkap",
                width=20, font=("bold", 10)).place(x=150, y=340)
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=300, y=340)

        tk.Label(self, text="Email", width=20,
                font=("bold", 10)).place(x=150, y=370)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=300, y=370)

        tk.Label(self, text="Password", width=20,
                font=("bold", 10)).place(x=150, y=400)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.place(x=300, y=400)

        tk.Label(self, text="Jenis Kelamin",
                width=20, font=("bold", 10)).place(x=150, y=430)

        self.var_gender = StringVar()

        self.select_gender = tk.Radiobutton(
            self, text="Pria", padx=5, value="pria", variable=self.var_gender
        ).place(x=280, y=430)
        self.select_gender = tk.Radiobutton(
            self, text="Wanita", padx=20, value="wanita", variable=self.var_gender
        ).place(x=330, y=430)

        tk.Label(self, text="Umur:", width=20,
                font=("bold", 10)).place(x=150, y=460)

        self.entry_age = tk.Entry(self)
        self.entry_age.place(x=300, y=460)

        tk.Button(
            self,
            text="Daftar",
            width=20,
            bg="dodger blue",
            fg="white",
            command=lambda: Auth.handleRegister(self, "customer"),
        ).place(x=150, y=520)

        tk.Button(
            self,
            text="Back to login",
            width=20,
            command=lambda: controller.show_frame("Login"),
        ).place(x=320, y=520)


ScrollOnItemsList = []


class ScrollBar(tk.Frame):
    def __init__(self, parent):
        self.height = 780
        self.width = 200

        tk.Frame.__init__(self, parent, width=self.width,
                        height=self.height, bg="grey")
        self.place(x=0, y=-2)

        self.last_delta = 0
        parent.update()

        self.c_frame = tk.Frame(self, width=self.width,
                                height=self.height, bg="grey")
        self.c_frame.place(x=0, y=0)
        self.c_Canvas = tk.Canvas(
            self.c_frame, width=self.width, height=self.height, bd=-2, bg="#232323"
        )
        scrollbar = tk.Scrollbar(
            self.c_frame, orient="vertical", command=self.c_Canvas.yview, bg="grey"
        )
        self.scrollframe = tk.Frame(self.c_Canvas)
        self.scrollframe.place(x=0, y=0)

        self.scrollframe.bind(
            "<Configure>",
            lambda e: self.c_Canvas.configure(
                scrollregion=self.c_Canvas.bbox("all")),
        )
        self.c_Canvas.create_window(
            (0, 0), window=self.scrollframe, anchor="nw")

        self.c_Canvas.configure(yscrollcommand=scrollbar.set)
        self.c_Canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


side_bar_tab_list = []


class SideBar(ScrollBar):
    def __init__(self, parent, *args, **kwargs):
        ScrollBar.__init__(self, parent)
        self.color = "#232323"

    def finish(self):
        self.select_first_tab()

    def add_button(self, text, command, tab=True):
        SideBarButton(self.scrollframe, text, command, tab=tab)

    def select_first_tab(self):
        i = side_bar_tab_list[0]
        i.click()


class SideBarButton(tk.Canvas):
    def __init__(self, parent, text, command, tab=True, *args, **kwargs):

        self.frame_color = "#232323"
        self.hover_color = "#4D4c4c"
        self.hover_border_color = "grey"
        self.is_tab = tab

        self.selected = False

        self.command = command

        tk.Canvas.__init__(
            self,
            parent,
            width=198,
            height=35,
            bg=self.frame_color,
            highlightthickness=1,
            highlightbackground=self.frame_color,
            *args,
            **kwargs,
        )
        self.pack()

        self.text = tk.Label(
            self, text=text, font="Segoe 10", bg=self.frame_color, fg="lightgrey"
        )
        self.text.place(x=40, y=10)

        self.bind("<Enter>", self.hover)
        self.bind("<Button-1>", self.click)
        if self.is_tab == False:
            self.bind("<ButtonRelease-1>", self.unclick)

        self.text.bind("<Enter>", self.hover)
        self.text.bind("<Button-1>", self.click)
        if self.is_tab == False:
            self.text.bind("<ButtonRelease-1>", self.unclick)
        if self.is_tab:
            side_bar_tab_list.append(self)
        ScrollOnItemsList.append(self)

    def hover(self, event=None):
        if self.selected == False:
            self.bind("<Leave>", self.unhover)
            self.config(
                highlightbackground=self.hover_border_color, bg=self.hover_color
            )
            self.text.config(bg=self.hover_color)

    def unhover(self, event=None):
        self.config(highlightbackground=self.frame_color, bg=self.frame_color)
        self.text.config(bg=self.frame_color)

    def click(self, event=None):

        if self.is_tab:
            self.bind("<Leave>", str)
            for i in side_bar_tab_list:
                i.unhover()
                i.selected = False

        self.selected = True

        self.config(bg=self.hover_border_color)
        self.text.config(bg=self.hover_border_color)

        self.command()

    def unclick(self, event=None):
        self.selected = False
        self.config(bg=self.hover_color)
        self.text.config(bg=self.hover_color)


active_page = []


class Page(tk.Frame):
    def __init__(self, parent):
        self.width = 1350
        self.height = 780
        # remove old page
        try:
            active_page[0].delete()
        except:
            pass

        # create new tab
        tk.Frame.__init__(
            self, parent, bg="white", height=self.height, width=self.width
        )

        # place page
        self.place(x=0, y=0)

        active_page.append(self)

    def delete(self):
        global active_page
        active_page.remove(self)
        self.destroy()


class UserMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Customer Menu")
        self.resizable(False, False)
        self.geometry("1305x780")

        main_frame = tk.Frame(self, bg="white", width=1350, height=1000)
        main_frame.place(x=200, y=0)

        sidebar = SideBar(self)

        sidebar.add_button("Home", lambda: UserHome(main_frame))
        sidebar.add_button("Cek Pengiriman", lambda: UserShipping(main_frame))
        sidebar.add_button("Profile", lambda: UserProfile(main_frame))
        sidebar.add_button("Exit", lambda: exit(self))
        sidebar.finish()

    def exit(self):
        self.destroy()


class UserHome(Page):
    def __init__(self, parent):

        # init page/ delete old page
        Page.__init__(self, parent)

        response = requests.get(f"{url}/port")

        self.results = response.json()

        port = []

        for index, element in enumerate(self.results):
            port.append(element["city_name"])

        self.optOrigin = tk.StringVar(self)  # variable
        self.optOrigin.set(port[0])  # default value

        tk.Label(self, text="Pilih kota asal").place(x=20, y=30)
        tk.OptionMenu(self, self.optOrigin, *port).place(x=20, y=60)

        self.optDestination = tk.StringVar(self)  # variable
        self.optDestination.set(port[0])  # default value

        tk.Label(self, text="Pilih kota tujuan").place(x=180, y=30)
        tk.OptionMenu(self, self.optDestination,
                      *port).place(x=180, y=60)

        tk.Label(self, text="Berat (kg)").place(x=330, y=30)
        self.entry_weight = tk.Entry(self)
        self.entry_weight.place(x=330, y=60)

        tk.Button(
            self,
            text="submit",
            bg="dodger blue",
            fg="white",
            command=self.handleShipping,
        ).place(x=500, y=60, height=30, width=100)

    def handleShipping(self):
        origin = self.optOrigin.get()
        destination = self.optDestination.get()
        weight = int(self.entry_weight.get())

        shippingData = {
            "customer": userName,
            "origin": origin,
            "destination": destination,
            "weight": weight,
        }

        response = requests.post(f"{url}/shipping", shippingData)
        shipping = response.json()

        if response.status_code == 200:
            messagebox.showinfo("Informasi", "Barang berhasil ditambahkan")
            self.entry_weight.delete(0, "end")

            tk.Label(self, text="Detail Pengiriman :").place(x=20, y=120)

            tk.Label(self, text="Kota Asal").place(x=20, y=150)
            tk.Label(
                self, text=shipping["origin"], anchor="w", width=100, bg="white"
            ).place(x=150, y=150)

            tk.Label(self, text="Kota Tujuan").place(x=20, y=180)
            tk.Label(
                self, text=shipping["destination"], anchor="w", width=100, bg="white"
            ).place(x=150, y=180)

            tk.Label(self, text="Berat Barang").place(x=20, y=210)
            tk.Label(
                self, text=shipping["weight"], anchor="w", width=100, bg="white"
            ).place(x=150, y=210)

            tk.Label(self, text="Biaya Pengiriman").place(x=20, y=240)
            tk.Label(
                self, text=shipping["cost"], anchor="w", width=100, bg="white"
            ).place(x=150, y=240)

            tk.Label(self, text="Estimasi Pengiriman").place(x=20, y=270)

            tk.Label(
                self,
                text=f"{shipping['estimation']} hari",
                anchor="w",
                width=100,
                bg="white",
            ).place(x=150, y=270)
        else:
            messagebox.showerror("Informasi", "Barang gagal ditambahkan")


class UserShipping(Page):
    def __init__(self, parent):
        # init page/ delete old page
        Page.__init__(self, parent)

        tk.Label(
            self, width=20, text="pengirim", anchor="w", bg="white").place(x=20, y=60)
        tk.Label(
            self, width=20, text="kota asal", anchor="w", bg="white").place(x=180, y=60)
        tk.Label(
            self, width=20, text="kota tujuan", anchor="w", bg="white"
        ).place(x=320, y=60)
        tk.Label(
            self, width=20, text="berat (kg)", anchor="w", bg="white"
        ).place(x=480, y=60)
        tk.Label(
            self, width=20, text="status", anchor="w", bg="white").place(x=580, y=60)

        response = requests.get(f"{url}/shippingcust/{userName}")
        results = response.json()

        for i in range(len(results)):
            self.labelShip = tk.Label(
                self, width=20, text=results[i]["shipper"], anchor="w", bg="white"
            )
            self.labelShip.place(x=20, y=(i + 1) * 30 + 60)

            if results[i]["shipper"] == "":
                self.labelShip.config(text="-")

            tk.Label(
                self, width=20, text=results[i]["origin"], anchor="w", bg="white"
            ).place(x=180, y=(i + 1) * 30 + 60)
            tk.Label(
                self, width=20, text=results[i]["destination"], anchor="w", bg="white"
            ).place(x=320, y=(i + 1) * 30 + 60)
            tk.Label(
                self, width=20, text=results[i]["weight"], anchor="w", bg="white"
            ).place(x=480, y=(i + 1) * 30 + 60)

            self.labelStatus = tk.Label(self, width=20, anchor="w", bg="white")
            self.labelStatus.place(
                x=580, y=(i + 1) * 30 + 60)
            if results[i]["status"] == 1:
                self.labelStatus.config(text="Sudah terkirim")
            else:
                self.labelStatus.config(text="Proses pengiriman")


class UserProfile(Page):
    def __init__(self, parent):
        # init page/ delete old page
        Page.__init__(self, parent)

        response = requests.get(f"{url}/users/{userEmail}")
        results = response.json()

        tk.Label(
            self,
            text="Detail Profile",
            width=20,
            bg="white",
            anchor="w",
            font=("bold", 20),
        ).place(x=20, y=60)

        tk.Label(self, text="Nama", width=20,
                bg="white", anchor="w").place(x=20, y=120)
        tk.Label(
            self, text=results["name"], width=20, bg="white", anchor="w").place(x=100, y=120)

        tk.Label(self, text="Email",
                width=20, bg="white", anchor="w").place(x=20, y=150)
        tk.Label(
            self, text=results["email"], width=20, bg="white", anchor="w").place(x=100, y=150)

        tk.Label(
            self, text="Jenis Kelamin", width=20, bg="white", anchor="w"
        ).place(x=20, y=180)
        tk.Label(
            self, text=results["gender"], width=20, bg="white", anchor="w"
        ).place(x=100, y=180)

        tk.Label(self, text="Umur", width=20,
                            bg="white", anchor="w").place(x=20, y=210)

        tk.Label(
            self, text=results["age"], width=20, bg="white", anchor="w").place(x=100, y=210)


class AdminMenu(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Shipper Menu")
        self.resizable(False, False)
        self.geometry("1305x780")

        main_frame = tk.Frame(self, bg="white", width=1350, height=1000)
        main_frame.place(x=200, y=0)

        sidebar = SideBar(self)

        sidebar.add_button("Home", lambda: AdminHome(main_frame))
        sidebar.add_button("Storage", lambda: AdminStorage(main_frame))
        sidebar.add_button("Profile", lambda: AdminProfile(main_frame))
        sidebar.add_button("Exit", lambda: exit(self))
        sidebar.finish()

    def exit(self):
        self.destroy()


class AdminHome(Page):
    def __init__(self, parent):
        # init page/ delete old page
        Page.__init__(self, parent)

        response = requests.get(f"{url}/port")
        self.results = response.json()
        portData = []

        for index, element in enumerate(self.results):
            portData.append(element["city_name"])

        self.optPort = tk.StringVar(self)  # variable
        self.optPort.set(portData[0])  # default value

        tk.Label(self, text="Pilih port").place(x=20, y=60)
        tk.OptionMenu(self, self.optPort, *portData).place(x=150, y=60)

        tk.Button(
            self, text="check", bg="dodger blue", fg="white", command=self.handlePort
        ).place(x=350, y=60, height=30, width=100)

    def handlePort(self):
        tk.Label(
            self, width=20, text="type", anchor="w", bg="white").place(x=20, y=120)
        tk.Label(
            self, width=20, text="capacity (kg)", anchor="w", bg="white"
        ).place(x=180, y=120)
        tk.Label(
            self, width=20, text="status", anchor="w", bg="white").place(x=320, y=120)
        tk.Label(
            self, width=20, text="action", anchor="w", bg="white").place(x=420, y=120)

        self.port = self.optPort.get()
        response = requests.get(f"{url}/port/{self.port}")
        results = response.json()

        for i in range(7):
            tk.Label(
                self,
                width=20,
                text=results["transport"][i]["type"],
                anchor="w",
                bg="white",
            ).place(x=20, y=(i + 1) * 30 + 120)

            tk.Label(
                self,
                width=20,
                text=results["transport"][i]["capacity"],
                anchor="w",
                bg="white",
            ).place(x=180, y=(i + 1) * 30 + 120)

            self.labelStatus = tk.Label(self, width=20, anchor="w", bg="white")
            self.labelStatus.place(
                x=320, y=(i + 1) * 30 + 120)

            if results["transport"][i]["status"] == 0:
                self.labelStatus.configure(text="Ready")

                tk.Button(
                    self,
                    text="kirim",
                    width=20,
                    bg="dodger blue",
                    command=lambda type=results["transport"][i][
                        "type"
                    ], capacity=results["transport"][i]["capacity"]: self.handleSend(
                        type, capacity
                    ),
                ).place(x=420, y=(i + 1) * 30 + 120)
            else:
                self.labelStatus.configure(text="On going")
                tk.Button(
                    self,
                    text="selesai",
                    width=20,
                    bg="yellow",
                    command=lambda type=results["transport"][i][
                        "type"
                    ]: self.handleDone(type),
                ).place(x=420, y=(i + 1) * 30 + 120)

    def handleSend(self, type, capacity):
        value = []
        weight = []
        item_id = []

        response1 = requests.get(f"{url}/storage/{self.port}/0")
        results = response1.json()

        for i in range(len(results)):
            deliveryDate = datetime.strptime(
                results[i]["deliveryDate"], "%Y-%m-%d %H:%M:%S"
            )
            nowDate = datetime.now()

            delivDate = int(deliveryDate.strftime("%Y%m%d%H%M%S"))
            nowInt = int(nowDate.strftime("%Y%m%d%H%M%S"))
            remaining = nowInt - delivDate

            value.append(remaining)
            weight.append(results[i]["weight"])
            item_id.append(results[i]["_id"])

        n = len(value)

        hasil = self.knapsack_brute(capacity, weight, value, n)

        if len(hasil[1]) == 0:
            messagebox.showerror("Informasi", "Tidak ada barang yang dikirim")
        else:
            tk.Label(
                self, width=20, text="customer", anchor="w", bg="white"
            ).grid(row=0, column=0)

            tk.Label(
                self, width=20, text="kota asal", anchor="w", bg="white"
            ).grid(row=0, column=1)

            tk.Label(
                self, width=20, text="kota tujuan", anchor="w", bg="white"
            ).grid(row=0, column=2)

            tk.Label(
                self, width=20, text="berat (kg)", anchor="w", bg="white"
            ).grid(row=0, column=3)

            listGoods = [[] for i in range(len(hasil[1]))]

            for i, v in enumerate(hasil[1]):
                requests.put(
                    f"{url}/shipping/{item_id[v]}",
                    {"shipper": userName},
                )

                listGoods[i].append(results[v]["customer"])
                listGoods[i].append(results[v]["origin"])
                listGoods[i].append(results[v]["destination"])
                listGoods[i].append(results[v]["weight"])

                for j in range(4):
                    tk.Label(
                        self, width=20, text=listGoods[i][j], anchor="w", bg="white"
                    ).grid(row=i + 1, column=j)
                    tk.Label(
                        self, width=20, text=listGoods[i][j], anchor="w", bg="white"
                    ).grid(row=i + 1, column=j)
                    tk.Label(
                        self, width=20, text=listGoods[i][j], anchor="w", bg="white"
                    ).grid(row=i + 1, column=j)
                    tk.Label(
                        self, width=20, text=listGoods[i][j], anchor="w", bg="white"
                    ).grid(row=i + 1, column=j)

            portData = {"type": type, "status": 1}

            response2 = requests.put(
                f"{url}/port/{self.port}", portData
            )

            if response2.status_code == 200:
                messagebox.showinfo("Informasi", "Barang telah dikirim")
            else:
                messagebox.showerror("Informasi", "Barang gagal dikirim")

    def knapsack_brute(self, W, wt, val, n):
        if n == 0 or W == 0:
            return [0, []]

        elif wt[n - 1] > W:
            return self.knapsack_brute(W, wt, val, n - 1)

        simpan1 = self.knapsack_brute(W - wt[n - 1], wt, val, n - 1)
        simpan2 = self.knapsack_brute(W, wt, val, n - 1)

        nilai1 = val[n - 1] + simpan1[0]
        nilai2 = simpan2[0]

        nilai_max = max(nilai1, nilai2)

        if nilai_max == nilai1:
            simpan1[0] = nilai_max
            index_item = [n - 1]
            simpan1[1].extend(index_item)
            return simpan1
        else:
            return simpan2

    def handleDone(self, type):
        portData = {"type": type, "status": 0}

        response2 = requests.put(f"{url}/port/{self.port}", portData)

        if response2.status_code == 200:
            messagebox.showinfo("Informasi", "Barang selesai dikirim")
        else:
            messagebox.showerror("Informasi", "Barang gagal dikirim")


class AdminStorage(Page):
    def __init__(self, parent):
        # init page/ delete old page
        Page.__init__(self, parent)

        response = requests.get(f"{url}/port")
        self.results = response.json()
        portData = []

        for index, element in enumerate(self.results):
            portData.append(element["city_name"])

        self.optPort = tk.StringVar(self)  # variable
        self.optPort.set(portData[0])  # default value

        tk.Label(self, text="Pilih port").place(x=20, y=60)
        tk.OptionMenu(self, self.optPort, *portData).place(x=150, y=60)

        tk.Button(
            self, text="check", bg="dodger blue", fg="white", command=self.handleStorage
        ).place(x=350, y=60, height=30, width=100)

    def handleStorage(self):
        tk.Label(
            self, width=20, text="customer", anchor="w", bg="white").place(x=20, y=120)
        tk.Label(
            self, width=20, text="kota asal", anchor="w", bg="white").place(x=180, y=120)
        tk.Label(
            self, width=20, text="kota tujuan", anchor="w", bg="white"
        ).place(x=320, y=120)
        tk.Label(
            self, width=20, text="berat (kg)", anchor="w", bg="white"
        ).place(x=450, y=120)

        origin = self.optPort.get()

        response = requests.get(f"{url}/storage/{origin}/0")
        results = response.json()

        if len(results) == 0:
            messagebox.showerror("informasi", "Tidak ada barang")
        else:
            for i in range(len(results)):
                tk.Label(
                    self, width=20, text=results[i]["customer"], anchor="w", bg="white"
                ).place(x=20, y=(i + 1) * 30 + 120)
                tk.Label(
                    self, width=20, text=results[i]["origin"], anchor="w", bg="white"
                ).place(x=180, y=(i + 1) * 30 + 120)
                tk.Label(
                    self, width=20, text=results[i]["destination"], anchor="w", bg="white"
                ).place(x=320, y=(i + 1) * 30 + 120)
                tk.Label(
                    self, width=20, text=results[i]["weight"], anchor="w", bg="white"
                ).place(x=480, y=(i + 1) * 30 + 120)


class AdminProfile(Page):
    def __init__(self, parent):
        # init page/ delete old page
        Page.__init__(self, parent)

        response = requests.get(f"{url}/users/{userEmail}")
        results = response.json()

        tk.Label(
            self,
            text="Detail Profile",
            width=20,
            bg="white",
            anchor="w",
            font=("bold", 20),
        ).place(x=20, y=60)

        tk.Label(self, text="Nama", width=20,
                bg="white", anchor="w").place(x=20, y=120)
        tk.Label(
            self, text=results["name"], width=20, bg="white", anchor="w").place(x=100, y=120)

        tk.Label(self, text="Email",
                width=20, bg="white", anchor="w").place(x=20, y=150)
        tk.Label(
            self, text=results["email"], width=20, bg="white", anchor="w").place(x=100, y=150)

        tk.Label(
            self, text="Jenis Kelamin", width=20, bg="white", anchor="w"
        ).place(x=20, y=180)
        tk.Label(
            self, text=results["gender"], width=20, bg="white", anchor="w"
        ).place(x=100, y=180)

        tk.Label(self, text="Umur", width=20,
                            bg="white", anchor="w").place(x=20, y=210)

        tk.Label(
            self, text=results["age"], width=20, bg="white", anchor="w").place(x=100, y=210)

        tk.Label(
            self, text="Tambah Pengirim Baru", width=20, bg="white", font=("bold", 20)
        ).place(x=400, y=60)

        tk.Label(self, text="Nama Lengkap", width=20).place(x=400, y=120)
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=550, y=120)

        tk.Label(self, text="Email", width=20).place(x=400, y=150)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=550, y=150)

        tk.Label(self, text="Password", width=20).place(x=400, y=180)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.place(x=550, y=180)

        tk.Label(self, text="Jenis Kelamin", width=20).place(x=400, y=210)

        self.var_gender = StringVar()

        self.select_gender = tk.Radiobutton(
            self, text="Pria", padx=5, value="pria", variable=self.var_gender
        ).place(x=550, y=210)
        self.select_gender = tk.Radiobutton(
            self, text="Wanita", padx=20, value="wanita", variable=self.var_gender
        ).place(x=600, y=210)

        tk.Label(self, text="Umur:", width=20).place(x=400, y=240)

        self.entry_age = tk.Entry(self)
        self.entry_age.place(x=550, y=240)

        tk.Button(
            self,
            text="Tambah pengirim",
            width=20,
            bg="dodger blue",
            fg="white",
            command=lambda: Auth.handleRegister(self, "shipper"),
        ).place(x=400, y=280)


if __name__ == "__main__":
    app = Auth()
    app.mainloop()
