import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext
import pyperclip
import random
import requests
import time
import pika

start_time = time.time()  # Record start time

def generate_unique_random_numbers(n, start, end):
    if n > (end - start + 1):
        raise ValueError("Range is too small to generate the required number of unique random numbers.")
    
    random_numbers = set()
    while len(random_numbers) < n:
        random_numbers.add(random.randint(start, end))
    return list(random_numbers)

def generate_customer_data(customer_count, currency, biller_code):

    data = []
    
    for i in range(customer_count):
        customer_code = f"234-8101{i+2}"
        if currency == "Mix":
            customer_currency = "USD" if i % 2 == 0 else "KHR"
        else:
            customer_currency = currency

        customer_data = {
            # "ConsumerId": consumer_ids[i],
            "CompanyCode": biller_code,
            "BranchCode": biller_code,
            "Company": "លោក ​ឈឹម គឹមឈន",
            "Branch": "លោក ​ឈឹម គឹមឈន",
            "Code": customer_code,
            "Name": f"ដារ៉ា {i+1}",
            "Currency": customer_currency,
            "AddressText": "ភូមិជ្រោយមេត្រីលើ ឃុំប្ញស្សីជ្រោយ",
            "RefId": f"333test03{i+1}",
            "Transformer": "ចំនុចភ្ជាប់ទី២ (ឬស្សីជ្រោយ)",
            "FeederNo": f"B00{i+1}",
            "BoxCode": f"B00{i+1}02"
        }
        data.append(customer_data)

    return data

def generate_bill_data(bill_count, customers, invoice_status, usd_range, khr_range, biller_code, customer_currency):
    bills = []
    for i in range(bill_count):
        
        customer = customers[i % len(customers)]
        customer_code = customer["Code"]
        customer_currency = customer["Currency"]

        if customer_currency == "USD":
            amount = round(random.uniform(usd_range[0], usd_range[1]), 2)
        elif customer_currency == "KHR":
            amount = random.randint(khr_range[0], khr_range[1])
        elif customer_currency == "Mix":
            if random.choice([True, False]):
                amount = round(random.uniform(usd_range[0], usd_range[1]), 2)
                customer_currency = "USD"
            else:
                amount = random.randint(khr_range[0], khr_range[1])
                customer_currency = "KHR"
        else:
            raise ValueError("Invalid currency type specified.")    
        
        # # Determine the invoice status and set the paid amount accordingly
        # if invoice_status == "Mix":
        #     status = "មិនទាន់បង់" if i % 2 == 0 else "បានបង់"
        # else:
        #     status = invoice_status

        # if status == "បានបង់":
        #     paid_amount = amount
        # else:
        #     paid_amount = 0

        # Determine the invoice status and set the paid amount accordingly
        if invoice_status == "Mix":
            if i % 3 == 0:
                status = "មិនទាន់បង់"  # Unpaid
            elif i % 3 == 1:
                status = "បានបង់"  # Paid
            else:
                status = "លុប"  # Deleted
        else:
            status = invoice_status

        if status == "បានបង់":
            paid_amount = amount
        elif status == "លុប":
            paid_amount = amount - amount
        else:  # This includes "មិនទាន់បង់"
            paid_amount = 0


        details = [
            {"RowNo": 1, "ItemName": "ថ្លៃអគ្គិសនី", "ItemNote": "20806926", "Price": 480.00000, "Quantity": 50.0000, "Amount": 24000.000000000, "MeterCurrent": 5100.0000, "MeterPrevoius": 5050.0000, "MeterCode": "20806926", "MeterMultiplier": 1, "MeterTotal": 50.0000, "MeterClass": "1", "TranDate":datetime.now().isoformat(), "RefNo":f"CINV25-151{i+1}"}
        ]

        bill_data = {
            "BillerCode": biller_code,
            "InvoiceStatusText": status,
            "InvoiceTitle": f"ថ្លៃអគ្គិសនី  ខែ6ឆ្នាំ2024",
            "InvoiceNo": f"CINV27-129{i+1}",
            "CustomerCode": customer_code,
            "ConsumerCode": customer_code,
            "CustomerName": f"Moon JeIN {i+1}",
            "Ampere": "8A",
            "AreaName": "C01",
            "PoleCode": f"00{i+1}",
            "BoxCode": f"C00{i+1}03",
            "BillingAddress": "ភូមិជ្រោយមេត្រីលើ ឃុំប្ញស្សីជ្រោយ",
            "Location": "ភូមិជ្រោយមេត្រីលើ ឃុំប្ញស្សីជ្រោយ",
            "InvoiceMonth": "2024-07-01T01:01:01",
            "InvoiceDate": "2024-07-01T10:54:54",
            "StartUseDate": "2024-07-01T01:02:00",
            "EndUseDate": "2024-07-30T23:59:59",
            "StartPaymentDate": "2024-07-10T06:09:59",
            "TotalDays": 29,
            "TotalAmount": amount,
            "AmountToPay": amount,
            "Currency": customer_currency,
            "DueDate": "2024-12-12T00:00:00",
            "OpeningBalance": 45090,
            "LastDueAmount": 81690,
            "LastPayAmount": 36600,
            "LastPaymentDate": "2024-05-03T16:45:08",
            "PaidAmount": paid_amount,  # Update the paid amount here
            "BranchName": "សហគ្រាស សូហ្វថេក",
            "BranchAddress": "ឃុំឬស្សីជ្រោយ ឃុំព្រែកដំបង និងឃុំព្រែកអញ្ចាញ ស្រុកមុខកំពូល ខេត្តកណ្តាល\r\n(098) 357 666 /(098) 237 666",
            "BranchPhone": f"01033344{i+1}",
            "ConsumptionHistory": json.dumps([
                {"d": "2023-06-01T00:00:00", "x": 29, "t": 57},
                {"d": "2023-07-01T00:00:00", "x": 30, "t": 59},
                {"d": "2023-08-01T00:00:00", "x": 30, "t": 61},
                {"d": "2023-09-01T00:00:00", "x": 29, "t": 57},
                {"d": "2023-10-01T00:00:00", "x": 30, "t": 61},
                {"d": "2023-11-01T00:00:00", "x": 29, "t": 54},
                {"d": "2023-12-01T00:00:00", "x": 30, "t": 53},
                {"d": "2024-01-01T00:00:00", "x": 30, "t": 54},
                {"d": "2024-02-01T00:00:00", "x": 28, "t": 51},
                {"d": "2024-03-01T00:00:00", "x": 30, "t": 60},
                {"d": "2024-04-01T00:00:00", "x": 29, "t": 62},
                {"d": "2024-05-01T00:00:00", "x": 30, "t": 15}
            ]),
            "Details": json.dumps(details, ensure_ascii=False),  # Ensure Unicode is preserved
            "ParentRefId": f"333Test05{i+2}",
            "RefId": f"333Test05{i+2}",
            # "BranchId": "234",
            "BranchCode": biller_code,
            "CompanyCode": biller_code
        }
        bills.append(bill_data)

    return bills   

def submit_data():
    try:
        customer_count = int(customer_count_entry.get())
        customer_currency = customer_currency_var.get()
        bill_count = int(bill_count_entry.get())
        invoice_status = invoice_status_var.get()  # Assuming invoice_status_var contains the status directly
        biller_code = biller_code_entry.get()  # Get the BillerCode from the entry field

        # Define amount ranges based on currency
        usd_range = (1, 100)
        khr_range = (100, 10000000)

        if customer_count > 0:
            customers = generate_customer_data(customer_count, customer_currency, biller_code)
        else:
            customers = []

        # Check if customer count is 0 but bill count is greater than 0
        if customer_count == 0 and bill_count > 0:
            # Create dummy customers with codes only
            customers = [{"Code": f"234-Dummy{i+1}", "Currency": random.choice(["USD", "KHR"])} for i in range(bill_count)]

        if customers:
            bills = generate_bill_data(bill_count, customers, invoice_status, usd_range, khr_range, biller_code, customer_currency)
        else:
            bills = []

        json_data = {
            "BillerCode": biller_code,
            "PushBackResult": True,
            "PushNotification": True,
            "SyncDate": datetime.now().isoformat(),
            "SyncBillDatas": bills,
            "SyncConsumerDatas": customers
        }

        json_text = json.dumps(json_data, ensure_ascii=False, indent=4)
        json_textbox.delete(1.0, tk.END)
        json_textbox.insert(tk.END, json_text)

        total_amount = sum(bill["TotalAmount"] for bill in bills)
        amount_to_pay = sum(bill["AmountToPay"] for bill in bills)
        paid_amount = sum(bill["PaidAmount"] for bill in bills)

        messagebox.showinfo("Data Generated", f"Total Customers: {customer_count}\nTotal Bills: {bill_count}\nTotal Amount: {total_amount}\nAmount To Pay: {amount_to_pay}\nPaid Amount: {paid_amount}")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for customer and bill counts.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

        
def publish_message(json_textbox):
    try:
        # RabbitMQ credentials
        username = 'b24developer'
        password = 'b24developer'
        # rabbitmq_host = '192.168.197.5' old
        rabbitmq_host = '192.168.197.18'
        # rabbitmq_port = '5674' old
        rabbitmq_port = '4673' 
        # rabbitmq_vhost = '/'
        # rabbitmq_vhost = 'billgatewaystage' old
        rabbitmq_vhost = 'billgateway'
        rabbitmq_exchange = 'SYNC_DATA-exchange'
        rabbitmq_queue = 'SYNC_DATA'
        QH_BUSINESS_PROFILE_ID = '32a645ef-060f-487e-ba9b-21efab99b3fd' #234
        # QH_BUSINESS_PROFILE_ID = '32a645ef-060f-487e-ba9b-21efab99b3ff' #333
        # QH_BUSINESS_PROFILE_ID = 'e2aab44d-4470-4108-b599-337c29cb3bcd' #128

        # Check if JSON textbox content is empty
        json_content = json_textbox.get("1.0", "end").strip()

        payload = json.loads(json_content)

        payload_str = json.dumps(payload)

        # Connection parameters
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_vhost,
            credentials=credentials
        )

        # Establish connection and channel
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Print connection parameters
        print("Connection Parameters:", parameters)

        # print("URL Queue:", {publish_url})

        # Message properties
        properties = {
            'routing_key': rabbitmq_queue,
            'properties': {
                'delivery_mode': 1  # Non-persistent
            },
            # 'payload': json.dumps(payload, ensure_ascii=False),
            'payload': payload_str,
            'payload_encoding': 'string',
        }

        # Declare the exchange
        channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='direct', durable=True)

        # Publish the message with custom properties
        properties = pika.BasicProperties(
            delivery_mode=1,  # Non-persistent
            headers={'QH-BUSINESS-PROFILE-ID': QH_BUSINESS_PROFILE_ID}
        )

        # Record start time
        start_time = time.time()

        channel.basic_publish(
            exchange=rabbitmq_exchange,
            routing_key=rabbitmq_queue,
            body=payload_str,
            properties=properties
        )

        # Calculate response time
        response_time = time.time() - start_time
        
        print("channel:",parameters)
        print(f"Message published to queue '{rabbitmq_queue}': success")
        print(f"Response time: {response_time:.6f} seconds")

       
        # Close the connection
        connection.close()

    except pika.exceptions.AMQPConnectionError as e:
        print(f"AMQP connection error occurred: {e}",parameters)
    except pika.exceptions.AuthenticationError:
        print("Authentication with RabbitMQ failed. Please check your username and password.")
    except pika.exceptions.ChannelError as e:
        print(f"Channel error occurred: {e}")
    except pika.exceptions.AMQPError as e:
        print(f"An AMQP error occurred: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON content.")
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def create_gui():
    global json_frame
    # Your GUI creation code here...
    root = tk.Tk()
    root.title("Customer and Bill Data Generator")
    json_frame = tk.LabelFrame(root, text="JSON Data", padx=10, pady=10)
    json_frame.pack(padx=10, pady=10, fill="both", expand=True)
    json_textbox = scrolledtext.ScrolledText(json_frame, width=80, height=20, wrap=tk.WORD)
    json_textbox.pack(padx=5, pady=5, fill="both", expand=True)
    return json_textbox


# Define function to copy JSON to clipboard
def copy_to_clipboard():
    json_text = json_textbox.get(1.0, tk.END)
    pyperclip.copy(json_text)
    messagebox.showinfo("Copied", "JSON data copied to clipboard")

# Define function to save JSON to file
def save_to_file():
    json_text = json_textbox.get(1.0, tk.END)
    with open("customer_data_with_bills.json", "w", encoding="utf-8") as json_file:
        json_file.write(json_text)
    messagebox.showinfo("Saved", "JSON data saved to customer_data_with_bills.json")

def edit_data():
    # Open a new window to edit JSON data
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit JSON Data")

    # Create a text box to edit JSON data
    edited_json_textbox = scrolledtext.ScrolledText(edit_window, width=80, height=20, wrap=tk.WORD)
    edited_json_textbox.insert(tk.INSERT, json_textbox.get("1.0", "end"))
    edited_json_textbox.pack(padx=5, pady=5, fill="both", expand=True)

    # Create a button to save edited JSON data
    save_button = tk.Button(edit_window, text="Save", command=lambda: save_edited_data(edit_window, edited_json_textbox))
    save_button.pack(pady=5)

def save_edited_data(edit_window, edited_json_textbox):
    # Save edited JSON data and close the edit window
    edited_json_data = edited_json_textbox.get("1.0", "end")
    try:
        # Load the edited JSON data
        edited_json = json.loads(edited_json_data)
        # Dump the JSON data back to string with proper formatting
        formatted_json = json.dumps(edited_json, ensure_ascii=False, indent=4)
        # Clear the original textbox and insert the formatted JSON
        json_textbox.delete("1.0", "end")
        json_textbox.insert(tk.INSERT, formatted_json)
    except json.JSONDecodeError as e:
        # If JSON decoding fails, display an error message
        tk.messagebox.showerror("Error", f"Invalid JSON: {e}")
    edit_window.destroy()

# Setup the GUI
# Initialize the main window
root = tk.Tk()
root.title("Customer and Bill Data Generator")

# Biller Section
biller_frame = tk.LabelFrame(root, text="Biller Section", padx=10, pady=10)
biller_frame.pack(padx=10, pady=10, fill="x")

# Create label and entry field for Biller Code
tk.Label(biller_frame, text="Biller Code:").grid(row=0, column=0, padx=5, pady=5)
biller_code_entry = tk.Entry(biller_frame)
biller_code_entry.grid(row=0, column=1, padx=5, pady=5)

# Customer Section
customer_frame = tk.LabelFrame(root, text="Customer Section", padx=10, pady=10)
customer_frame.pack(padx=10, pady=10, fill="x")

# Create labels and entry for customer count
tk.Label(customer_frame, text="Count:").grid(row=0, column=0, padx=5, pady=5)
customer_count_entry = tk.Entry(customer_frame)
customer_count_entry.grid(row=0, column=1, padx=5, pady=5)

# Create labels and option menu for customer currency
tk.Label(customer_frame, text="Currency:").grid(row=1, column=0, padx=5, pady=5)
customer_currency_var = tk.StringVar(value="KHR")
tk.OptionMenu(customer_frame, customer_currency_var, "KHR", "USD", "Mix").grid(row=1, column=1, padx=5, pady=5)

# Bill Section
bill_frame = tk.LabelFrame(root, text="Bill Section", padx=10, pady=10)
bill_frame.pack(padx=10, pady=10, fill="x")

# Create labels and entry for bill count
tk.Label(bill_frame, text="Count:").grid(row=0, column=0, padx=5, pady=5)
bill_count_entry = tk.Entry(bill_frame)
bill_count_entry.grid(row=0, column=1, padx=5, pady=5)

# Create labels and option menu for bill currency
tk.Label(bill_frame, text="Currency:").grid(row=1, column=0, padx=5, pady=5)
bill_currency_var = tk.StringVar(value="KHR")
tk.OptionMenu(bill_frame, bill_currency_var, "KHR", "USD", "Mix").grid(row=1, column=1, padx=5, pady=5)

# Create labels and option menu for invoice status
tk.Label(bill_frame, text="Invoice Status:").grid(row=2, column=0, padx=5, pady=5)
invoice_status_var = tk.StringVar(value="មិនទាន់បង់")
tk.OptionMenu(bill_frame, invoice_status_var, "មិនទាន់បង់", "បានបង់", "លុប", "Mix").grid(row=2, column=1, padx=5, pady=5)

# Submit Section
submit_frame = tk.Frame(root, padx=10, pady=10)
submit_frame.pack(padx=10, pady=10, fill="x")

# Create button to generate data
submit_button = tk.Button(submit_frame, text="Generate Data", command=submit_data)
submit_button.pack(side=tk.LEFT, padx=(10, 0))  # Button aligned to the left with padding on the right
# Button to push data to the queue
push_queue_button = tk.Button(submit_frame, text="Push to Queue", command=lambda: publish_message(json_textbox), bg="blue", fg="white")
push_queue_button.pack(side=tk.RIGHT, padx=(0, 10))  # Button aligned to the left with padding on the right


# JSON Display Section
json_frame = tk.LabelFrame(root, text="JSON Data", padx=10, pady=10)
json_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Create scrolled text box to display JSON data
json_textbox = scrolledtext.ScrolledText(json_frame, width=80, height=20, wrap=tk.WORD)
json_textbox.pack(padx=5, pady=5, fill="both", expand=True)

# publish_message(json_textbox)

# Buttons for Copying and Saving JSON
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

# Create button to copy JSON to clipboard
copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=0, column=0, padx=5, pady=5)

# Create button to save JSON to file
save_button = tk.Button(button_frame, text="Save to File", command=save_to_file)
save_button.grid(row=0, column=1, padx=5, pady=5)

# Button to edit JSON data
edit_json_button = tk.Button(button_frame, text="Edit JSON Data", command=edit_data)
edit_json_button.grid(row=0, column=2, padx=5, pady=5)

# Call the function
# publish_message(json_textbox)

# Start the main loop
root.mainloop()