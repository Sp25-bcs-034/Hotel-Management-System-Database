import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
    client.server_info()
    db = client["hotel_management"]
    CONNECTED = True
    ERR = ""
except Exception as ex:
    CONNECTED = False
    ERR = str(ex)

# ── COLOURS ───────────────────────────────────────────────────────────────────
BG      = "#1a3c34"
SIDEBAR = "#14302a"
WHITE   = "#ffffff"
GREEN   = "#2d6a4f"
ACCENT  = "#40916c"
GOLD    = "#f4a261"
DANGER  = "#e63946"
BTN_GRN = "#52b788"
SUBTEXT = "#95d5b2"

F_TITLE = ("Arial", 18, "bold")
F_HEAD  = ("Arial", 12, "bold")
F_LABEL = ("Arial", 10, "bold")
F_BODY  = ("Arial", 10)
F_BTN   = ("Arial", 10, "bold")
F_SMALL = ("Arial",  8)

# ── ROOT ──────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("1300x730")
root.configure(bg=BG)
root.resizable(True, True)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
    background=WHITE, foreground="#1a3c34",
    fieldbackground=WHITE, rowheight=26, font=F_BODY)
style.configure("Treeview.Heading",
    background="#1a3c34", foreground=WHITE,
    font=F_LABEL, relief="flat", padding=5)
style.map("Treeview",
    background=[("selected", ACCENT)],
    foreground=[("selected", WHITE)])

# ── HEADER ────────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=SIDEBAR, height=60)
header.pack(side="top", fill="x")
header.pack_propagate(False)
tk.Label(header, text="  Hotel Management System",
         font=F_TITLE, bg=SIDEBAR, fg=WHITE).pack(side="left", padx=12, pady=10)
badge = "●  Connected" if CONNECTED else "●  Offline"
tk.Label(header, text=badge, font=F_LABEL, bg=SIDEBAR,
         fg=BTN_GRN if CONNECTED else DANGER).pack(side="right", padx=20)

# ── BODY ──────────────────────────────────────────────────────────────────────
body = tk.Frame(root, bg=BG)
body.pack(fill="both", expand=True)

# Scrollable sidebar
sidebar_outer = tk.Frame(body, bg=SIDEBAR, width=200)
sidebar_outer.pack(side="left", fill="y")
sidebar_outer.pack_propagate(False)
canvas_sb = tk.Canvas(sidebar_outer, bg=SIDEBAR, highlightthickness=0, width=200)
sb_scroll = tk.Scrollbar(sidebar_outer, orient="vertical", command=canvas_sb.yview)
canvas_sb.configure(yscrollcommand=sb_scroll.set)
sb_scroll.pack(side="right", fill="y")
canvas_sb.pack(side="left", fill="both", expand=True)
sidebar = tk.Frame(canvas_sb, bg=SIDEBAR)
canvas_sb.create_window((0, 0), window=sidebar, anchor="nw", width=190)
sidebar.bind("<Configure>", lambda e: canvas_sb.configure(scrollregion=canvas_sb.bbox("all")))

main_area = tk.Frame(body, bg=BG)
main_area.pack(side="left", fill="both", expand=True, padx=14, pady=10)

# ── ALL 21 PAGES ──────────────────────────────────────────────────────────────
PAGE_NAMES = [
    "Guest", "Booking", "Invoice", "Staff",
    "Hotel", "Room", "Amenity",
    "MemberGuest", "WalkingGuest", "Suit",
    "HousekeepingTask", "MaintenanceStaff", "FrontDeskStaff", "StaffProfile", "MaintainsRoom",
    "HotelPhone", "GuestPhone", "StaffPhone",
    "HasAmenity", "PerformsTask",
    "SingleRoom", "DoubleRoom", "RoomStatusLog"
]

NAV_LABELS = {
    "Guest":            "  Guest",
    "Booking":          "  Booking",
    "Invoice":          "  Invoice",
    "Staff":            "  Staff",
    "Hotel":            "  Hotel",
    "Room":             "  Room",
    "Amenity":          "  Amenity",
    "MemberGuest":      "  Member Guest",
    "WalkingGuest":     "  Walking Guest",
    "Suit":             "  Suit",
    "HousekeepingTask": "  Housekeeping Task",
    "MaintenanceStaff": "  Maintenance Staff",
    "FrontDeskStaff":   "  Front Desk Staff",
    "StaffProfile":     "  Staff Profile",
    "MaintainsRoom":    "  Maintains Room",
    "HotelPhone":       "  Hotel Phone",
    "GuestPhone":       "  Guest Phone",
    "StaffPhone":       "  Staff Phone",
    "HasAmenity":       "  Has Amenity",
    "PerformsTask":     "  Performs Task",
    "SingleRoom":       "  Single Room",
    "DoubleRoom":       "  Double Room",
    "RoomStatusLog":    "  Room Status Log",
}

pages = {n: tk.Frame(main_area, bg=BG) for n in PAGE_NAMES}
nav_btns = []

def show_page(name):
    for p in pages.values():
        p.pack_forget()
    pages[name].pack(fill="both", expand=True)
    for b in nav_btns:
        active = b._page_name == name
        b.configure(bg=BTN_GRN if active else SIDEBAR,
                    fg=WHITE   if active else SUBTEXT)

tk.Label(sidebar, text="COLLECTIONS", font=F_SMALL,
         bg=SIDEBAR, fg=SUBTEXT).pack(pady=(16, 4), anchor="w", padx=10)

for name in PAGE_NAMES:
    b = tk.Button(sidebar, text=NAV_LABELS[name],
                  font=F_BTN, bg=SIDEBAR, fg=SUBTEXT,
                  activebackground=BTN_GRN, activeforeground=WHITE,
                  bd=0, pady=9, anchor="w", cursor="hand2",
                  command=lambda n=name: show_page(n))
    b._page_name = name
    b.pack(fill="x", padx=6, pady=2)
    nav_btns.append(b)

tk.Label(sidebar, text="hotel_management", font=F_SMALL,
         bg=SIDEBAR, fg=SUBTEXT).pack(pady=14, anchor="w", padx=10)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def make_tree(parent, cols, widths):
    card = tk.Frame(parent, bg=ACCENT, padx=2, pady=2)
    card.pack(fill="both", expand=True, pady=4)
    inner = tk.Frame(card, bg=WHITE)
    inner.pack(fill="both", expand=True)
    tree = ttk.Treeview(inner, columns=cols, show="headings", selectmode="browse")
    for i, c in enumerate(cols):
        tree.heading(c, text=c.upper().replace("_", " "))
        tree.column(c, width=widths[i], anchor="w", minwidth=40)
    vsb = ttk.Scrollbar(inner, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(inner, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    inner.rowconfigure(0, weight=1)
    inner.columnconfigure(0, weight=1)
    return tree

def fill_tree(tree, rows):
    tree.delete(*tree.get_children())
    for r in rows:
        tree.insert("", "end", values=[str(v) if v is not None else "" for v in r])

def hdr(parent, title, sub=""):
    tk.Label(parent, text=title, font=F_HEAD, bg=BG, fg=WHITE).pack(anchor="w", pady=(0,2))
    if sub:
        tk.Label(parent, text=sub, font=F_BODY, bg=BG, fg=SUBTEXT).pack(anchor="w")
    ttk.Separator(parent).pack(fill="x", pady=(4,6))

def action_btns(parent, btns):
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", pady=(0,6))
    for txt, cmd, color in btns:
        tk.Button(f, text=txt, font=F_BTN, bg=color, fg=WHITE,
                  bd=0, padx=12, pady=5, cursor="hand2",
                  command=cmd).pack(side="left", padx=4)

def popup(title, fields, on_submit, defaults=None):
    win = tk.Toplevel(root)
    win.title(title)
    win.configure(bg=BG)
    win.geometry(f"420x{min(80 + len(fields)*54, 600)}")
    entries = {}
    container = tk.Frame(win, bg=BG)
    container.pack(fill="both", expand=True)
    cv = tk.Canvas(container, bg=BG, highlightthickness=0)
    sb = tk.Scrollbar(container, orient="vertical", command=cv.yview)
    cv.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    cv.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(cv, bg=BG)
    cv.create_window((0,0), window=inner, anchor="nw", width=400)
    inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
    for f in fields:
        tk.Label(inner, text=f, font=F_LABEL, bg=BG, fg=WHITE).pack(anchor="w", padx=22, pady=(10,0))
        e = tk.Entry(inner, font=F_BODY, bg=WHITE, fg="#1a3c34",
                     insertbackground="#1a3c34", relief="flat",
                     highlightthickness=2, highlightbackground=ACCENT, highlightcolor=BTN_GRN)
        if defaults and f in defaults and defaults[f] is not None:
            e.insert(0, str(defaults[f]))
        e.pack(fill="x", padx=22)
        entries[f] = e
    tk.Button(inner, text="  Submit  ", font=F_BTN, bg=BTN_GRN, fg=WHITE,
              bd=0, padx=16, pady=6, cursor="hand2",
              command=lambda: on_submit(entries, win)).pack(pady=14)

def safe_int(v):
    try: return int(v)
    except: return v

def safe_float(v):
    try: return float(v)
    except: return v

# ══════════════════════════════════════════════════════════════════════════════
# 1. GUEST
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Guest"]
hdr(pg, "Guest Collection", "Manage all registered guests")
g_cols = ["guestid","first_name","last_name","email","dob"]
g_tree = make_tree(pg, g_cols, [70,115,115,215,105])

def load_guests():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(g_tree, [[d.get(c,"") for c in g_cols] for d in db.guest.find({},{"_id":0})])

def insert_guest():
    def submit(e, win):
        doc = {f: e[f].get() for f in g_cols}
        doc["guestid"] = safe_int(doc["guestid"])
        db.guest.insert_one(doc); load_guests()
        messagebox.showinfo("Done","Guest inserted!"); win.destroy()
    popup("Insert Guest", g_cols, submit)

def update_guest():
    sel = g_tree.selection()
    if not sel: messagebox.showwarning("!","Select a guest first"); return
    vals = g_tree.item(sel[0])["values"]
    def submit(e, win):
        db.guest.update_one({"guestid": safe_int(vals[0])},
            {"$set": {f: e[f].get() for f in g_cols[1:]}})
        load_guests(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Guest", g_cols[1:], submit, dict(zip(g_cols, vals)))

def delete_guest():
    sel = g_tree.selection()
    if not sel: messagebox.showwarning("!","Select a guest first"); return
    gid = safe_int(g_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete guest ID {gid}?"):
        db.guest.delete_one({"guestid": gid}); load_guests()

action_btns(pg, [("Refresh",load_guests,BTN_GRN),("Insert",insert_guest,GREEN),
                  ("Update",update_guest,GOLD),("Delete",delete_guest,DANGER)])
load_guests()

# ══════════════════════════════════════════════════════════════════════════════
# 2. BOOKING
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Booking"]
hdr(pg, "Booking Collection", "Bookings with embedded Assign Room")
b_cols = ["bookingid","check_date","checkout_date","status","staffid","guestid","roomid","assign_date"]
b_tree = make_tree(pg, b_cols, [80,100,110,100,68,68,80,100])

def load_bookings():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    rows = []
    for d in db.booking.find({},{"_id":0}):
        ar = d.get("assigned_room",{}) or {}
        rows.append([d.get("bookingid",""),d.get("check_date",""),d.get("checkout_date",""),
                     d.get("status",""),d.get("staffid",""),d.get("guestid",""),
                     ar.get("roomid",""),ar.get("assign_date","")])
    fill_tree(b_tree, rows)

def insert_booking():
    fields = ["bookingid","check_date","checkout_date","status","staffid","guestid","roomid","assign_date"]
    def submit(e, win):
        doc = {"bookingid": safe_int(e["bookingid"].get()),
               "check_date": e["check_date"].get(), "checkout_date": e["checkout_date"].get(),
               "status": e["status"].get(), "staffid": safe_int(e["staffid"].get()),
               "guestid": safe_int(e["guestid"].get()),
               "assigned_room": {"roomid": safe_int(e["roomid"].get()), "assign_date": e["assign_date"].get()}}
        db.booking.insert_one(doc); load_bookings()
        messagebox.showinfo("Done","Booking inserted!"); win.destroy()
    popup("Insert Booking", fields, submit)

def update_booking():
    sel = b_tree.selection()
    if not sel: messagebox.showwarning("!","Select a booking first"); return
    vals = b_tree.item(sel[0])["values"]
    def submit(e, win):
        db.booking.update_one({"bookingid": safe_int(vals[0])},
            {"$set": {"status": e["status"].get()}})
        load_bookings(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Status", ["status"], submit, {"status": vals[3]})

def delete_booking():
    sel = b_tree.selection()
    if not sel: messagebox.showwarning("!","Select a booking first"); return
    bid = safe_int(b_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete booking ID {bid}?"):
        db.booking.delete_one({"bookingid": bid}); load_bookings()

action_btns(pg, [("Refresh",load_bookings,BTN_GRN),("Insert",insert_booking,GREEN),
                  ("Update",update_booking,GOLD),("Delete",delete_booking,DANGER)])
load_bookings()

# ══════════════════════════════════════════════════════════════════════════════
# 3. INVOICE
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Invoice"]
hdr(pg, "Invoice Collection", "All billing records")
i_cols = ["invoiceid","issue_date","amount_due","payment_mode","paid","bookingid"]
i_tree = make_tree(pg, i_cols, [80,110,110,130,80,90])

def load_invoices():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(i_tree, [[d.get(c,"") for c in i_cols] for d in db.invoice.find({},{"_id":0})])

def insert_invoice():
    def submit(e, win):
        doc = {f: e[f].get() for f in i_cols}
        for k in ["invoiceid","bookingid","paid"]: doc[k] = safe_int(doc[k])
        doc["amount_due"] = safe_float(doc["amount_due"])
        db.invoice.insert_one(doc); load_invoices()
        messagebox.showinfo("Done","Invoice inserted!"); win.destroy()
    popup("Insert Invoice", i_cols, submit)

def update_invoice():
    sel = i_tree.selection()
    if not sel: messagebox.showwarning("!","Select an invoice first"); return
    vals = i_tree.item(sel[0])["values"]
    def submit(e, win):
        db.invoice.update_one({"invoiceid": safe_int(vals[0])},
            {"$set": {"amount_due": safe_float(e["amount_due"].get()),
                      "payment_mode": e["payment_mode"].get()}})
        load_invoices(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Invoice", ["amount_due","payment_mode"], submit,
          {"amount_due": vals[2], "payment_mode": vals[3]})

def delete_invoice():
    sel = i_tree.selection()
    if not sel: messagebox.showwarning("!","Select an invoice first"); return
    iid = safe_int(i_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete invoice ID {iid}?"):
        db.invoice.delete_one({"invoiceid": iid}); load_invoices()

action_btns(pg, [("Refresh",load_invoices,BTN_GRN),("Insert",insert_invoice,GREEN),
                  ("Update",update_invoice,GOLD),("Delete",delete_invoice,DANGER)])
load_invoices()

# ══════════════════════════════════════════════════════════════════════════════
# 4. STAFF
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Staff"]
hdr(pg, "Staff Collection", "All hotel staff members")
s_cols = ["staffid","s_first_name","s_last_name","s_salary"]
s_tree = make_tree(pg, s_cols, [80,155,155,120])

def load_staff():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(s_tree, [[d.get(c,"") for c in s_cols] for d in db.staff.find({},{"_id":0})])

def insert_staff():
    def submit(e, win):
        doc = {f: e[f].get() for f in s_cols}
        doc["staffid"] = safe_int(doc["staffid"]); doc["s_salary"] = safe_int(doc["s_salary"])
        db.staff.insert_one(doc); load_staff()
        messagebox.showinfo("Done","Staff inserted!"); win.destroy()
    popup("Insert Staff", s_cols, submit)

def update_staff():
    sel = s_tree.selection()
    if not sel: messagebox.showwarning("!","Select a staff member first"); return
    vals = s_tree.item(sel[0])["values"]
    def submit(e, win):
        db.staff.update_one({"staffid": safe_int(vals[0])},
            {"$set": {"s_salary": safe_int(e["s_salary"].get())}})
        load_staff(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Salary", ["s_salary"], submit, {"s_salary": vals[3]})

def delete_staff():
    sel = s_tree.selection()
    if not sel: messagebox.showwarning("!","Select a staff member first"); return
    sid = safe_int(s_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete staff ID {sid}?"):
        db.staff.delete_one({"staffid": sid}); load_staff()

action_btns(pg, [("Refresh",load_staff,BTN_GRN),("Insert",insert_staff,GREEN),
                  ("Update",update_staff,GOLD),("Delete",delete_staff,DANGER)])
load_staff()

# ══════════════════════════════════════════════════════════════════════════════
# 5. HOTEL
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Hotel"]
hdr(pg, "Hotel Collection", "All hotel properties")
h_cols = ["hotelid","hotelname","city","country","starrating"]
h_tree = make_tree(pg, h_cols, [70,200,120,110,90])

def load_hotel():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(h_tree, [[d.get(c,"") for c in h_cols] for d in db.hotel.find({},{"_id":0})])

def insert_hotel():
    def submit(e, win):
        doc = {f: e[f].get() for f in h_cols}
        doc["hotelid"] = safe_int(doc["hotelid"]); doc["starrating"] = safe_int(doc["starrating"])
        db.hotel.insert_one(doc); load_hotel()
        messagebox.showinfo("Done","Hotel inserted!"); win.destroy()
    popup("Insert Hotel", h_cols, submit)

def update_hotel():
    sel = h_tree.selection()
    if not sel: messagebox.showwarning("!","Select a hotel first"); return
    vals = h_tree.item(sel[0])["values"]
    def submit(e, win):
        db.hotel.update_one({"hotelid": safe_int(vals[0])},
            {"$set": {f: e[f].get() for f in ["hotelname","city","country","starrating"]}})
        load_hotel(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Hotel", ["hotelname","city","country","starrating"], submit, dict(zip(h_cols,vals)))

def delete_hotel():
    sel = h_tree.selection()
    if not sel: messagebox.showwarning("!","Select a hotel first"); return
    hid = safe_int(h_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete hotel ID {hid}?"):
        db.hotel.delete_one({"hotelid": hid}); load_hotel()

action_btns(pg, [("Refresh",load_hotel,BTN_GRN),("Insert",insert_hotel,GREEN),
                  ("Update",update_hotel,GOLD),("Delete",delete_hotel,DANGER)])
load_hotel()

# ══════════════════════════════════════════════════════════════════════════════
# 6. ROOM
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Room"]
hdr(pg, "Room Collection", "All hotel rooms")
r_cols = ["roomid","roomnum","floor","status","wing","building","pricepernight","hotelid"]
r_tree = make_tree(pg, r_cols, [70,80,60,110,80,100,120,70])

def load_room():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(r_tree, [[d.get(c,"") for c in r_cols] for d in db.room.find({},{"_id":0})])

def insert_room():
    def submit(e, win):
        doc = {f: e[f].get() for f in r_cols}
        for k in ["roomid","floor","hotelid"]: doc[k] = safe_int(doc[k])
        doc["pricepernight"] = safe_float(doc["pricepernight"])
        db.room.insert_one(doc); load_room()
        messagebox.showinfo("Done","Room inserted!"); win.destroy()
    popup("Insert Room", r_cols, submit)

def update_room():
    sel = r_tree.selection()
    if not sel: messagebox.showwarning("!","Select a room first"); return
    vals = r_tree.item(sel[0])["values"]
    def submit(e, win):
        db.room.update_one({"roomid": safe_int(vals[0])},
            {"$set": {"status": e["status"].get(),
                      "pricepernight": safe_float(e["pricepernight"].get())}})
        load_room(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Room", ["status","pricepernight"], submit, dict(zip(r_cols,vals)))

def delete_room():
    sel = r_tree.selection()
    if not sel: messagebox.showwarning("!","Select a room first"); return
    rid = safe_int(r_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete room ID {rid}?"):
        db.room.delete_one({"roomid": rid}); load_room()

action_btns(pg, [("Refresh",load_room,BTN_GRN),("Insert",insert_room,GREEN),
                  ("Update",update_room,GOLD),("Delete",delete_room,DANGER)])
load_room()

# ══════════════════════════════════════════════════════════════════════════════
# 7. AMENITY
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Amenity"]
hdr(pg, "Amenity Collection", "Room amenities")
a_cols = ["amenityid","category","amenityname"]
a_tree = make_tree(pg, a_cols, [90,160,220])

def load_amenity():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(a_tree, [[d.get(c,"") for c in a_cols] for d in db.amneity.find({},{"_id":0})])

def insert_amenity():
    def submit(e, win):
        doc = {f: e[f].get() for f in a_cols}
        doc["amenityid"] = safe_int(doc["amenityid"])
        db.amneity.insert_one(doc); load_amenity()
        messagebox.showinfo("Done","Amenity inserted!"); win.destroy()
    popup("Insert Amenity", a_cols, submit)

def update_amenity():
    sel = a_tree.selection()
    if not sel: messagebox.showwarning("!","Select an amenity first"); return
    vals = a_tree.item(sel[0])["values"]
    def submit(e, win):
        db.amneity.update_one({"amenityid": safe_int(vals[0])},
            {"$set": {"category": e["category"].get(), "amenityname": e["amenityname"].get()}})
        load_amenity(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Amenity", ["category","amenityname"], submit, dict(zip(a_cols,vals)))

def delete_amenity():
    sel = a_tree.selection()
    if not sel: messagebox.showwarning("!","Select an amenity first"); return
    aid = safe_int(a_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete amenity ID {aid}?"):
        db.amneity.delete_one({"amenityid": aid}); load_amenity()

action_btns(pg, [("Refresh",load_amenity,BTN_GRN),("Insert",insert_amenity,GREEN),
                  ("Update",update_amenity,GOLD),("Delete",delete_amenity,DANGER)])
load_amenity()

# ══════════════════════════════════════════════════════════════════════════════
# 8. MEMBER GUEST
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["MemberGuest"]
hdr(pg, "Member Guest Collection", "Loyalty / membership guests")
mg_cols = ["guestid","memberid","member_type"]
mg_tree = make_tree(pg, mg_cols, [80,100,160])

def load_member_guest():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(mg_tree, [[d.get(c,"") for c in mg_cols] for d in db.member_guest.find({},{"_id":0})])

def insert_member_guest():
    def submit(e, win):
        doc = {f: e[f].get() for f in mg_cols}
        doc["guestid"] = safe_int(doc["guestid"]); doc["memberid"] = safe_int(doc["memberid"])
        db.member_guest.insert_one(doc); load_member_guest()
        messagebox.showinfo("Done","Member Guest inserted!"); win.destroy()
    popup("Insert Member Guest", mg_cols, submit)

def update_member_guest():
    sel = mg_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = mg_tree.item(sel[0])["values"]
    def submit(e, win):
        db.member_guest.update_one({"guestid": safe_int(vals[0])},
            {"$set": {"member_type": e["member_type"].get()}})
        load_member_guest(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Member Type", ["member_type"], submit, {"member_type": vals[2]})

def delete_member_guest():
    sel = mg_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    gid = safe_int(mg_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete member guest ID {gid}?"):
        db.member_guest.delete_one({"guestid": gid}); load_member_guest()

action_btns(pg, [("Refresh",load_member_guest,BTN_GRN),("Insert",insert_member_guest,GREEN),
                  ("Update",update_member_guest,GOLD),("Delete",delete_member_guest,DANGER)])
load_member_guest()

# ══════════════════════════════════════════════════════════════════════════════
# 9. WALKING GUEST
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["WalkingGuest"]
hdr(pg, "Walking Guest Collection", "Walk-in and referral guests")
wg_cols = ["guestid","arrival_mode"]
wg_tree = make_tree(pg, wg_cols, [90,200])

def load_walking_guest():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(wg_tree, [[d.get(c,"") for c in wg_cols] for d in db.walking_guest.find({},{"_id":0})])

def insert_walking_guest():
    def submit(e, win):
        doc = {f: e[f].get() for f in wg_cols}
        doc["guestid"] = safe_int(doc["guestid"])
        db.walking_guest.insert_one(doc); load_walking_guest()
        messagebox.showinfo("Done","Walking Guest inserted!"); win.destroy()
    popup("Insert Walking Guest", wg_cols, submit)

def update_walking_guest():
    sel = wg_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = wg_tree.item(sel[0])["values"]
    def submit(e, win):
        db.walking_guest.update_one({"guestid": safe_int(vals[0])},
            {"$set": {"arrival_mode": e["arrival_mode"].get()}})
        load_walking_guest(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Arrival Mode", ["arrival_mode"], submit, {"arrival_mode": vals[1]})

def delete_walking_guest():
    sel = wg_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    gid = safe_int(wg_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete walking guest ID {gid}?"):
        db.walking_guest.delete_one({"guestid": gid}); load_walking_guest()

action_btns(pg, [("Refresh",load_walking_guest,BTN_GRN),("Insert",insert_walking_guest,GREEN),
                  ("Update",update_walking_guest,GOLD),("Delete",delete_walking_guest,DANGER)])
load_walking_guest()

# ══════════════════════════════════════════════════════════════════════════════
# 10. SUIT
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["Suit"]
hdr(pg, "Suit Collection", "Suite rooms with lounge and jacuzzi")
st_cols = ["roomid","lounge","jacuzzi"]
st_tree = make_tree(pg, st_cols, [80,200,120])

def load_suit():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(st_tree, [[d.get(c,"") for c in st_cols] for d in db.suit.find({},{"_id":0})])

def insert_suit():
    def submit(e, win):
        doc = {f: e[f].get() for f in st_cols}
        doc["roomid"] = safe_int(doc["roomid"])
        db.suit.insert_one(doc); load_suit()
        messagebox.showinfo("Done","Suit inserted!"); win.destroy()
    popup("Insert Suit", st_cols, submit)

def update_suit():
    sel = st_tree.selection()
    if not sel: messagebox.showwarning("!","Select a suit first"); return
    vals = st_tree.item(sel[0])["values"]
    def submit(e, win):
        db.suit.update_one({"roomid": safe_int(vals[0])},
            {"$set": {"lounge": e["lounge"].get(), "jacuzzi": e["jacuzzi"].get()}})
        load_suit(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Suit", ["lounge","jacuzzi"], submit, dict(zip(st_cols,vals)))

def delete_suit():
    sel = st_tree.selection()
    if not sel: messagebox.showwarning("!","Select a suit first"); return
    rid = safe_int(st_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete suit room ID {rid}?"):
        db.suit.delete_one({"roomid": rid}); load_suit()

action_btns(pg, [("Refresh",load_suit,BTN_GRN),("Insert",insert_suit,GREEN),
                  ("Update",update_suit,GOLD),("Delete",delete_suit,DANGER)])
load_suit()

# ══════════════════════════════════════════════════════════════════════════════
# 11. HOUSEKEEPING TASK
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["HousekeepingTask"]
hdr(pg, "Housekeeping Task Collection", "Cleaning and maintenance tasks")
ht_cols = ["taskid","task_type","priority","status","roomid","note","scheduleat"]
ht_tree = make_tree(pg, ht_cols, [65,110,90,100,70,170,150])

def load_housekeeping_task():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(ht_tree, [[d.get(c,"") for c in ht_cols] for d in db.housekeeping_task.find({},{"_id":0})])

def insert_housekeeping_task():
    def submit(e, win):
        doc = {f: e[f].get() for f in ht_cols}
        doc["taskid"] = safe_int(doc["taskid"]); doc["roomid"] = safe_int(doc["roomid"])
        db.housekeeping_task.insert_one(doc); load_housekeeping_task()
        messagebox.showinfo("Done","Task inserted!"); win.destroy()
    popup("Insert Housekeeping Task", ht_cols, submit)

def update_housekeeping_task():
    sel = ht_tree.selection()
    if not sel: messagebox.showwarning("!","Select a task first"); return
    vals = ht_tree.item(sel[0])["values"]
    def submit(e, win):
        db.housekeeping_task.update_one({"taskid": safe_int(vals[0])},
            {"$set": {"status": e["status"].get(), "priority": e["priority"].get()}})
        load_housekeeping_task(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Task", ["status","priority"], submit, {"status":vals[3],"priority":vals[2]})

def delete_housekeeping_task():
    sel = ht_tree.selection()
    if not sel: messagebox.showwarning("!","Select a task first"); return
    tid = safe_int(ht_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete task ID {tid}?"):
        db.housekeeping_task.delete_one({"taskid": tid}); load_housekeeping_task()

action_btns(pg, [("Refresh",load_housekeeping_task,BTN_GRN),("Insert",insert_housekeeping_task,GREEN),
                  ("Update",update_housekeeping_task,GOLD),("Delete",delete_housekeeping_task,DANGER)])
load_housekeeping_task()

# ══════════════════════════════════════════════════════════════════════════════
# 12. MAINTENANCE STAFF
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["MaintenanceStaff"]
hdr(pg, "Maintenance Staff Collection", "Specialist maintenance employees")
ms_cols = ["staffid","specialist"]
ms_tree = make_tree(pg, ms_cols, [90,200])

def load_maintenance_staff():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(ms_tree, [[d.get(c,"") for c in ms_cols] for d in db.maintenance_Staff.find({},{"_id":0})])

def insert_maintenance_staff():
    def submit(e, win):
        doc = {f: e[f].get() for f in ms_cols}
        doc["staffid"] = safe_int(doc["staffid"])
        db.maintenance_Staff.insert_one(doc); load_maintenance_staff()
        messagebox.showinfo("Done","Maintenance Staff inserted!"); win.destroy()
    popup("Insert Maintenance Staff", ms_cols, submit)

def update_maintenance_staff():
    sel = ms_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = ms_tree.item(sel[0])["values"]
    def submit(e, win):
        db.maintenance_Staff.update_one({"staffid": safe_int(vals[0])},
            {"$set": {"specialist": e["specialist"].get()}})
        load_maintenance_staff(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Specialist", ["specialist"], submit, {"specialist": vals[1]})

def delete_maintenance_staff():
    sel = ms_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    sid = safe_int(ms_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete maintenance staff ID {sid}?"):
        db.maintenance_Staff.delete_one({"staffid": sid}); load_maintenance_staff()

action_btns(pg, [("Refresh",load_maintenance_staff,BTN_GRN),("Insert",insert_maintenance_staff,GREEN),
                  ("Update",update_maintenance_staff,GOLD),("Delete",delete_maintenance_staff,DANGER)])
load_maintenance_staff()

# ══════════════════════════════════════════════════════════════════════════════
# 13. FRONT DESK STAFF
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["FrontDeskStaff"]
hdr(pg, "Front Desk Staff Collection", "Check-in, checkout, and concierge staff")
fd_cols = ["staffid","desk","shifttime"]
fd_tree = make_tree(pg, fd_cols, [80,140,200])

def load_front_desk_staff():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(fd_tree, [[d.get(c,"") for c in fd_cols] for d in db.front_desk_staff.find({},{"_id":0})])

def insert_front_desk_staff():
    def submit(e, win):
        doc = {f: e[f].get() for f in fd_cols}
        doc["staffid"] = safe_int(doc["staffid"])
        db.front_desk_staff.insert_one(doc); load_front_desk_staff()
        messagebox.showinfo("Done","Front Desk Staff inserted!"); win.destroy()
    popup("Insert Front Desk Staff", fd_cols, submit)

def update_front_desk_staff():
    sel = fd_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = fd_tree.item(sel[0])["values"]
    def submit(e, win):
        db.front_desk_staff.update_one({"staffid": safe_int(vals[0])},
            {"$set": {"desk": e["desk"].get(), "shifttime": e["shifttime"].get()}})
        load_front_desk_staff(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Front Desk", ["desk","shifttime"], submit, dict(zip(fd_cols,vals)))

def delete_front_desk_staff():
    sel = fd_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    sid = safe_int(fd_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete front desk staff ID {sid}?"):
        db.front_desk_staff.delete_one({"staffid": sid}); load_front_desk_staff()

action_btns(pg, [("Refresh",load_front_desk_staff,BTN_GRN),("Insert",insert_front_desk_staff,GREEN),
                  ("Update",update_front_desk_staff,GOLD),("Delete",delete_front_desk_staff,DANGER)])
load_front_desk_staff()

# ══════════════════════════════════════════════════════════════════════════════
# 14. STAFF PROFILE
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["StaffProfile"]
hdr(pg, "Staff Profile Collection", "Login credentials and access levels")
sp_cols = ["userid","username","pasword","accesslevel","staffid"]
sp_tree = make_tree(pg, sp_cols, [70,140,130,120,70])

def load_staff_profile():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(sp_tree, [[d.get(c,"") for c in sp_cols] for d in db.staff_profile.find({},{"_id":0})])

def insert_staff_profile():
    def submit(e, win):
        doc = {f: e[f].get() for f in sp_cols}
        doc["userid"] = safe_int(doc["userid"]); doc["staffid"] = safe_int(doc["staffid"])
        db.staff_profile.insert_one(doc); load_staff_profile()
        messagebox.showinfo("Done","Staff Profile inserted!"); win.destroy()
    popup("Insert Staff Profile", sp_cols, submit)

def update_staff_profile():
    sel = sp_tree.selection()
    if not sel: messagebox.showwarning("!","Select a profile first"); return
    vals = sp_tree.item(sel[0])["values"]
    def submit(e, win):
        db.staff_profile.update_one({"userid": safe_int(vals[0])},
            {"$set": {"accesslevel": e["accesslevel"].get()}})
        load_staff_profile(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Access Level", ["accesslevel"], submit, {"accesslevel": vals[3]})

def delete_staff_profile():
    sel = sp_tree.selection()
    if not sel: messagebox.showwarning("!","Select a profile first"); return
    uid = safe_int(sp_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete staff profile ID {uid}?"):
        db.staff_profile.delete_one({"userid": uid}); load_staff_profile()

action_btns(pg, [("Refresh",load_staff_profile,BTN_GRN),("Insert",insert_staff_profile,GREEN),
                  ("Update",update_staff_profile,GOLD),("Delete",delete_staff_profile,DANGER)])
load_staff_profile()

# ══════════════════════════════════════════════════════════════════════════════
# 15. MAINTAINS ROOM
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["MaintainsRoom"]
hdr(pg, "MaintainsRoom Collection", "Staff-to-room maintenance assignments")
mr_cols = ["roomid","staffid"]
mr_tree = make_tree(pg, mr_cols, [100,100])

def load_maintainsroom():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(mr_tree, [[d.get(c,"") for c in mr_cols] for d in db.maintainsroom.find({},{"_id":0})])

def insert_maintainsroom():
    def submit(e, win):
        doc = {f: safe_int(e[f].get()) for f in mr_cols}
        db.maintainsroom.insert_one(doc); load_maintainsroom()
        messagebox.showinfo("Done","Assignment inserted!"); win.destroy()
    popup("Insert MaintainsRoom", mr_cols, submit)

def delete_maintainsroom():
    sel = mr_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = mr_tree.item(sel[0])["values"]
    rid, sid = safe_int(vals[0]), safe_int(vals[1])
    if messagebox.askyesno("Confirm",f"Delete assignment Room {rid} / Staff {sid}?"):
        db.maintainsroom.delete_one({"roomid": rid, "staffid": sid}); load_maintainsroom()

action_btns(pg, [("Refresh",load_maintainsroom,BTN_GRN),("Insert",insert_maintainsroom,GREEN),
                  ("Delete",delete_maintainsroom,DANGER)])
load_maintainsroom()

# ══════════════════════════════════════════════════════════════════════════════
# 16. HOTEL PHONE
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["HotelPhone"]
hdr(pg, "Hotel Phone Collection", "Phone numbers for each hotel")
hp_cols = ["hotelid","phone"]
hp_tree = make_tree(pg, hp_cols, [90,200])

def load_hotel_phone():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(hp_tree, [[d.get(c,"") for c in hp_cols] for d in db.hotel_phone.find({},{"_id":0})])

def insert_hotel_phone():
    def submit(e, win):
        doc = {f: e[f].get() for f in hp_cols}
        doc["hotelid"] = safe_int(doc["hotelid"])
        db.hotel_phone.insert_one(doc); load_hotel_phone()
        messagebox.showinfo("Done","Hotel Phone inserted!"); win.destroy()
    popup("Insert Hotel Phone", hp_cols, submit)

def update_hotel_phone():
    sel = hp_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = hp_tree.item(sel[0])["values"]
    def submit(e, win):
        db.hotel_phone.update_one({"hotelid": safe_int(vals[0]), "phone": vals[1]},
            {"$set": {"phone": e["phone"].get()}})
        load_hotel_phone(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Phone", ["phone"], submit, {"phone": vals[1]})

def delete_hotel_phone():
    sel = hp_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = hp_tree.item(sel[0])["values"]
    hid, phone = safe_int(vals[0]), vals[1]
    if messagebox.askyesno("Confirm",f"Delete phone {phone} for hotel {hid}?"):
        db.hotel_phone.delete_one({"hotelid": hid, "phone": phone}); load_hotel_phone()

action_btns(pg, [("Refresh",load_hotel_phone,BTN_GRN),("Insert",insert_hotel_phone,GREEN),
                  ("Update",update_hotel_phone,GOLD),("Delete",delete_hotel_phone,DANGER)])
load_hotel_phone()

# ══════════════════════════════════════════════════════════════════════════════
# 17. GUEST PHONE
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["GuestPhone"]
hdr(pg, "Guest Phone Collection", "Phone numbers for each guest")
gp_cols = ["guestid","guest_phone"]
gp_tree = make_tree(pg, gp_cols, [90,200])

def load_guest_phone():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(gp_tree, [[d.get(c,"") for c in gp_cols] for d in db.guest_phone.find({},{"_id":0})])

def insert_guest_phone():
    def submit(e, win):
        doc = {f: e[f].get() for f in gp_cols}
        doc["guestid"] = safe_int(doc["guestid"])
        db.guest_phone.insert_one(doc); load_guest_phone()
        messagebox.showinfo("Done","Guest Phone inserted!"); win.destroy()
    popup("Insert Guest Phone", gp_cols, submit)

def update_guest_phone():
    sel = gp_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = gp_tree.item(sel[0])["values"]
    def submit(e, win):
        db.guest_phone.update_one({"guestid": safe_int(vals[0]), "guest_phone": vals[1]},
            {"$set": {"guest_phone": e["guest_phone"].get()}})
        load_guest_phone(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Phone", ["guest_phone"], submit, {"guest_phone": vals[1]})

def delete_guest_phone():
    sel = gp_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = gp_tree.item(sel[0])["values"]
    gid, phone = safe_int(vals[0]), vals[1]
    if messagebox.askyesno("Confirm",f"Delete phone {phone} for guest {gid}?"):
        db.guest_phone.delete_one({"guestid": gid, "guest_phone": phone}); load_guest_phone()

action_btns(pg, [("Refresh",load_guest_phone,BTN_GRN),("Insert",insert_guest_phone,GREEN),
                  ("Update",update_guest_phone,GOLD),("Delete",delete_guest_phone,DANGER)])
load_guest_phone()

# ══════════════════════════════════════════════════════════════════════════════
# 18. STAFF PHONE
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["StaffPhone"]
hdr(pg, "Staff Phone Collection", "Phone numbers for each staff member")
sph_cols = ["staffid","phone"]
sph_tree = make_tree(pg, sph_cols, [90,200])

def load_staff_phone():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(sph_tree, [[d.get(c,"") for c in sph_cols] for d in db.staff_phone.find({},{"_id":0})])

def insert_staff_phone():
    def submit(e, win):
        doc = {f: e[f].get() for f in sph_cols}
        doc["staffid"] = safe_int(doc["staffid"])
        db.staff_phone.insert_one(doc); load_staff_phone()
        messagebox.showinfo("Done","Staff Phone inserted!"); win.destroy()
    popup("Insert Staff Phone", sph_cols, submit)

def update_staff_phone():
    sel = sph_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = sph_tree.item(sel[0])["values"]
    def submit(e, win):
        db.staff_phone.update_one({"staffid": safe_int(vals[0]), "phone": vals[1]},
            {"$set": {"phone": e["phone"].get()}})
        load_staff_phone(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Phone", ["phone"], submit, {"phone": vals[1]})

def delete_staff_phone():
    sel = sph_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = sph_tree.item(sel[0])["values"]
    sid, phone = safe_int(vals[0]), vals[1]
    if messagebox.askyesno("Confirm",f"Delete phone {phone} for staff {sid}?"):
        db.staff_phone.delete_one({"staffid": sid, "phone": phone}); load_staff_phone()

action_btns(pg, [("Refresh",load_staff_phone,BTN_GRN),("Insert",insert_staff_phone,GREEN),
                  ("Update",update_staff_phone,GOLD),("Delete",delete_staff_phone,DANGER)])
load_staff_phone()

# ══════════════════════════════════════════════════════════════════════════════
# 19. HAS AMENITY
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["HasAmenity"]
hdr(pg, "Has Amenity Collection", "Room-to-amenity assignments")
ha_cols = ["roomid","amenityid"]
ha_tree = make_tree(pg, ha_cols, [100,100])

def load_has_amenity():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(ha_tree, [[d.get(c,"") for c in ha_cols] for d in db.has_amenity.find({},{"_id":0})])

def insert_has_amenity():
    def submit(e, win):
        doc = {f: safe_int(e[f].get()) for f in ha_cols}
        db.has_amenity.insert_one(doc); load_has_amenity()
        messagebox.showinfo("Done","Has Amenity inserted!"); win.destroy()
    popup("Insert Has Amenity", ha_cols, submit)

def delete_has_amenity():
    sel = ha_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = ha_tree.item(sel[0])["values"]
    rid, aid = safe_int(vals[0]), safe_int(vals[1])
    if messagebox.askyesno("Confirm",f"Delete Room {rid} / Amenity {aid}?"):
        db.has_amenity.delete_one({"roomid": rid, "amenityid": aid}); load_has_amenity()

action_btns(pg, [("Refresh",load_has_amenity,BTN_GRN),("Insert",insert_has_amenity,GREEN),
                  ("Delete",delete_has_amenity,DANGER)])
load_has_amenity()

# ══════════════════════════════════════════════════════════════════════════════
# 20. PERFORMS TASK
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["PerformsTask"]
hdr(pg, "Performs Task Collection", "Staff-to-task assignments")
pt_cols = ["taskid","staffid"]
pt_tree = make_tree(pg, pt_cols, [100,100])

def load_performs_task():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(pt_tree, [[d.get(c,"") for c in pt_cols] for d in db.performs_task.find({},{"_id":0})])

def insert_performs_task():
    def submit(e, win):
        doc = {f: safe_int(e[f].get()) for f in pt_cols}
        db.performs_task.insert_one(doc); load_performs_task()
        messagebox.showinfo("Done","Performs Task inserted!"); win.destroy()
    popup("Insert Performs Task", pt_cols, submit)

def delete_performs_task():
    sel = pt_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = pt_tree.item(sel[0])["values"]
    tid, sid = safe_int(vals[0]), safe_int(vals[1])
    if messagebox.askyesno("Confirm",f"Delete Task {tid} / Staff {sid}?"):
        db.performs_task.delete_one({"taskid": tid, "staffid": sid}); load_performs_task()

action_btns(pg, [("Refresh",load_performs_task,BTN_GRN),("Insert",insert_performs_task,GREEN),
                  ("Delete",delete_performs_task,DANGER)])
load_performs_task()

# ══════════════════════════════════════════════════════════════════════════════
# 21. SINGLE ROOM
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["SingleRoom"]
hdr(pg, "Single Room Collection", "Single occupancy rooms")
sr_cols = ["roomid","bedtype","maxguest"]
sr_tree = make_tree(pg, sr_cols, [90,130,100])

def load_single_room():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(sr_tree, [[d.get(c,"") for c in sr_cols] for d in db.single_room.find({},{"_id":0})])

def insert_single_room():
    def submit(e, win):
        doc = {f: e[f].get() for f in sr_cols}
        doc["roomid"] = safe_int(doc["roomid"]); doc["maxguest"] = safe_int(doc["maxguest"])
        db.single_room.insert_one(doc); load_single_room()
        messagebox.showinfo("Done","Single Room inserted!"); win.destroy()
    popup("Insert Single Room", sr_cols, submit)

def update_single_room():
    sel = sr_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = sr_tree.item(sel[0])["values"]
    def submit(e, win):
        db.single_room.update_one({"roomid": safe_int(vals[0])},
            {"$set": {"bedtype": e["bedtype"].get(), "maxguest": safe_int(e["maxguest"].get())}})
        load_single_room(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Single Room", ["bedtype","maxguest"], submit, dict(zip(sr_cols,vals)))

def delete_single_room():
    sel = sr_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    rid = safe_int(sr_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete single room ID {rid}?"):
        db.single_room.delete_one({"roomid": rid}); load_single_room()

action_btns(pg, [("Refresh",load_single_room,BTN_GRN),("Insert",insert_single_room,GREEN),
                  ("Update",update_single_room,GOLD),("Delete",delete_single_room,DANGER)])
load_single_room()

# ══════════════════════════════════════════════════════════════════════════════
# 22. DOUBLE ROOM
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["DoubleRoom"]
hdr(pg, "Double Room Collection", "Double occupancy rooms")
dr_cols = ["roomid","bedcount"]
dr_tree = make_tree(pg, dr_cols, [100,120])

def load_double_room():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(dr_tree, [[d.get(c,"") for c in dr_cols] for d in db.double_room.find({},{"_id":0})])

def insert_double_room():
    def submit(e, win):
        doc = {f: safe_int(e[f].get()) for f in dr_cols}
        db.double_room.insert_one(doc); load_double_room()
        messagebox.showinfo("Done","Double Room inserted!"); win.destroy()
    popup("Insert Double Room", dr_cols, submit)

def update_double_room():
    sel = dr_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = dr_tree.item(sel[0])["values"]
    def submit(e, win):
        db.double_room.update_one({"roomid": safe_int(vals[0])},
            {"$set": {"bedcount": safe_int(e["bedcount"].get())}})
        load_double_room(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Bed Count", ["bedcount"], submit, {"bedcount": vals[1]})

def delete_double_room():
    sel = dr_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    rid = safe_int(dr_tree.item(sel[0])["values"][0])
    if messagebox.askyesno("Confirm",f"Delete double room ID {rid}?"):
        db.double_room.delete_one({"roomid": rid}); load_double_room()

action_btns(pg, [("Refresh",load_double_room,BTN_GRN),("Insert",insert_double_room,GREEN),
                  ("Update",update_double_room,GOLD),("Delete",delete_double_room,DANGER)])
load_double_room()

# ══════════════════════════════════════════════════════════════════════════════
# 23. ROOM STATUS LOG
# ══════════════════════════════════════════════════════════════════════════════
pg = pages["RoomStatusLog"]
hdr(pg, "Room Status Log Collection", "History of room status changes")
rl_cols = ["logid","roomid","status","changedat"]
rl_tree = make_tree(pg, rl_cols, [70,80,120,130])

def load_roomstatuslog():
    if not CONNECTED: messagebox.showerror("Error", ERR); return
    fill_tree(rl_tree, [[d.get(c,"") for c in rl_cols] for d in db.roomstatuslog.find({},{"_id":0})])

def insert_roomstatuslog():
    def submit(e, win):
        doc = {f: e[f].get() for f in rl_cols}
        doc["logid"] = safe_int(doc["logid"]); doc["roomid"] = safe_int(doc["roomid"])
        db.roomstatuslog.insert_one(doc); load_roomstatuslog()
        messagebox.showinfo("Done","Log inserted!"); win.destroy()
    popup("Insert Room Status Log", rl_cols, submit)

def update_roomstatuslog():
    sel = rl_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = rl_tree.item(sel[0])["values"]
    def submit(e, win):
        db.roomstatuslog.update_one({"logid": safe_int(vals[0]), "roomid": safe_int(vals[1])},
            {"$set": {"status": e["status"].get()}})
        load_roomstatuslog(); messagebox.showinfo("Done","Updated!"); win.destroy()
    popup("Update Status", ["status"], submit, {"status": vals[2]})

def delete_roomstatuslog():
    sel = rl_tree.selection()
    if not sel: messagebox.showwarning("!","Select a record first"); return
    vals = rl_tree.item(sel[0])["values"]
    lid, rid = safe_int(vals[0]), safe_int(vals[1])
    if messagebox.askyesno("Confirm",f"Delete log {lid} for room {rid}?"):
        db.roomstatuslog.delete_one({"logid": lid, "roomid": rid}); load_roomstatuslog()

action_btns(pg, [("Refresh",load_roomstatuslog,BTN_GRN),("Insert",insert_roomstatuslog,GREEN),
                  ("Update",update_roomstatuslog,GOLD),("Delete",delete_roomstatuslog,DANGER)])
load_roomstatuslog()

# ── FOOTER ────────────────────────────────────────────────────────────────────
footer = tk.Frame(root, bg=SIDEBAR, height=26)
footer.pack(side="bottom", fill="x")
footer.pack_propagate(False)
tk.Label(footer, text="  COMSATS University Islamabad  |  hotel_management  |  MongoDB localhost:27017",
         font=F_SMALL, bg=SIDEBAR, fg=SUBTEXT).pack(side="left", pady=5)

show_page("Guest")
root.mainloop()
