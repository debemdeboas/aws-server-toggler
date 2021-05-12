from threading import Thread, Event
import tkinter as tk
from tkinter import messagebox
import boto3
import time
import configparser


event_configuration_ready = Event()

def server_monitor():
    event_configuration_ready.wait()

    global ec2;
    ec2 = boto3.client('ec2', aws_access_key_id=config['default']['ACCESS_KEY'], aws_secret_access_key=config['default']['SECRET_KEY'], region_name=config['default']['REGION'])

    while True:
        response = ec2.describe_instances(InstanceIds=[config['default']['INSTANCE_ID']])
        server_state = response['Reservations'][0]['Instances'][0]['State']['Name'].lower()

        tk_server_status['text'] = server_state.capitalize()

        # check current state
        if server_state == 'running':
            # stop the server
            tk_button_on_off.configure(state='active')
            tk_button_on_off['text'] = f'Stop server'
            tk_server_status.configure(bg='green', fg='azure')
        elif server_state == 'stopped':
            # start the server
            tk_button_on_off.configure(state='active')
            tk_button_on_off['text'] = f'Start server'
            tk_server_status.configure(bg='red3', fg='azure')
        else:
            # do nothing because the server is pending
            tk_server_status.configure(bg='yellow', fg='black')
            tk_button_on_off.configure(state='disabled')

        time.sleep(0.5)


def tk_button_on_off_on_click():
    server_state = tk_server_status['text'].lower()

    # check current state
    if server_state == 'running':
        # stop the server
        ec2.stop_instances(InstanceIds=[config['default']['INSTANCE_ID']])
    elif server_state == 'stopped':
        # start the server
        ec2.start_instances(InstanceIds=[config['default']['INSTANCE_ID']])
    else:
        # do nothing because the server is pending
        return


def tk_about_on_click():
    messagebox.showinfo('About', 'Made with love by @debemdeboas on GitHub', master=root)


def tk_configure_on_click():
    configuration = tk.Tk()
    configuration.geometry('500x100')
    configuration.title('Server Configuration')
    configuration.wm_resizable(False, False)
    configuration.iconbitmap('icon.ico')
    
    tk_label_access_key = tk.Label(configuration, text='Access key:')
    tk_entry_access_key = tk.Entry(configuration, width=70)
    tk_label_access_key.grid(row=0, column=0)
    tk_entry_access_key.grid(row=0, column=1)
    tk_entry_access_key.delete(0, tk.END)
    tk_entry_access_key.insert(0, config['default']['ACCESS_KEY'])

    tk_label_secret_key = tk.Label(configuration, text='Secret key:')
    tk_entry_secret_key = tk.Entry(configuration, width=70)
    tk_label_secret_key.grid(row=1, column=0)
    tk_entry_secret_key.grid(row=1, column=1)
    tk_entry_secret_key.delete(0, tk.END)
    tk_entry_secret_key.insert(0, config['default']['SECRET_KEY'])
    
    tk_label_region = tk.Label(configuration, text='Region:')
    tk_entry_region = tk.Entry(configuration, width=70)
    tk_label_region.grid(row=2, column=0)
    tk_entry_region.grid(row=2, column=1)
    tk_entry_region.delete(0, tk.END)
    tk_entry_region.insert(0, config['default']['REGION'])

    tk_label_instance_id = tk.Label(configuration, text='Instance ID:')
    tk_entry_instance_id = tk.Entry(configuration, width=70)
    tk_label_instance_id.grid(row=3, column=0)
    tk_entry_instance_id.grid(row=3, column=1)
    tk_entry_instance_id.delete(0, tk.END)
    tk_entry_instance_id.insert(0, config['default']['INSTANCE_ID'])

    def set_and_close():
        global config;

        config.set('default', 'ACCESS_KEY', tk_entry_access_key.get())
        config.set('default', 'SECRET_KEY', tk_entry_secret_key.get())
        config.set('default', 'REGION', tk_entry_region.get())
        config.set('default', 'INSTANCE_ID', tk_entry_instance_id.get())

        # validate configuration
        try:
            boto3.client('ec2', aws_access_key_id=config['default']['ACCESS_KEY'], aws_secret_access_key=config['default']['SECRET_KEY'], region_name=config['default']['REGION'])

            config.write(open('config.ini', 'w'))
            ready()
        except:
            # invalid configuration
            tk_server_status['text'] = 'Invalid configuration'
        configuration.destroy()

    configuration.protocol('WM_DELETE_WINDOW', set_and_close)
    configuration.mainloop()


def ready():
    event_configuration_ready.set()


root = tk.Tk()
root.geometry('350x180')
root.title('AnsibleSI Manager')
root.wm_resizable(False, False)
root.iconbitmap('icon.ico')

tk_status = tk.Label(text='Server status:', pady=5)
tk_status.pack()

tk_server_status = tk.Label(text='Waiting confiugration', width=20, height=2, font=('Arial', 14))
tk_server_status.pack(pady=10)

tk_button_on_off = tk.Button(text='Waiting...', width=25, height=2, state='disabled', command=tk_button_on_off_on_click)
tk_button_on_off.pack()

tk_menubar = tk.Menu(root)
tk_about_menu = tk.Menu(root, tearoff=0)
tk_about_menu.add_command(label='About', command=tk_about_on_click)

tk_menubar.add_command(label='Configure', command=tk_configure_on_click)
tk_menubar.add_cascade(label='Help', menu=tk_about_menu)
root.config(menu=tk_menubar)

# load configuration
config = configparser.ConfigParser()
config.add_section('default')
config['default'] = {'ACCESS_KEY': '', 'SECRET_KEY': '', 'REGION': '', 'INSTANCE_ID': ''}
config.read('config.ini')
if config['default']['ACCESS_KEY'] != '' and \
    config['default']['SECRET_KEY'] != '' and \
    config['default']['REGION'] != '' and \
    config['default']['INSTANCE_ID'] != '':
    ready()

# start
Thread(target=server_monitor, daemon=True).start()
root.mainloop()
