import tkinter as tk
from tkinter import font, Frame, Label, Button, ttk, messagebox,PhotoImage,scrolledtext
import threading
import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import webbrowser


#amer

#switch used for the switch button
def switchMFUE(from_currency_var, to_currency_var):
    # This will affect the actual StringVar objects passed as arguments
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    from_currency_var.set(to_currency)
    to_currency_var.set(from_currency)

# Function to fetch live exchange rates
def fetch_live_exchange_rates(currency_rates, update_currency_options):
    access_key = "8de0701a8cf230f2c892260fa346094e"  # Replace with your actual access key
    url = f"http://api.exchangeratesapi.io/v1/latest?access_key={access_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            currency_rates.update(data['rates'])
            currency_rates["EUR"] = 1  # Manually add EUR since it's the base
            update_currency_options()
        else:
            print(f"Error fetching live exchange rates: {data}")
    except Exception as e:
        print(f"Exception occurred: {e}")

# Function to handle the conversion
def convert(amount_entry, from_currency_var, to_currency_var, currency_rates, result_label):
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()

        if from_currency not in currency_rates or to_currency not in currency_rates:
            result_label.config(text="Currency not available")
            return

        from_rate = currency_rates.get(from_currency, 1)
        to_rate = currency_rates.get(to_currency, 1)

        converted_amount = amount / from_rate * to_rate
        result_label.config(text=f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")
    except ValueError:
        result_label.config(text="Invalid amount")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

# Initialize a list to keep track of pages
pages = []

#use this to keep track of amount of pages
i = 0
# Function to add pages
def add_page(from_currency_var, to_currency_var,page):
    
    # Define currency rates dict
    currency_rates = {}
    
    def update_currency_options():
        currencies = list(currency_rates.keys())
        menu = from_currency_menu["menu"]
        menu.delete(0, "end")
        for currency in currencies:
            menu.add_command(label=currency, command=lambda value=currency: from_currency_var.set(value))
        from_currency_var.set("USD") 
        menu = to_currency_menu["menu"]
        menu.delete(0, "end")
        for currency in currencies:
            menu.add_command(label=currency, command=lambda value=currency: to_currency_var.set(value))
        to_currency_var.set("EUR")

    # Fetch live exchange rates
    fetch_live_exchange_rates(currency_rates, update_currency_options)
    
    mainmenu = page
    # Configure styles using ttk.Style
    style = ttk.Style()
    large_font = ('Helvetica', 18,'bold')  # Larger font size
    result_font = ('Helvetica', 24)  # Even larger font size for the result label
    style.configure('TEntry', font=large_font, relief='groove', borderwidth=3)
    style.configure('TButton', font=large_font, relief='raised', borderwidth=3)
    style.configure('TMenubutton', font=large_font)
    
    global i  # Declare i as global if it's defined outside this function
    
    # Create font styles
    style1 = font.Font(size=55, weight="bold")
    style2 = font.Font(size=20, weight="bold")
    
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()

    title = f" {from_currency} vs {to_currency} "
    title2 = f"Flip {from_currency} & {to_currency}"


    
    # Create a new page
    NewPage = Frame(window, bg='#F4A460')
    NewPage.grid(row=0, column=0, sticky='nsew')

    NewPage.grid_remove()
    
    # Append the new page to the list of pages
    pages.append(NewPage)

    Label(NewPage, text=title,bd=5, relief = 'raised',font=style1,  bg='#F4A460', fg='white').pack(pady=20)
    



    # Custom Exchange Widgets with larger font and padding
    Label(NewPage, text="Amount:", font=large_font, background='white', foreground='#F4A460',bd=5, relief = 'raised').pack(pady=10)
    amount_entry_MFUE1 = ttk.Entry(NewPage, style='TEntry', width=20)  # Larger width for Entry
    amount_entry_MFUE1.pack(pady=10)

    Label(NewPage, text="From:", font=large_font,  background='white', foreground='#F4A460',bd=5, relief = 'raised').pack(pady=10)
    from_currency_var_MFUEpage1 = tk.StringVar()
    from_currency_menu_MFUEpage1 = ttk.OptionMenu(NewPage, from_currency_var_MFUEpage1, '', style='TMenubutton')
    from_currency_menu_MFUEpage1.pack(pady=10)

    Label(NewPage, text="To:", font=large_font,  background='white', foreground='#F4A460',bd=5, relief = 'raised').pack(pady=10)
    to_currency_var_MFUEpage1 = tk.StringVar()
    to_currency_menu_MFUEpage1 = ttk.OptionMenu(NewPage, to_currency_var_MFUEpage1, '', style='TMenubutton')
    to_currency_menu_MFUEpage1.pack(pady=10)
        
    from_currency_var_MFUEpage1.set(from_currency)
    to_currency_var_MFUEpage1.set(to_currency)

    result_label_MFUE1 = ttk.Label(NewPage, text="", font=result_font, background='#F4A460', foreground='white')
    result_label_MFUE1.pack(pady=20)

    from_currency_var_MFUEpage1.set(from_currency)
    to_currency_var_MFUEpage1.set(to_currency)


    convert_button_MFUE1 = Button(NewPage, text="Convert",bd=5, relief = 'raised',bg='#F4A460', fg='white',font=large_font, command=lambda: threading.Thread(target=lambda: convert(amount_entry_MFUE1, from_currency_var_MFUEpage1, to_currency_var_MFUEpage1, currency_rates, result_label_MFUE1)).start())
    convert_button_MFUE1.pack()

    Button(NewPage, text=title2,bd=5, relief = 'raised',bg='white', fg='#F4A460',command=lambda: switchMFUE(from_currency_var_MFUEpage1,to_currency_var_MFUEpage1),font = large_font).pack(pady=20)

    # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE1 = ttk.Button(NewPage, text="Back", command=lambda: mainmenu.tkraise())
    back_button_MFUE1.pack(side='bottom', fill='x', pady=20)

    # Increment i for the next page
    i += 1
        
def setup_navigation_buttons():
    """Sets up navigation buttons on each page."""
    global pages  # Assuming 'pages' is a global list of Frame widgets
    style2 = font.Font(size=20, weight="bold")
    light_brown_hex = "#ffffe0"  # Hexadecimal color code for light brown

    for i, page in enumerate(pages):
        # Clear previous navigation frame if exists
        for widget in page.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        # Create a new frame for navigation buttons on this page
        navigation_frame = tk.Frame(page, bg='#F4A460')
        navigation_frame.pack(pady=5, fill='x', expand=True)

        # Add Previous Button if not the first page
        if i > 0:
            prev_btn = Button(navigation_frame, text="Previous Page",bd=5, relief = 'raised',font=style2, bg='#c3834c', fg='white',
                                 command=lambda i=i: pages[i-1].tkraise())
            prev_btn.pack(side='left', padx=0)

        # Add Next Button if not the last page
        if i < len(pages) - 1:
            next_btn = Button(navigation_frame, text="Next Page",bd=5, relief = 'raised', font=style2, bg='#c3834c', fg='white',
                                 command=lambda i=i: pages[i+1].tkraise())
            next_btn.pack(side='right', padx=0)

def show_page(page_index=0):
    """Shows a specific page and ensures that all pages are properly set in the grid."""
    global pages  # Assuming 'pages' is a global list of Frame widgets

    if not pages:
        messagebox.showinfo("No Saved Pages", "You have not added any pages yet.")

    # Ensure every page is properly gridded (might not be necessary if already done during page creation)
    for page in pages:
        page.grid(row=0, column=0, sticky="nsew")

    # Make sure navigation buttons are set up (this can be moved outside if only needed once)
    setup_navigation_buttons()

    # Raise the requested page to the front
    if 0 <= page_index < len(pages):
        pages[page_index].tkraise()


def fetch_historical_rates(start_date, end_date, base_currency, symbols):
    access_key = "8de0701a8cf230f2c892260fa346094e"
    url = f"http://api.exchangeratesapi.io/v1/timeseries?access_key={access_key}&start_date={start_date}&end_date={end_date}&base={base_currency}&symbols={symbols}"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data['rates']
        else:
            print(f"Error fetching historical rates: {data}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

def plot_exchange_rate_trends(page, historical_data, currency, to_this):
    dates = sorted(historical_data.keys())
    rates = [historical_data[date][currency] for date in dates]
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    
    fig, ax = plt.subplots(figsize=(12, 6))  # Increased figure size
    ax.plot(dates, rates, marker='o')
    
    # Format the dates and set locators for ticks
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Set major ticks to months
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Format major ticks as 'Year-Month'
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())  # Set minor ticks to weeks
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')  # Rotate labels for better readability
    plt.title(f"Exchange Rate Trend for {currency} (Base: {to_this})")
    plt.xlabel("Date")
    plt.ylabel("Exchange Rate")
    plt.grid(True)
    plt.tight_layout()
    
    # To display the plot in a Tkinter window instead of a new popup, you would need to use FigureCanvasTkAgg as shown in previous examples.
    plt.show()

def show_graphs(page, from_currency_var, to_currency_var):
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    # Ensure to pass 'from_currency' and 'to_currency' correctly to the API call
    historical_data = fetch_historical_rates(start_date, end_date, from_currency, to_currency)
    
    if historical_data:
        # Correctly call 'plot_exchange_rate_trends' with appropriate parameters
        plot_exchange_rate_trends(page, historical_data, to_currency, from_currency)



#this is my main window im operating out from
window = tk.Tk()
def main():
    window.title("Currency Converter")

    # Set the window to full screen
    window.attributes('-fullscreen', True)

    # Configure the window's grid to allow the frame to expand
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # Create font styles
    style1 = font.Font(size=55, weight="bold")
    style2 = font.Font(size=20, weight="bold")
    style3 = font.Font(size=30, weight="bold")


    # Creating Frames for each page with background color
    page1 = Frame(window, bg='light blue')
    page2 = Frame(window, bg='light blue')
    page3 = Frame(window, bg='light yellow')
    page4 = Frame(window, bg='#556B2F')
    page5 = Frame(window, bg='brown')


    nice_red = '#E57373'


    #pages for the most frequently used
    MFUEpage1 = Frame(window, bg=nice_red)
    MFUEpage2 = Frame(window, bg=nice_red)
    MFUEpage3 = Frame(window, bg=nice_red)
    MFUEpage4 = Frame(window, bg=nice_red)

    brown_background = '#A52A2A'  # A shade of brown


    #page for adding most frequently used
    background_color1 = "#D2B48C"  # Light brown background for the page

    Apage1 = Frame(window, bg=background_color1)
    BasePage = Frame(window, bg='#EAD9BD')



    # Configure styles using ttk.Style
    style = ttk.Style()
    large_font = ('Helvetica', 18, 'bold')  # Larger and bold font size
    result_font = ('Helvetica', 24)  # Even larger font size for the result label
    style.configure('TLabel', font=large_font, background='light grey', foreground='black')
    style.configure('TEntry', font=large_font, relief='groove', borderwidth=3)
    style.configure('TButton', font=large_font, relief='raised', borderwidth=3)
    style.configure('TMenubutton', font=large_font)

    style.configure('TLabel', font=large_font, background='light grey', foreground='black')

    

    # Grid all pages
    for page in (page1, page2, page3, page4, MFUEpage1,MFUEpage2,MFUEpage3,MFUEpage4,Apage1,BasePage,page5):
        page.grid(row=0, column=0, sticky='nsew')





############################################################################################################################################################
    # Page 1: Home Page
    Label(page1, text=" Welcome To Currency Converter ", font=style1, bg='light blue', fg='#4f9cb5',bd=5, relief = 'raised').pack(pady=40)

    #logo under the start button on page 1
    CurrencyConverterLogo_img = tk.PhotoImage(file="MainLogo.png")
    img_label = Label(page1, image=CurrencyConverterLogo_img, bg='light blue')
    img_label.image = CurrencyConverterLogo_img  # Keep a reference
    img_label.pack(pady=5)
    Label(page1, text=" By Amer Kadric & Devin Barr ", font=style3, bg='light blue', fg='#4f9cb5',bd=5, relief = 'raised').pack(side="bottom")

    Button(page1, text="Start", command=lambda: page2.tkraise(), font=style2, bg='#4f9cb5', fg='white',bd=15, relief = 'raised').pack(pady=100)

    # Custom button style
    button_style = ttk.Style()
    button_style.configure('W.TButton', font=style2, background='dark blue', foreground='#4f9cb5')
############################################################################################################################################################







############################################################################################################################################################
    # Main Menu Label
    Label(page2, text=" Main Menu ", font=style1, bg='light blue', fg='#4f9cb5',bd=5, relief = 'raised').pack(pady=40)

    # Logo
    CurrencyConverterLogo2_img = PhotoImage(file="MainLogo.png")
    img_label = Label(page2, image=CurrencyConverterLogo2_img, bg='light blue')
    img_label.image = CurrencyConverterLogo2_img  # Keep a reference
    img_label.pack(pady=5)

    # Button Frame
    button_frame = ttk.Frame(page2, relief='raised', borderwidth=1)
    button_frame.pack(pady=20)

    # Define button function to raise a frame
    def raise_frame(frame):
        frame.tkraise()
        

    # Buttons
    buttons = [
        ("Quick Convert", lambda: raise_frame(page4)),
        ("Most Common Exchanges", lambda: raise_frame(MFUEpage1)),
        ("Establish Your Dashboard", lambda: raise_frame(Apage1)),
        ("Currency Trends", lambda: raise_frame(page3)),
        ("Current Currency Events", lambda: raise_frame(page5)),
        ("Exit", lambda: window.destroy()),
    ]

    for (text, command) in buttons:
        ttk.Button(button_frame, text=text, style='W.TButton', command=command, width=30).pack(fill='x', pady=5, padx=10)


        # Define currency rates dict
        currency_rates = {}
############################################################################################################################################################







############################################################################################################################################################
    #page for usd to euro
    Label(MFUEpage1, text=" USD vs EUR ", font=style1,  bg=nice_red, fg='white',bd=5, relief = 'raised').pack(pady=20)
    
    # Custom Exchange Widgets with larger font and padding
    Label(MFUEpage1, text="Amount:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    amount_entry_MFUE1 = ttk.Entry(MFUEpage1, style='TEntry', width=20)  # Larger width for Entry
    amount_entry_MFUE1.pack(pady=10)

    Label(MFUEpage1, text="From:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    from_currency_var_MFUEpage1 = tk.StringVar()
    from_currency_menu_MFUEpage1 = ttk.OptionMenu(MFUEpage1, from_currency_var_MFUEpage1, '', style='TMenubutton')
    from_currency_menu_MFUEpage1.pack(pady=10)

    Label(MFUEpage1, text="To:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    to_currency_var_MFUEpage1 = tk.StringVar()
    to_currency_menu_MFUEpage1 = ttk.OptionMenu(MFUEpage1, to_currency_var_MFUEpage1, '', style='TMenubutton')
    to_currency_menu_MFUEpage1.pack(pady=10)
        
    from_currency_var_MFUEpage1.set("USD")
    to_currency_var_MFUEpage1.set("EUR")

    result_label_MFUE1 = ttk.Label(MFUEpage1, text="", font=result_font, background=nice_red, foreground='white')
    result_label_MFUE1.pack(pady=20)

    from_currency_var_MFUEpage1.set("USD")
    to_currency_var_MFUEpage1.set("EUR")


    convert_button_MFUE1 = Button(MFUEpage1, text="Convert", font=style2,bd=10, relief = 'raised',bg=nice_red, fg='white', command=lambda: threading.Thread(target=lambda: convert(amount_entry_MFUE1, from_currency_var_MFUEpage1, to_currency_var_MFUEpage1, currency_rates, result_label_MFUE1)).start())
    convert_button_MFUE1.pack()

    Button(MFUEpage1, text="Flip USD & EURO",bd=5, relief = 'raised',background='white', foreground=nice_red,command=lambda: switchMFUE(from_currency_var_MFUEpage1,to_currency_var_MFUEpage1), font=large_font).pack(pady=20)


    # Create a new frame for navigation buttons on this page
    navigation_frame = tk.Frame(MFUEpage1, bg=nice_red)
    navigation_frame.pack(pady=1, fill='x', expand=True)
    
    
    # Add Next Button if not the last page
    next_btn = Button(navigation_frame, text="Next Page",bd=5, relief = 'raised', font=style2, bg='#D53F3F', fg='white',
                         command=lambda: MFUEpage2.tkraise())
    next_btn.pack(side='right', padx=0)

    # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE1 = ttk.Button(MFUEpage1, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button_MFUE1.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################







############################################################################################################################################################
    #page for yin to cad
    Label(MFUEpage2, text=" CNY vs CAD ", font=style1,  bg=nice_red, fg='white',bd=5, relief = 'raised',).pack(pady=20)
    
    # Custom Exchange Widgets with larger font and padding
    Label(MFUEpage2, text="Amount:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    amount_entry_MFUE2 = ttk.Entry(MFUEpage2, style='TEntry', width=20)  # Larger width for Entry
    amount_entry_MFUE2.pack(pady=10)

    Label(MFUEpage2, text="From:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    from_currency_var_MFUEpage2 = tk.StringVar()
    from_currency_menu_MFUEpage2 = ttk.OptionMenu(MFUEpage2, from_currency_var_MFUEpage2, '', style='TMenubutton')
    from_currency_menu_MFUEpage2.pack(pady=10)

    Label(MFUEpage2, text="To:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    to_currency_var_MFUEpage2 = tk.StringVar()
    to_currency_menu_MFUEpage2 = ttk.OptionMenu(MFUEpage2, to_currency_var_MFUEpage2, '', style='TMenubutton')
    to_currency_menu_MFUEpage2.pack(pady=10)
        
    from_currency_var_MFUEpage2.set("CNY")
    to_currency_var_MFUEpage2.set("CAD")

    result_label_MFUE2 = ttk.Label(MFUEpage2, text="", font=result_font, background=nice_red, foreground='white')
    result_label_MFUE2.pack(pady=20)

    from_currency_var_MFUEpage2.set("CNY")
    to_currency_var_MFUEpage2.set("CAD")


    convert_button_MFUE2 = Button(MFUEpage2, text="Convert",bd=10, relief = 'raised',  bg=nice_red, fg='white',font=style2, command=lambda: threading.Thread(target=lambda: convert(amount_entry_MFUE2, from_currency_var_MFUEpage2, to_currency_var_MFUEpage2, currency_rates, result_label_MFUE2)).start())
    convert_button_MFUE2.pack()

    Button(MFUEpage2, text="Flip CNY & CAD",bd=5, relief = 'raised',background='white', foreground=nice_red,command=lambda: switchMFUE(from_currency_var_MFUEpage2,to_currency_var_MFUEpage2), font=large_font).pack(pady=20)


    # Create a new frame for navigation buttons on this page
    navigation_frame = tk.Frame(MFUEpage2, bg=nice_red)
    navigation_frame.pack(pady=1, fill='x', expand=True)
    
    # Add Previous Button if not the first page
    rev_btn = Button(navigation_frame, text="Previous Page",bd=5, relief = 'raised',font=style2, bg='#D53F3F', fg='white',
                        command=lambda: MFUEpage1.tkraise())
    rev_btn.pack(side='left', padx=0)
    
    # Add Next Button if not the last page
    next_btn = Button(navigation_frame, text="Next Page",bd=5, relief = 'raised', font=style2, bg='#D53F3F', fg='white',
                         command=lambda: MFUEpage3.tkraise())
    next_btn.pack(side='right', padx=0)



    # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE2 = ttk.Button(MFUEpage2, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button_MFUE2.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################







############################################################################################################################################################
    #page for peso to rupee
    Label(MFUEpage3, text=" MXN vs INR ", font=style1,  bg=nice_red, fg='white',bd=5, relief = 'raised',).pack(pady=20)
    
    # Custom Exchange Widgets with larger font and padding
    Label(MFUEpage3, text="Amount:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    amount_entry_MFUE3 = ttk.Entry(MFUEpage3, style='TEntry', width=20)  # Larger width for Entry
    amount_entry_MFUE3.pack(pady=10)

    Label(MFUEpage3, text="From:", font=large_font, background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    from_currency_var_MFUEpage3 = tk.StringVar()
    from_currency_menu_MFUEpage3 = ttk.OptionMenu(MFUEpage3, from_currency_var_MFUEpage3, '', style='TMenubutton')
    from_currency_menu_MFUEpage3.pack(pady=10)

    Label(MFUEpage3, text="To:", font=large_font,  background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    to_currency_var_MFUEpage3 = tk.StringVar()
    to_currency_menu_MFUEpage3 = ttk.OptionMenu(MFUEpage3, to_currency_var_MFUEpage3, '', style='TMenubutton')
    to_currency_menu_MFUEpage3.pack(pady=10)
        
    from_currency_var_MFUEpage3.set("MXN")
    to_currency_var_MFUEpage3.set("INR")

    result_label_MFUE3 = ttk.Label(MFUEpage3, text="", font=result_font, background=nice_red, foreground='white')
    result_label_MFUE3.pack(pady=20)

    from_currency_var_MFUEpage3.set("MXN")
    to_currency_var_MFUEpage3.set("INR")


    convert_button_MFUE3 = Button(MFUEpage3, text="Convert",bd=10, bg=nice_red, fg='white',relief = 'raised',font=style2, command=lambda: threading.Thread(target=lambda: convert(amount_entry_MFUE3, from_currency_var_MFUEpage3, to_currency_var_MFUEpage3, currency_rates, result_label_MFUE3)).start())
    convert_button_MFUE3.pack()

    Button(MFUEpage3, text="Flip MXN & INR",bd=5, background='white', foreground=nice_red, relief = 'raised',command=lambda: switchMFUE(from_currency_var_MFUEpage3,to_currency_var_MFUEpage3), font=large_font).pack(pady=20)


    # Create a new frame for navigation buttons on this page
    navigation_frame = tk.Frame(MFUEpage3, bg=nice_red)
    navigation_frame.pack(pady=1, fill='x', expand=True)
    
    # Add Previous Button if not the first page
    rev_btn = Button(navigation_frame, text="Previous Page",bd=5, relief = 'raised',font=style2, bg='#D53F3F', fg='white',
                        command=lambda: MFUEpage2.tkraise())
    rev_btn.pack(side='left', padx=0)
    
    # Add Next Button if not the last page
    next_btn = Button(navigation_frame, text="Next Page",bd=5, relief = 'raised', font=style2, bg='#D53F3F', fg='white',
                         command=lambda: MFUEpage4.tkraise())
    next_btn.pack(side='right', padx=0)


    # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE3 = ttk.Button(MFUEpage3, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button_MFUE3.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################ 
    
    





    
    
 ############################################################################################################################################################
    #page for riyad to british pound
    Label(MFUEpage4, text=" SAR vs GBP ", font=style1,  bg=nice_red, fg='white',bd=5, relief = 'raised',).pack(pady=20)
    
    # Custom Exchange Widgets with larger font and padding
    Label(MFUEpage4, text="Amount:", font=large_font,  background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    amount_entry_MFUE4 = ttk.Entry(MFUEpage4, style='TEntry', width=20)  # Larger width for Entry
    amount_entry_MFUE4.pack(pady=10)

    Label(MFUEpage4, text="From:", font=large_font,  background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    from_currency_var_MFUEpage4 = tk.StringVar()
    from_currency_menu_MFUEpage4 = ttk.OptionMenu(MFUEpage4, from_currency_var_MFUEpage4, '', style='TMenubutton')
    from_currency_menu_MFUEpage4.pack(pady=10)

    Label(MFUEpage4, text="To:", font=large_font,  background='white', foreground=nice_red,bd=5, relief = 'raised').pack(pady=10)
    to_currency_var_MFUEpage4 = tk.StringVar()
    to_currency_menu_MFUEpage4 = ttk.OptionMenu(MFUEpage4, to_currency_var_MFUEpage4, '', style='TMenubutton')
    to_currency_menu_MFUEpage4.pack(pady=10)
        
    from_currency_var_MFUEpage4.set("SAR")
    to_currency_var_MFUEpage4.set("GBP")

    result_label_MFUE4 = ttk.Label(MFUEpage4, text="", font=result_font, background=nice_red, foreground='white')
    result_label_MFUE4.pack(pady=20)

    from_currency_var_MFUEpage4.set("SAR")
    to_currency_var_MFUEpage4.set("GBP")


    convert_button_MFUE4 = Button(MFUEpage4, text="Convert",bd=10, bg=nice_red, fg='white',relief = 'raised', font=style2, command=lambda: threading.Thread(target=lambda: convert(amount_entry_MFUE4, from_currency_var_MFUEpage4, to_currency_var_MFUEpage4, currency_rates, result_label_MFUE4)).start())
    convert_button_MFUE4.pack()

    Button(MFUEpage4, text="Flip SAR & GBP",bd=5, relief = 'raised',  background='white', foreground=nice_red,command=lambda: switchMFUE(from_currency_var_MFUEpage4,to_currency_var_MFUEpage4), font=large_font).pack(pady=20)


    # Create a new frame for navigation buttons on this page
    navigation_frame = tk.Frame(MFUEpage4, bg=nice_red)
    navigation_frame.pack(pady=1, fill='x', expand=True)


    # Add the Previous Currency button
    prev_btn = Button(navigation_frame, text="Previous Page",bd=5, relief = 'raised',font=style2, bg='#D53F3F', fg='white',
                                 command=lambda: MFUEpage3.tkraise())
    prev_btn.pack(side='left', padx=0)

    

    # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE4 = ttk.Button(MFUEpage4, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button_MFUE4.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################








############################################################################################################################################################
    # Page 3: Graph Page
    Label(page3, text=" Graph For Selected Currency ", font=style1, bg='light yellow', fg='dark orange',bd=5, relief = 'raised').pack(pady=20)
    
    Label(page3, text="Base:", font=large_font, background='dark orange', foreground='light yellow',bd=5, relief = 'raised').pack(pady=10)
    from_currency_var2 = tk.StringVar()
    from_currency_menu2 = ttk.OptionMenu(page3, from_currency_var2, '', style='TMenubutton')
    from_currency_menu2.pack(pady=10)

    Label(page3, text="Exchange Rate Trend For:", font=large_font, background='dark orange', foreground='light yellow',bd=5, relief = 'raised').pack(pady=10)
    to_currency_var2 = tk.StringVar()
    to_currency_menu2 = ttk.OptionMenu(page3, to_currency_var2, '', style='TMenubutton')
    to_currency_menu2.pack(pady=10)

    def update_currency_options2():
            currencies = list(currency_rates.keys())
            menu2 = from_currency_menu2["menu"]
            menu2.delete(0, "end")
            for currency in currencies:
                menu2.add_command(label=currency, command=lambda value=currency: from_currency_var2.set(value))
            from_currency_var2.set("USD")

            menu2 = to_currency_menu2["menu"]
            menu2.delete(0, "end")
            for currency in currencies:
                menu2.add_command(label=currency, command=lambda value=currency: to_currency_var2.set(value))
            to_currency_var2.set("EUR")

    # Fetch live exchange rates
    fetch_live_exchange_rates(currency_rates, update_currency_options2)

    load_graphs_btn = tk.Button(page3, text="Load Graph",bd=5, relief = 'raised', command=lambda: show_graphs(page3,from_currency_var2,to_currency_var2), font=style2,  bg='light yellow', fg='dark orange')
    load_graphs_btn.pack(pady=10)

  # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE1 = ttk.Button(page3, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button_MFUE1.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################






############################################################################################################################################################
    page_background = '#556B2F'  # Forest green
    button_background = '#5D761C'  # Olive green
    button_foreground = 'white'
    entry_background = 'white'
    # Page 4: Custom Exchange
    Label(page4, text=" Custom Exchange ", font=style1, background=button_background, foreground=button_foreground,bd=5, relief = 'raised').pack(pady=20)
    
    def update_currency_options():
                currencies = list(currency_rates.keys())
                menu = from_currency_menu["menu"]
                menu.delete(0, "end")
                for currency in currencies:
                    menu.add_command(label=currency, command=lambda value=currency: from_currency_var.set(value))
                from_currency_var.set("USD")

                menu = to_currency_menu["menu"]
                menu.delete(0, "end")
                for currency in currencies:
                    menu.add_command(label=currency, command=lambda value=currency: to_currency_var.set(value))
                to_currency_var.set("EUR")
   
    # Custom Exchange Widgets with larger font and padding
    Label(page4, text="Amount:", font=large_font, background=button_foreground, foreground=button_background,bd=5, relief = 'raised').pack(pady=10)
    amount_entry = ttk.Entry(page4, style='TEntry', width=20)  # Larger width for Entry
    amount_entry.pack(pady=10)

    Label(page4, text="From:", font=large_font, background=button_foreground, foreground=button_background,bd=5, relief = 'raised').pack(pady=10)
    from_currency_var = tk.StringVar()
    from_currency_menu = ttk.OptionMenu(page4, from_currency_var, '', style='TMenubutton')
    from_currency_menu.pack(pady=10)

    Label(page4, text="To:", font=large_font, background=button_foreground, foreground=button_background,bd=5, relief = 'raised').pack(pady=10)
    to_currency_var = tk.StringVar()
    to_currency_menu = ttk.OptionMenu(page4, to_currency_var, '', style='TMenubutton')
    to_currency_menu.pack(pady=10)

    

    # Fetch live exchange rates
    fetch_live_exchange_rates(currency_rates, update_currency_options)

    result_label = ttk.Label(page4, text="", font=result_font, background=page_background, foreground=entry_background)
    result_label.pack(pady=20)

    convert_button = Button(page4, text="Convert",bd=10, background=button_background, foreground=button_foreground, relief = 'raised',  font=style2,command=lambda: threading.Thread(target=lambda: convert(amount_entry, from_currency_var, to_currency_var, currency_rates, result_label)).start())
    convert_button.pack()

    # Ensure that this button is packed last to appear at the bottom
    back_button = ttk.Button(page4, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button.pack(side='bottom', fill='x', pady=20)
    


    text_color = '#FFF8DC'  # A light color for text for contrast
    button_color = '#DEB887'  # A lighter shade of brown for buttons

    # Define colors and styles
    button_color1 = "#4f9cb5"  # The blue color you provided
    text_color1 = "white"  # White text for contrast
    style21 = font.Font(family="Helvetica", size=16, weight="bold")
############################################################################################################################################################





############################################################################################################################################################
    #Store exchange pages 
    Label(Apage1, text=" View / Add Saved Exchanges ", font=style1, bg=button_color, fg=text_color,bd=5, relief = 'raised').pack(pady=40)

    # Button configurations
    button_config = {
        "font": style2,
        "bg": button_color,
        "fg": text_color,
        "width": 30,
        "height": 2,
        "bd": 10,  # Border width
        "highlightthickness": 0,  # No highlight around the button
        "activebackground": button_color,  # Background color when the button is clicked
        "activeforeground": text_color  # Text color when the button is clicked
    }

    # Create and pack the View Saved Exchange Pages Button
    view_button = tk.Button(Apage1, text="View Saved Exchange Pages", command=lambda: show_page(), **button_config)
    view_button.pack(pady=20)

    # Create and pack the Add Exchange Page Button
    add_button = tk.Button(Apage1, text="Add Exchange Page", command=lambda: BasePage.tkraise(), **button_config)
    add_button.pack(pady=20)

    # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE2 = ttk.Button(Apage1, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button_MFUE2.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################






############################################################################################################################################################
    #base page that adds pages
    Label(BasePage, text=" Select Exchange You Want To Have Added ", font=style1, bg='#EAD9BD', fg='#A9926E',bd=10, relief = 'raised').pack(pady=20)

    Label(BasePage, text="From:", font=large_font, background='#A9926E', foreground='#EAD9BD',bd=5, relief = 'raised').pack(pady=10)
    from_currency_var1 = tk.StringVar()
    from_currency_menu1 = ttk.OptionMenu(BasePage, from_currency_var1, '', style='TMenubutton')
    from_currency_menu1.pack(pady=10)

    Label(BasePage, text="To:", font=large_font, background='#A9926E', foreground='#EAD9BD',bd=5, relief = 'raised').pack(pady=10)
    to_currency_var1 = tk.StringVar()
    to_currency_menu1 = ttk.OptionMenu(BasePage, to_currency_var1, '', style='TMenubutton')
    to_currency_menu1.pack(pady=10)

    def update_currency_options1():
            currencies = list(currency_rates.keys())
            menu1 = from_currency_menu1["menu"]
            menu1.delete(0, "end")
            for currency in currencies:
                menu1.add_command(label=currency, command=lambda value=currency: from_currency_var1.set(value))
            from_currency_var1.set("USD")

            menu1 = to_currency_menu1["menu"]
            menu1.delete(0, "end")
            for currency in currencies:
                menu1.add_command(label=currency, command=lambda value=currency: to_currency_var1.set(value))
            to_currency_var1.set("EUR")

    # Fetch live exchange rates
    fetch_live_exchange_rates(currency_rates, update_currency_options1)

    result_label1 = ttk.Label(BasePage, text="", font=result_font, background='#EAD9BD', foreground='black')
    result_label1.pack(pady=20)

    def show_new_widget_message():
        messagebox.showinfo("New Widget Added", "Go back to 'View Saved Exchange Pages' to view saved exhange!")

    convert_button = Button(BasePage, text="Click Here To Save",bd=5, relief = 'raised',bg='#EAD9BD', fg='#A9926E', command=lambda:[show_new_widget_message(),add_page(from_currency_var1, to_currency_var1,Apage1)], font=large_font)
    convert_button.pack()

    # Ensure that this button is packed last to appear at the bottom
    back_button = ttk.Button(BasePage, text="Back", command=lambda: Apage1.tkraise())
    back_button.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################






############################################################################################################################################################
    Label(page5, text=" Latest Currency News ", font=style1, bg='brown', fg='black',bd=10, relief = 'raised').pack(pady=20)


    def fetch_forex_news(api_key):
        url = "https://newsapi.org/v2/everything"
        parameters = {
            "q": "forex",  # Query for forex-related news
            "apiKey": api_key,
            "language": "en",
            "pageSize": 50,  # Number of articles to fetch
        }
        response = requests.get(url, params=parameters)
        return response.json()

    def display_news(api_key):
        news_data = fetch_forex_news(api_key)
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            news_text.configure(state='normal')  # Enable the widget for text insertion
            news_text.delete('1.0', tk.END)  # Clear previous news
            for i, article in enumerate(articles):
                news_text.insert(tk.END, f"Title: {article['title']}\n")
                news_text.insert(tk.END, f"Description: {article['description']}\n")
                url_start = news_text.index(tk.END+"-1c linestart")
                news_text.insert(tk.END, f"URL: {article['url']}\n\n")
                url_end = news_text.index(tk.END+"-1c linestart")
                news_text.tag_add(f"url{i}", url_start, url_end)
                news_text.tag_config(f"url{i}", foreground="blue", underline=True)
                news_text.tag_bind(f"url{i}", "<Button-1>", lambda e, url=article['url']: webbrowser.open(url))
            news_text.configure(state='disabled')  # Disable the widget again
        else:
            news_text.configure(state='normal')  # Enable the widget for text insertion
            news_text.insert(tk.END, "Failed to fetch news.")
            news_text.configure(state='disabled')  # Disable the widget again




    api_key = "1662a5c4dec64fabbf57cf04595fb0d9"



    # ScrolledText widget to display news
    news_text = scrolledtext.ScrolledText(page5, wrap=tk.WORD, width=150, height=35)
    news_text.pack(pady=10)


    # Button to fetch and display news
    fetch_news_button = ttk.Button(page5, text="Fetch Currency News", command=lambda: display_news(api_key))
    fetch_news_button.pack(pady=5)

    # Ensure that this button is packed last to appear at the bottom
    back_button_MFUE3 = ttk.Button(page5, text="Back to Home Page", command=lambda: page2.tkraise())
    back_button_MFUE3.pack(side='bottom', fill='x', pady=20)
############################################################################################################################################################






    
    page1.tkraise()
    window.mainloop()


if __name__ == "__main__":
    main()
