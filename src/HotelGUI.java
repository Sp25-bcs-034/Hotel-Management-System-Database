import javax.swing.*;
import javax.swing.table.*;
import java.awt.*;
import java.awt.event.*;
import com.mongodb.client.*;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Updates;
import org.bson.Document;

class NavListener implements ActionListener {
    HotelGUI gui;
    public NavListener(HotelGUI gui) { this.gui = gui; }
    public void actionPerformed(ActionEvent e) { gui.showPanel(e.getActionCommand()); }
}

class CrudListener implements ActionListener {
    HotelGUI gui; String col, action;
    public CrudListener(HotelGUI gui, String col, String action) {
        this.gui = gui; this.col = col; this.action = action;
    }
    public void actionPerformed(ActionEvent e) {
        if      (action.equals("refresh")) gui.loadTable(col);
        else if (action.equals("insert"))  gui.insertForm(col);
        else if (action.equals("update"))  gui.updateForm(col);
        else if (action.equals("delete"))  gui.deleteRecord(col);
    }
}

public class HotelGUI {

    static final Color BG      = new Color(26,  60,  52);
    static final Color SIDEBAR = new Color(20,  48,  42);
    static final Color WHITE   = new Color(255, 255, 255);
    static final Color ACCENT  = new Color(64,  145, 108);
    static final Color BTN_GRN = new Color(82,  183, 136);
    static final Color GOLD    = new Color(244, 162,  97);
    static final Color SUBTEXT = new Color(149, 213, 178);
    static final Color DANGER  = new Color(230,  57,  70);
    static final Color GREEN   = new Color(45,  106,  79);

    static final Font F_TITLE = new Font("Arial", Font.BOLD,  18);
    static final Font F_HEAD  = new Font("Arial", Font.BOLD,  13);
    static final Font F_BODY  = new Font("Arial", Font.PLAIN, 12);
    static final Font F_BTN   = new Font("Arial", Font.BOLD,  11);
    static final Font F_SMALL = new Font("Arial", Font.PLAIN,  9);

    MongoClient mongoClient;
    MongoDatabase db;
    boolean connected = false;

    JFrame mainFrame;
    JPanel mainArea;
    CardLayout cardLayout;

    // ── Table models ─────────────────────────────────────────────────────────
    DefaultTableModel guestModel, bookingModel, invoiceModel, staffModel;
    DefaultTableModel hotelModel, roomModel, amenityModel, memberGuestModel;
    DefaultTableModel walkingGuestModel, suitModel, houseTaskModel;
    DefaultTableModel maintStaffModel, frontDeskModel, staffProfileModel, maintainsRoomModel;
    DefaultTableModel hotelPhoneModel, guestPhoneModel, staffPhoneModel;
    DefaultTableModel hasAmenityModel, performsTaskModel;
    DefaultTableModel singleRoomModel, doubleRoomModel, roomStatusLogModel;

    // ── Tables ───────────────────────────────────────────────────────────────
    JTable guestTable, bookingTable, invoiceTable, staffTable;
    JTable hotelTable, roomTable, amenityTable, memberGuestTable;
    JTable walkingGuestTable, suitTable, houseTaskTable;
    JTable maintStaffTable, frontDeskTable, staffProfileTable, maintainsRoomTable;
    JTable hotelPhoneTable, guestPhoneTable, staffPhoneTable;
    JTable hasAmenityTable, performsTaskTable;
    JTable singleRoomTable, doubleRoomTable, roomStatusLogTable;

    JButton[] navBtns;

    String[] pages = {
        "Guest","Booking","Invoice","Staff",
        "Hotel","Room","Amenity","MemberGuest","WalkingGuest","Suit",
        "HouseTask","MaintStaff","FrontDesk","StaffProfile","MaintainsRoom",
        "HotelPhone","GuestPhone","StaffPhone",
        "HasAmenity","PerformsTask",
        "SingleRoom","DoubleRoom","RoomStatusLog"
    };
    String[] navLabels = {
        "  Guest","  Booking","  Invoice","  Staff",
        "  Hotel","  Room","  Amenity","  Member Guest","  Walking Guest","  Suit",
        "  Housekeeping Task","  Maintenance Staff","  Front Desk Staff","  Staff Profile","  Maintains Room",
        "  Hotel Phone","  Guest Phone","  Staff Phone",
        "  Has Amenity","  Performs Task",
        "  Single Room","  Double Room","  Room Status Log"
    };

    public HotelGUI() {
        connectMongo();
        buildUI();
        showPanel("Guest");
    }

    void connectMongo() {
        try {
            mongoClient = MongoClients.create("mongodb://localhost:27017");
            db = mongoClient.getDatabase("hotel_management");
            db.listCollectionNames().first();
            connected = true;
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(null, "MongoDB not connected!\n" + ex.getMessage());
        }
    }

    void buildUI() {
        mainFrame = new JFrame("Hotel Management System");
        mainFrame.setSize(1300, 730);
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        mainFrame.setLayout(new BorderLayout());
        mainFrame.getContentPane().setBackground(BG);
        mainFrame.add(buildHeader(),   BorderLayout.NORTH);
        mainFrame.add(buildSidebar(),  BorderLayout.WEST);
        mainFrame.add(buildMainArea(), BorderLayout.CENTER);
        mainFrame.add(buildFooter(),   BorderLayout.SOUTH);
        mainFrame.setVisible(true);
    }

    JPanel buildHeader() {
        JPanel p = new JPanel(new BorderLayout());
        p.setBackground(SIDEBAR);
        p.setPreferredSize(new Dimension(0, 60));
        p.setBorder(BorderFactory.createEmptyBorder(0, 16, 0, 16));
        JLabel title = new JLabel("  Hotel Management System");
        title.setFont(F_TITLE); title.setForeground(WHITE);
        p.add(title, BorderLayout.WEST);
        JLabel badge = new JLabel(connected ? "●  Connected  " : "●  Offline  ");
        badge.setFont(F_BTN);
        badge.setForeground(connected ? BTN_GRN : DANGER);
        p.add(badge, BorderLayout.EAST);
        return p;
    }

    JPanel buildSidebar() {
        JPanel wrapper = new JPanel(new BorderLayout());
        wrapper.setBackground(SIDEBAR);
        wrapper.setPreferredSize(new Dimension(200, 0));

        JPanel p = new JPanel();
        p.setLayout(new BoxLayout(p, BoxLayout.Y_AXIS));
        p.setBackground(SIDEBAR);

        JLabel lbl = new JLabel("  COLLECTIONS");
        lbl.setFont(F_SMALL); lbl.setForeground(SUBTEXT);
        p.add(Box.createVerticalStrut(18)); p.add(lbl);
        p.add(Box.createVerticalStrut(6));

        navBtns = new JButton[pages.length];
        NavListener nl = new NavListener(this);
        for (int i = 0; i < pages.length; i++) {
            JButton b = makeBtn(navLabels[i], SIDEBAR, SUBTEXT);
            b.setActionCommand(pages[i]);
            b.addActionListener(nl);
            b.setMaximumSize(new Dimension(200, 38));
            b.setHorizontalAlignment(SwingConstants.LEFT);
            p.add(b); p.add(Box.createVerticalStrut(2));
            navBtns[i] = b;
        }
        p.add(Box.createVerticalGlue());
        JLabel dbl = new JLabel("  hotel_management");
        dbl.setFont(F_SMALL); dbl.setForeground(SUBTEXT);
        p.add(dbl); p.add(Box.createVerticalStrut(12));

        JScrollPane scroll = new JScrollPane(p,
            JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
            JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        scroll.setBorder(null);
        scroll.getViewport().setBackground(SIDEBAR);
        wrapper.add(scroll, BorderLayout.CENTER);
        return wrapper;
    }

    JPanel buildMainArea() {
        cardLayout = new CardLayout();
        mainArea   = new JPanel(cardLayout);
        mainArea.setBackground(BG);

        // Column arrays
        String[] gC   = {"guestid","first_name","last_name","email","dob"};
        String[] bC   = {"bookingid","check_date","checkout_date","status","staffid","guestid","roomid","assign_date"};
        String[] iC   = {"invoiceid","issue_date","amount_due","payment_mode","paid","bookingid"};
        String[] sC   = {"staffid","s_first_name","s_last_name","s_salary"};
        String[] hC   = {"hotelid","hotelname","city","country","starrating"};
        String[] rC   = {"roomid","roomnum","floor","status","wing","building","pricepernight","hotelid"};
        String[] aC   = {"amenityid","category","amenityname"};
        String[] mgC  = {"guestid","memberid","member_type"};
        String[] wgC  = {"guestid","arrival_mode"};
        String[] stC  = {"roomid","lounge","jacuzzi"};
        String[] htC  = {"taskid","task_type","priority","status","roomid","note","scheduleat"};
        String[] msC  = {"staffid","specialist"};
        String[] fdC  = {"staffid","desk","shifttime"};
        String[] spC  = {"userid","username","pasword","accesslevel","staffid"};
        String[] mrC  = {"roomid","staffid"};
        String[] hpC  = {"hotelid","phone"};
        String[] gpC  = {"guestid","guest_phone"};
        String[] sphC = {"staffid","phone"};
        String[] haC  = {"roomid","amenityid"};
        String[] ptC  = {"taskid","staffid"};
        String[] srC  = {"roomid","bedtype","maxguest"};
        String[] drC  = {"roomid","bedcount"};
        String[] rlC  = {"logid","roomid","status","changedat"};

        guestModel        = new DefaultTableModel(gC,   0);
        bookingModel      = new DefaultTableModel(bC,   0);
        invoiceModel      = new DefaultTableModel(iC,   0);
        staffModel        = new DefaultTableModel(sC,   0);
        hotelModel        = new DefaultTableModel(hC,   0);
        roomModel         = new DefaultTableModel(rC,   0);
        amenityModel      = new DefaultTableModel(aC,   0);
        memberGuestModel  = new DefaultTableModel(mgC,  0);
        walkingGuestModel = new DefaultTableModel(wgC,  0);
        suitModel         = new DefaultTableModel(stC,  0);
        houseTaskModel    = new DefaultTableModel(htC,  0);
        maintStaffModel   = new DefaultTableModel(msC,  0);
        frontDeskModel    = new DefaultTableModel(fdC,  0);
        staffProfileModel = new DefaultTableModel(spC,  0);
        maintainsRoomModel= new DefaultTableModel(mrC,  0);
        hotelPhoneModel   = new DefaultTableModel(hpC,  0);
        guestPhoneModel   = new DefaultTableModel(gpC,  0);
        staffPhoneModel   = new DefaultTableModel(sphC, 0);
        hasAmenityModel   = new DefaultTableModel(haC,  0);
        performsTaskModel = new DefaultTableModel(ptC,  0);
        singleRoomModel   = new DefaultTableModel(srC,  0);
        doubleRoomModel   = new DefaultTableModel(drC,  0);
        roomStatusLogModel= new DefaultTableModel(rlC,  0);

        guestTable        = makeTable(guestModel);
        bookingTable      = makeTable(bookingModel);
        invoiceTable      = makeTable(invoiceModel);
        staffTable        = makeTable(staffModel);
        hotelTable        = makeTable(hotelModel);
        roomTable         = makeTable(roomModel);
        amenityTable      = makeTable(amenityModel);
        memberGuestTable  = makeTable(memberGuestModel);
        walkingGuestTable = makeTable(walkingGuestModel);
        suitTable         = makeTable(suitModel);
        houseTaskTable    = makeTable(houseTaskModel);
        maintStaffTable   = makeTable(maintStaffModel);
        frontDeskTable    = makeTable(frontDeskModel);
        staffProfileTable = makeTable(staffProfileModel);
        maintainsRoomTable= makeTable(maintainsRoomModel);
        hotelPhoneTable   = makeTable(hotelPhoneModel);
        guestPhoneTable   = makeTable(guestPhoneModel);
        staffPhoneTable   = makeTable(staffPhoneModel);
        hasAmenityTable   = makeTable(hasAmenityModel);
        performsTaskTable = makeTable(performsTaskModel);
        singleRoomTable   = makeTable(singleRoomModel);
        doubleRoomTable   = makeTable(doubleRoomModel);
        roomStatusLogTable= makeTable(roomStatusLogModel);

        mainArea.add(buildPage("Guest Collection",          "Manage all registered guests",           guestTable,         "Guest"),         "Guest");
        mainArea.add(buildPage("Booking Collection",        "Bookings with embedded Assign Room",     bookingTable,       "Booking"),       "Booking");
        mainArea.add(buildPage("Invoice Collection",        "All billing records",                    invoiceTable,       "Invoice"),       "Invoice");
        mainArea.add(buildPage("Staff Collection",          "All hotel staff members",                staffTable,         "Staff"),         "Staff");
        mainArea.add(buildPage("Hotel Collection",          "All hotel properties",                   hotelTable,         "Hotel"),         "Hotel");
        mainArea.add(buildPage("Room Collection",           "All hotel rooms",                        roomTable,          "Room"),          "Room");
        mainArea.add(buildPage("Amenity Collection",        "Room amenities",                         amenityTable,       "Amenity"),       "Amenity");
        mainArea.add(buildPage("Member Guest Collection",   "Loyalty / membership guests",            memberGuestTable,   "MemberGuest"),   "MemberGuest");
        mainArea.add(buildPage("Walking Guest Collection",  "Walk-in and referral guests",            walkingGuestTable,  "WalkingGuest"),  "WalkingGuest");
        mainArea.add(buildPage("Suit Collection",           "Suite rooms with lounge and jacuzzi",    suitTable,          "Suit"),          "Suit");
        mainArea.add(buildPage("Housekeeping Task",         "Cleaning and maintenance tasks",         houseTaskTable,     "HouseTask"),     "HouseTask");
        mainArea.add(buildPage("Maintenance Staff",         "Specialist maintenance employees",       maintStaffTable,    "MaintStaff"),    "MaintStaff");
        mainArea.add(buildPage("Front Desk Staff",          "Check-in, checkout, concierge staff",    frontDeskTable,     "FrontDesk"),     "FrontDesk");
        mainArea.add(buildPage("Staff Profile Collection",  "Login credentials and access levels",    staffProfileTable,  "StaffProfile"),  "StaffProfile");
        mainArea.add(buildPage("MaintainsRoom Collection",  "Staff-to-room maintenance assignments",  maintainsRoomTable, "MaintainsRoom"), "MaintainsRoom");
        mainArea.add(buildPage("Hotel Phone Collection",    "Phone numbers for each hotel",           hotelPhoneTable,    "HotelPhone"),    "HotelPhone");
        mainArea.add(buildPage("Guest Phone Collection",    "Phone numbers for each guest",           guestPhoneTable,    "GuestPhone"),    "GuestPhone");
        mainArea.add(buildPage("Staff Phone Collection",    "Phone numbers for each staff member",    staffPhoneTable,    "StaffPhone"),    "StaffPhone");
        mainArea.add(buildPage("Has Amenity Collection",    "Room-to-amenity assignments",            hasAmenityTable,    "HasAmenity"),    "HasAmenity");
        mainArea.add(buildPage("Performs Task Collection",  "Staff-to-task assignments",              performsTaskTable,  "PerformsTask"),  "PerformsTask");
        mainArea.add(buildPage("Single Room Collection",    "Single occupancy rooms",                 singleRoomTable,    "SingleRoom"),    "SingleRoom");
        mainArea.add(buildPage("Double Room Collection",    "Double occupancy rooms",                 doubleRoomTable,    "DoubleRoom"),    "DoubleRoom");
        mainArea.add(buildPage("Room Status Log",           "History of room status changes",         roomStatusLogTable, "RoomStatusLog"), "RoomStatusLog");
        return mainArea;
    }

    JPanel buildPage(String title, String sub, JTable table, String col) {
        JPanel p = new JPanel(new BorderLayout(0, 8));
        p.setBackground(BG);
        p.setBorder(BorderFactory.createEmptyBorder(12, 14, 8, 14));

        JPanel top = new JPanel(new BorderLayout());
        top.setBackground(BG);
        JPanel titles = new JPanel();
        titles.setLayout(new BoxLayout(titles, BoxLayout.Y_AXIS));
        titles.setBackground(BG);
        JLabel tl = new JLabel(title); tl.setFont(F_HEAD); tl.setForeground(WHITE);
        JLabel sl = new JLabel(sub);   sl.setFont(F_BODY); sl.setForeground(SUBTEXT);
        titles.add(tl); titles.add(sl);
        top.add(titles, BorderLayout.WEST);

        JPanel btnPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT, 6, 0));
        btnPanel.setBackground(BG);

        // Junction/composite-key tables: no update button
        boolean noUpdate = col.equals("MaintainsRoom") || col.equals("HasAmenity") ||
                           col.equals("PerformsTask");

        JButton ref = makeBtn("Refresh", BTN_GRN, WHITE);
        JButton ins = makeBtn("Insert",  GREEN,    WHITE);
        ref.addActionListener(new CrudListener(this, col, "refresh"));
        ins.addActionListener(new CrudListener(this, col, "insert"));
        btnPanel.add(ref); btnPanel.add(ins);

        if (!noUpdate) {
            JButton upd = makeBtn("Update", GOLD, WHITE);
            upd.addActionListener(new CrudListener(this, col, "update"));
            btnPanel.add(upd);
        }
        JButton del = makeBtn("Delete", DANGER, WHITE);
        del.addActionListener(new CrudListener(this, col, "delete"));
        btnPanel.add(del);
        top.add(btnPanel, BorderLayout.EAST);

        JSeparator sep = new JSeparator(); sep.setForeground(ACCENT);
        JPanel topWrap = new JPanel(new BorderLayout(0, 4));
        topWrap.setBackground(BG);
        topWrap.add(top, BorderLayout.NORTH);
        topWrap.add(sep, BorderLayout.SOUTH);

        JPanel card = new JPanel(new BorderLayout());
        card.setBackground(ACCENT);
        card.setBorder(BorderFactory.createLineBorder(ACCENT, 2));
        JScrollPane scroll = new JScrollPane(table);
        scroll.setBorder(null);
        scroll.getViewport().setBackground(WHITE);
        card.add(scroll);

        p.add(topWrap, BorderLayout.NORTH);
        p.add(card,    BorderLayout.CENTER);
        return p;
    }

    JPanel buildFooter() {
        JPanel p = new JPanel(new FlowLayout(FlowLayout.LEFT));
        p.setBackground(SIDEBAR); p.setPreferredSize(new Dimension(0, 26));
        JLabel l = new JLabel("  COMSATS University Islamabad  |  hotel_management  |  MongoDB localhost:27017");
        l.setFont(F_SMALL); l.setForeground(SUBTEXT);
        p.add(l); return p;
    }

    void showPanel(String name) {
        cardLayout.show(mainArea, name);
        for (int i = 0; i < pages.length; i++) {
            boolean active = pages[i].equals(name);
            navBtns[i].setBackground(active ? BTN_GRN : SIDEBAR);
            navBtns[i].setForeground(active ? WHITE : SUBTEXT);
        }
        loadTable(name);
    }

    void loadTable(String col) {
        if (!connected) return;
        switch (col) {
            case "Guest":
                guestModel.setRowCount(0);
                for (Document d : db.getCollection("guest").find())
                    guestModel.addRow(new Object[]{d.get("guestid"),d.get("first_name"),d.get("last_name"),d.get("email"),d.get("dob")});
                break;
            case "Booking":
                bookingModel.setRowCount(0);
                for (Document d : db.getCollection("booking").find()) {
                    Document ar = (Document) d.get("assigned_room");
                    bookingModel.addRow(new Object[]{d.get("bookingid"),d.get("check_date"),d.get("checkout_date"),
                        d.get("status"),d.get("staffid"),d.get("guestid"),
                        ar!=null?ar.get("roomid"):"", ar!=null?ar.get("assign_date"):""});
                } break;
            case "Invoice":
                invoiceModel.setRowCount(0);
                for (Document d : db.getCollection("invoice").find())
                    invoiceModel.addRow(new Object[]{d.get("invoiceid"),d.get("issue_date"),d.get("amount_due"),d.get("payment_mode"),d.get("paid"),d.get("bookingid")});
                break;
            case "Staff":
                staffModel.setRowCount(0);
                for (Document d : db.getCollection("staff").find())
                    staffModel.addRow(new Object[]{d.get("staffid"),d.get("s_first_name"),d.get("s_last_name"),d.get("s_salary")});
                break;
            case "Hotel":
                hotelModel.setRowCount(0);
                for (Document d : db.getCollection("hotel").find())
                    hotelModel.addRow(new Object[]{d.get("hotelid"),d.get("hotelname"),d.get("city"),d.get("country"),d.get("starrating")});
                break;
            case "Room":
                roomModel.setRowCount(0);
                for (Document d : db.getCollection("room").find())
                    roomModel.addRow(new Object[]{d.get("roomid"),d.get("roomnum"),d.get("floor"),d.get("status"),d.get("wing"),d.get("building"),d.get("pricepernight"),d.get("hotelid")});
                break;
            case "Amenity":
                amenityModel.setRowCount(0);
                for (Document d : db.getCollection("amneity").find())
                    amenityModel.addRow(new Object[]{d.get("amenityid"),d.get("category"),d.get("amenityname")});
                break;
            case "MemberGuest":
                memberGuestModel.setRowCount(0);
                for (Document d : db.getCollection("member_guest").find())
                    memberGuestModel.addRow(new Object[]{d.get("guestid"),d.get("memberid"),d.get("member_type")});
                break;
            case "WalkingGuest":
                walkingGuestModel.setRowCount(0);
                for (Document d : db.getCollection("walking_guest").find())
                    walkingGuestModel.addRow(new Object[]{d.get("guestid"),d.get("arrival_mode")});
                break;
            case "Suit":
                suitModel.setRowCount(0);
                for (Document d : db.getCollection("suit").find())
                    suitModel.addRow(new Object[]{d.get("roomid"),d.get("lounge"),d.get("jacuzzi")});
                break;
            case "HouseTask":
                houseTaskModel.setRowCount(0);
                for (Document d : db.getCollection("housekeeping_task").find())
                    houseTaskModel.addRow(new Object[]{d.get("taskid"),d.get("task_type"),d.get("priority"),d.get("status"),d.get("roomid"),d.get("note"),d.get("scheduleat")});
                break;
            case "MaintStaff":
                maintStaffModel.setRowCount(0);
                for (Document d : db.getCollection("maintenance_Staff").find())
                    maintStaffModel.addRow(new Object[]{d.get("staffid"),d.get("specialist")});
                break;
            case "FrontDesk":
                frontDeskModel.setRowCount(0);
                for (Document d : db.getCollection("front_desk_staff").find())
                    frontDeskModel.addRow(new Object[]{d.get("staffid"),d.get("desk"),d.get("shifttime")});
                break;
            case "StaffProfile":
                staffProfileModel.setRowCount(0);
                for (Document d : db.getCollection("staff_profile").find())
                    staffProfileModel.addRow(new Object[]{d.get("userid"),d.get("username"),d.get("pasword"),d.get("accesslevel"),d.get("staffid")});
                break;
            case "MaintainsRoom":
                maintainsRoomModel.setRowCount(0);
                for (Document d : db.getCollection("maintainsroom").find())
                    maintainsRoomModel.addRow(new Object[]{d.get("roomid"),d.get("staffid")});
                break;
            case "HotelPhone":
                hotelPhoneModel.setRowCount(0);
                for (Document d : db.getCollection("hotel_phone").find())
                    hotelPhoneModel.addRow(new Object[]{d.get("hotelid"),d.get("phone")});
                break;
            case "GuestPhone":
                guestPhoneModel.setRowCount(0);
                for (Document d : db.getCollection("guest_phone").find())
                    guestPhoneModel.addRow(new Object[]{d.get("guestid"),d.get("guest_phone")});
                break;
            case "StaffPhone":
                staffPhoneModel.setRowCount(0);
                for (Document d : db.getCollection("staff_phone").find())
                    staffPhoneModel.addRow(new Object[]{d.get("staffid"),d.get("phone")});
                break;
            case "HasAmenity":
                hasAmenityModel.setRowCount(0);
                for (Document d : db.getCollection("has_amenity").find())
                    hasAmenityModel.addRow(new Object[]{d.get("roomid"),d.get("amenityid")});
                break;
            case "PerformsTask":
                performsTaskModel.setRowCount(0);
                for (Document d : db.getCollection("performs_task").find())
                    performsTaskModel.addRow(new Object[]{d.get("taskid"),d.get("staffid")});
                break;
            case "SingleRoom":
                singleRoomModel.setRowCount(0);
                for (Document d : db.getCollection("single_room").find())
                    singleRoomModel.addRow(new Object[]{d.get("roomid"),d.get("bedtype"),d.get("maxguest")});
                break;
            case "DoubleRoom":
                doubleRoomModel.setRowCount(0);
                for (Document d : db.getCollection("double_room").find())
                    doubleRoomModel.addRow(new Object[]{d.get("roomid"),d.get("bedcount")});
                break;
            case "RoomStatusLog":
                roomStatusLogModel.setRowCount(0);
                for (Document d : db.getCollection("roomstatuslog").find())
                    roomStatusLogModel.addRow(new Object[]{d.get("logid"),d.get("roomid"),d.get("status"),d.get("changedat")});
                break;
        }
    }

    void insertForm(String col) {
        String[] fields;
        switch (col) {
            case "Guest":         fields = new String[]{"guestid","first_name","last_name","email","dob"}; break;
            case "Booking":       fields = new String[]{"bookingid","check_date","checkout_date","status","staffid","guestid","roomid","assign_date"}; break;
            case "Invoice":       fields = new String[]{"invoiceid","issue_date","amount_due","payment_mode","paid","bookingid"}; break;
            case "Staff":         fields = new String[]{"staffid","s_first_name","s_last_name","s_salary"}; break;
            case "Hotel":         fields = new String[]{"hotelid","hotelname","city","country","starrating"}; break;
            case "Room":          fields = new String[]{"roomid","roomnum","floor","status","wing","building","pricepernight","hotelid"}; break;
            case "Amenity":       fields = new String[]{"amenityid","category","amenityname"}; break;
            case "MemberGuest":   fields = new String[]{"guestid","memberid","member_type"}; break;
            case "WalkingGuest":  fields = new String[]{"guestid","arrival_mode"}; break;
            case "Suit":          fields = new String[]{"roomid","lounge","jacuzzi"}; break;
            case "HouseTask":     fields = new String[]{"taskid","task_type","priority","status","roomid","note","scheduleat"}; break;
            case "MaintStaff":    fields = new String[]{"staffid","specialist"}; break;
            case "FrontDesk":     fields = new String[]{"staffid","desk","shifttime"}; break;
            case "StaffProfile":  fields = new String[]{"userid","username","pasword","accesslevel","staffid"}; break;
            case "MaintainsRoom": fields = new String[]{"roomid","staffid"}; break;
            case "HotelPhone":    fields = new String[]{"hotelid","phone"}; break;
            case "GuestPhone":    fields = new String[]{"guestid","guest_phone"}; break;
            case "StaffPhone":    fields = new String[]{"staffid","phone"}; break;
            case "HasAmenity":    fields = new String[]{"roomid","amenityid"}; break;
            case "PerformsTask":  fields = new String[]{"taskid","staffid"}; break;
            case "SingleRoom":    fields = new String[]{"roomid","bedtype","maxguest"}; break;
            case "DoubleRoom":    fields = new String[]{"roomid","bedcount"}; break;
            default:              fields = new String[]{"logid","roomid","status","changedat"}; break; // RoomStatusLog
        }

        JFrame f = new JFrame("Insert " + col);
        f.setSize(400, Math.min(80 + fields.length * 54, 560));
        f.getContentPane().setBackground(BG);

        JPanel form = new JPanel(new GridLayout(fields.length + 1, 2, 6, 6));
        form.setBackground(BG);
        form.setBorder(BorderFactory.createEmptyBorder(14, 14, 14, 14));
        JTextField[] entries = new JTextField[fields.length];

        for (int i = 0; i < fields.length; i++) {
            JLabel lbl = new JLabel(fields[i] + ":"); lbl.setFont(F_BTN); lbl.setForeground(WHITE);
            entries[i] = makeField();
            form.add(lbl); form.add(entries[i]);
        }

        JButton ins = makeBtn("Submit", BTN_GRN, WHITE);
        JTextField[] fe = entries; String[] ff = fields;
        ins.addActionListener(ev -> {
            try {
                Document doc = new Document();
                for (int i = 0; i < ff.length; i++) {
                    String v = fe[i].getText().trim();
                    if (ff[i].equals("amount_due") || ff[i].equals("pricepernight")) {
                        try { doc.append(ff[i], Double.parseDouble(v)); } catch(Exception ex){ doc.append(ff[i], v); }
                    } else if (ff[i].contains("id") || ff[i].equals("paid") || ff[i].equals("floor")
                               || ff[i].equals("starrating") || ff[i].equals("maxguest") || ff[i].equals("bedcount")) {
                        try { doc.append(ff[i], Integer.parseInt(v)); } catch(Exception ex){ doc.append(ff[i], v); }
                    } else { doc.append(ff[i], v); }
                }
                if (col.equals("Booking")) {
                    Object rid = doc.get("roomid"); Object ad = doc.get("assign_date");
                    doc.remove("roomid"); doc.remove("assign_date");
                    doc.append("assigned_room", new Document("roomid", rid).append("assign_date", ad));
                }
                db.getCollection(getCollectionName(col)).insertOne(doc);
                loadTable(col);
                JOptionPane.showMessageDialog(f, col + " inserted successfully!");
                f.dispose();
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(f, "Error: " + ex.getMessage());
            }
        });
        form.add(new JLabel()); form.add(ins);

        JScrollPane scroll = new JScrollPane(form,
            JScrollPane.VERTICAL_SCROLLBAR_AS_NEEDED,
            JScrollPane.HORIZONTAL_SCROLLBAR_NEVER);
        scroll.setBorder(null);
        scroll.getViewport().setBackground(BG);
        f.add(scroll);
        f.setVisible(true);
    }

    void updateForm(String col) {
        JTable t = getTable(col);
        if (t == null || t.getSelectedRow() == -1) {
            JOptionPane.showMessageDialog(mainFrame, "Select a row first!"); return;
        }
        int row = t.getSelectedRow();
        String idField, updField; Object id, curVal;

        switch (col) {
            case "Guest":         idField="guestid";   updField="last_name";   id=t.getValueAt(row,0); curVal=t.getValueAt(row,2); break;
            case "Booking":       idField="bookingid";  updField="status";      id=t.getValueAt(row,0); curVal=t.getValueAt(row,3); break;
            case "Invoice":       idField="invoiceid";  updField="amount_due";  id=t.getValueAt(row,0); curVal=t.getValueAt(row,2); break;
            case "Staff":         idField="staffid";    updField="s_salary";    id=t.getValueAt(row,0); curVal=t.getValueAt(row,3); break;
            case "Hotel":         idField="hotelid";    updField="starrating";  id=t.getValueAt(row,0); curVal=t.getValueAt(row,4); break;
            case "Room":          idField="roomid";     updField="status";      id=t.getValueAt(row,0); curVal=t.getValueAt(row,3); break;
            case "Amenity":       idField="amenityid";  updField="amenityname"; id=t.getValueAt(row,0); curVal=t.getValueAt(row,2); break;
            case "MemberGuest":   idField="guestid";    updField="member_type"; id=t.getValueAt(row,0); curVal=t.getValueAt(row,2); break;
            case "WalkingGuest":  idField="guestid";    updField="arrival_mode";id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "Suit":          idField="roomid";     updField="lounge";      id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "HouseTask":     idField="taskid";     updField="status";      id=t.getValueAt(row,0); curVal=t.getValueAt(row,3); break;
            case "MaintStaff":    idField="staffid";    updField="specialist";  id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "FrontDesk":     idField="staffid";    updField="shifttime";   id=t.getValueAt(row,0); curVal=t.getValueAt(row,2); break;
            case "StaffProfile":  idField="userid";     updField="accesslevel"; id=t.getValueAt(row,0); curVal=t.getValueAt(row,3); break;
            case "HotelPhone":    idField="hotelid";    updField="phone";       id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "GuestPhone":    idField="guestid";    updField="guest_phone"; id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "StaffPhone":    idField="staffid";    updField="phone";       id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "SingleRoom":    idField="roomid";     updField="bedtype";     id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "DoubleRoom":    idField="roomid";     updField="bedcount";    id=t.getValueAt(row,0); curVal=t.getValueAt(row,1); break;
            case "RoomStatusLog": idField="logid";      updField="status";      id=t.getValueAt(row,0); curVal=t.getValueAt(row,2); break;
            default: JOptionPane.showMessageDialog(mainFrame, "Update not applicable for " + col); return;
        }

        JFrame f = new JFrame("Update " + col + " — " + updField);
        f.setSize(340, 185); f.getContentPane().setBackground(BG);
        JPanel p = new JPanel(new GridLayout(2, 2, 8, 8));
        p.setBackground(BG); p.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        JLabel lbl = new JLabel(updField + ":"); lbl.setFont(F_BTN); lbl.setForeground(WHITE);
        JTextField entry = makeField(); entry.setText(String.valueOf(curVal));
        JButton upd = makeBtn("Update", GOLD, WHITE);

        final String fIdField = idField, fUpdField = updField;
        final Object fId = id;
        upd.addActionListener(ev -> {
            String raw = entry.getText().trim();
            Object newVal = raw;
            try { newVal = Integer.parseInt(raw); } catch(Exception ignored){}
            try { newVal = Double.parseDouble(raw); } catch(Exception ignored){}
            db.getCollection(getCollectionName(col)).updateOne(
                Filters.eq(fIdField, fId), Updates.set(fUpdField, newVal));
            loadTable(col);
            JOptionPane.showMessageDialog(f, col + " updated!"); f.dispose();
        });
        p.add(lbl); p.add(entry); p.add(new JLabel()); p.add(upd);
        f.add(p); f.setVisible(true);
    }

    void deleteRecord(String col) {
        JTable t = getTable(col);
        if (t == null || t.getSelectedRow() == -1) {
            JOptionPane.showMessageDialog(mainFrame, "Select a row first!"); return;
        }
        int row = t.getSelectedRow();
        int ok = JOptionPane.showConfirmDialog(mainFrame,
            "Delete selected " + col + " record?", "Confirm Delete", JOptionPane.YES_NO_OPTION);
        if (ok != JOptionPane.YES_OPTION) return;

        String colName = getCollectionName(col);
        // Composite-key tables
        switch (col) {
            case "MaintainsRoom":
                db.getCollection(colName).deleteOne(Filters.and(
                    Filters.eq("roomid",  toInt(t.getValueAt(row,0))),
                    Filters.eq("staffid", toInt(t.getValueAt(row,1))))); break;
            case "HasAmenity":
                db.getCollection(colName).deleteOne(Filters.and(
                    Filters.eq("roomid",    toInt(t.getValueAt(row,0))),
                    Filters.eq("amenityid", toInt(t.getValueAt(row,1))))); break;
            case "PerformsTask":
                db.getCollection(colName).deleteOne(Filters.and(
                    Filters.eq("taskid",  toInt(t.getValueAt(row,0))),
                    Filters.eq("staffid", toInt(t.getValueAt(row,1))))); break;
            case "HotelPhone":
                db.getCollection(colName).deleteOne(Filters.and(
                    Filters.eq("hotelid", toInt(t.getValueAt(row,0))),
                    Filters.eq("phone", t.getValueAt(row,1).toString()))); break;
            case "GuestPhone":
                db.getCollection(colName).deleteOne(Filters.and(
                    Filters.eq("guestid", toInt(t.getValueAt(row,0))),
                    Filters.eq("guest_phone", t.getValueAt(row,1).toString()))); break;
            case "StaffPhone":
                db.getCollection(colName).deleteOne(Filters.and(
                    Filters.eq("staffid", toInt(t.getValueAt(row,0))),
                    Filters.eq("phone", t.getValueAt(row,1).toString()))); break;
            case "RoomStatusLog":
                db.getCollection(colName).deleteOne(Filters.and(
                    Filters.eq("logid",  toInt(t.getValueAt(row,0))),
                    Filters.eq("roomid", toInt(t.getValueAt(row,1))))); break;
            default:
                db.getCollection(colName).deleteOne(Filters.eq(getIdField(col), toInt(t.getValueAt(row,0))));
                break;
        }
        loadTable(col);
    }

    // ── Helpers ───────────────────────────────────────────────────────────────
    String getCollectionName(String col) {
        switch (col) {
            case "Guest":         return "guest";
            case "Booking":       return "booking";
            case "Invoice":       return "invoice";
            case "Staff":         return "staff";
            case "Hotel":         return "hotel";
            case "Room":          return "room";
            case "Amenity":       return "amneity";
            case "MemberGuest":   return "member_guest";
            case "WalkingGuest":  return "walking_guest";
            case "Suit":          return "suit";
            case "HouseTask":     return "housekeeping_task";
            case "MaintStaff":    return "maintenance_Staff";
            case "FrontDesk":     return "front_desk_staff";
            case "StaffProfile":  return "staff_profile";
            case "MaintainsRoom": return "maintainsroom";
            case "HotelPhone":    return "hotel_phone";
            case "GuestPhone":    return "guest_phone";
            case "StaffPhone":    return "staff_phone";
            case "HasAmenity":    return "has_amenity";
            case "PerformsTask":  return "performs_task";
            case "SingleRoom":    return "single_room";
            case "DoubleRoom":    return "double_room";
            case "RoomStatusLog": return "roomstatuslog";
            default: return col.toLowerCase();
        }
    }

    String getIdField(String col) {
        switch (col) {
            case "Guest": case "MemberGuest": case "WalkingGuest": case "GuestPhone": return "guestid";
            case "Booking":      return "bookingid";
            case "Invoice":      return "invoiceid";
            case "Staff": case "MaintStaff": case "FrontDesk": case "StaffPhone": return "staffid";
            case "Hotel": case "HotelPhone": return "hotelid";
            case "Room": case "Suit": case "SingleRoom": case "DoubleRoom": return "roomid";
            case "Amenity":      return "amenityid";
            case "HouseTask":    return "taskid";
            case "StaffProfile": return "userid";
            default: return "id";
        }
    }

    Object toInt(Object v) {
        try { return Integer.parseInt(String.valueOf(v)); } catch(Exception e) { return v; }
    }

    JTable getTable(String col) {
        switch (col) {
            case "Guest":         return guestTable;
            case "Booking":       return bookingTable;
            case "Invoice":       return invoiceTable;
            case "Staff":         return staffTable;
            case "Hotel":         return hotelTable;
            case "Room":          return roomTable;
            case "Amenity":       return amenityTable;
            case "MemberGuest":   return memberGuestTable;
            case "WalkingGuest":  return walkingGuestTable;
            case "Suit":          return suitTable;
            case "HouseTask":     return houseTaskTable;
            case "MaintStaff":    return maintStaffTable;
            case "FrontDesk":     return frontDeskTable;
            case "StaffProfile":  return staffProfileTable;
            case "MaintainsRoom": return maintainsRoomTable;
            case "HotelPhone":    return hotelPhoneTable;
            case "GuestPhone":    return guestPhoneTable;
            case "StaffPhone":    return staffPhoneTable;
            case "HasAmenity":    return hasAmenityTable;
            case "PerformsTask":  return performsTaskTable;
            case "SingleRoom":    return singleRoomTable;
            case "DoubleRoom":    return doubleRoomTable;
            case "RoomStatusLog": return roomStatusLogTable;
            default: return null;
        }
    }

    JTable makeTable(DefaultTableModel model) {
        JTable t = new JTable(model);
        t.setBackground(WHITE); t.setForeground(new Color(26, 60, 52));
        t.setFont(F_BODY); t.setRowHeight(26);
        t.setGridColor(new Color(200, 230, 215));
        t.setSelectionBackground(BTN_GRN); t.setSelectionForeground(WHITE);
        t.getTableHeader().setBackground(new Color(26, 60, 52));
        t.getTableHeader().setForeground(WHITE);
        t.getTableHeader().setFont(F_BTN);
        t.setFillsViewportHeight(true);
        t.setAutoResizeMode(JTable.AUTO_RESIZE_ALL_COLUMNS);
        return t;
    }

    JButton makeBtn(String txt, Color bg, Color fg) {
        JButton b = new JButton(txt);
        b.setFont(F_BTN); b.setBackground(bg); b.setForeground(fg);
        b.setFocusPainted(false); b.setBorderPainted(false); b.setOpaque(true);
        b.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        return b;
    }

    JTextField makeField() {
        JTextField f = new JTextField();
        f.setBackground(WHITE); f.setForeground(new Color(26, 60, 52));
        f.setFont(F_BODY); f.setCaretColor(new Color(26, 60, 52));
        f.setBorder(BorderFactory.createLineBorder(BTN_GRN, 1));
        return f;
    }

    public static void main(String[] args) { new HotelGUI(); }
}
