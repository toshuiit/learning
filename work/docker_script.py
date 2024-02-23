
import os
import sys
import questionary
from questionary import Choice
from questionary import Style
import mysql.connector
from mysql.connector import Error
import paramiko
import time


SERVER_TABLE = "GPU_SERVER"
CARDS_TABLE = "GPU_CARDS"



style_fancy = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#f44336 bold'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#cc5454'),         # style for a selected item of a checkbox
    ('separator', 'fg:#cc5454'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_mysql():
    connection = None
    print("Connecting to Database...")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="docker",
            passwd="blahblahblah..",
            database ="GPU_ALLOC",
           # port="3306"
        )
        print("Connected to Database !")
        clear_terminal()

    except Error as err:
        print(f"Error: '{err}'")
        sys.exit()

    return connection

connect_db = connect_mysql()

handle_none = lambda x: sys.exit() if x is None else x


def check_gpu_availablity(gpu_type,no_of_gpu):
    if connect_db.is_connected():
        cursor = connect_db.cursor()
        table_name = "GPU_SERVER"
        query = f"SELECT * FROM {table_name} WHERE CARD_TYPE = '{gpu_type}' AND AVAILABLE_GPU >= {no_of_gpu}"
        cursor.execute(query)
        rows = cursor.fetchall()
        if cursor.rowcount > 0:
            return True
        else:
            return False

def find_and_assign_gpu(gpu_type,no_of_gpu,image_type,username,duration):
    if connect_db.is_connected():
        cursor = connect_db.cursor()
        query = f"SELECT * FROM {SERVER_TABLE} WHERE CARD_TYPE = '{gpu_type}' AND AVAILABLE_GPU >= {no_of_gpu}"
        cursor.execute(query)
        gpu_server = cursor.fetchone()
        server_id = gpu_server[0]
        gpu_hostname = gpu_server[1]
        cursor.close()

        cursor = connect_db.cursor()
        card_query = f"SELECT * FROM {CARDS_TABLE} WHERE SERVER_ID = '{server_id}' AND AVAILABILITY = 0x01"
        cursor.execute(card_query)
        gpu_cards = cursor.fetchmany(no_of_gpu)
        results = cursor.fetchall()
        cursor.close()

        card_num=[]

        for card_details in gpu_cards:
            gpu_no = card_details[0].split("_",1)[1]
            card_num.append(gpu_no)

        ## Creating the docker container

        host = gpu_hostname+"."+"domain"
        password = "blahblahblah..."
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host,port=22, username="username", password=password)

        gpu_string = ','.join(map(str, card_num))
        container_name = gpu_hostname+'_'+gpu_string.replace(",","_")
        port = str (10000 + int(card_num[0]) +1)
        command = f"sudo docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES='{gpu_string}' --shm-size 8G -it -p {port}:22 --name {container_name} -v /data/{username}:/data -d  {image_type} "
        # Copy the authenticator.py file to the user's directory
        auth_file_cp_cmd = f"sudo cp /data/authenticator.py /data/{username}/authenticator.py"

        docker_created = 0

        # Execute the command on the Docker client
        _stdin, _stdout, _stderr = client.exec_command(command)

        # Wait for 3 seconds
        time.sleep(3)

        # Check if the Docker container was created successfully
        if _stdout.read().decode('utf-8').strip() != '':
            print('Docker container created successfully!')
            details = f'Details are as follows:\nContainer Name: {container_name}\nUserName: {username}\nHost: {gpu_hostname}\nPort:{port}'
            print(details)

            # Copy the authenticator.py file to the user's directory inside the container
            _in, _out, _err = client.exec_command(auth_file_cp_cmd)
            docker_created = 1
        else:
            print('Error creating Docker container:', _stderr.read().decode('utf-8').strip())

        # Start the SSH service inside the container
        stdin, stdout, stderr = client.exec_command(f"sudo docker exec {container_name} service ssh start")

        client.close()

        # Update the available GPU count in the server table
        if docker_created == 1:
            cursor = connect_db.cursor()
            query = f"UPDATE {SERVER_TABLE} SET AVAILABLE_GPU = AVAILABLE_GPU-{no_of_gpu} WHERE SERVER_ID = {server_id} AND HOSTNAME = '{gpu_hostname}'"
            cursor.execute(query)
            connect_db.commit()
            cursor.close()

            # Update the GPU card details in the cards table
            for card_details in gpu_cards:
                cursor = connect_db.cursor()
                gpu_card_update_query = f"UPDATE {CARDS_TABLE} SET availability = 0x00, username = '{username}', container_name = '{container_name}',ASSIGNED_DATE = NOW(), requested_days = {duration}, port_no ={port}, EXP_DATE = DATE_ADD( NOW(), INTERVAL {duration} DAY) where ID='{card_details[0]}' "
                cursor.execute(gpu_card_update_query)
                connect_db.commit()
                cursor.close()

        # Function to create a new container
def createContainer():
            clear_terminal()
            print("Let's create a new container\n")

            # Ask for GPU type and number of cards needed
            gpu_type = handle_none(questionary.select(
                "What do you want to do?",
                choices=["1080", "1080Ti", "A40", "P5000"]).ask())
            no_of_gpu = handle_none(questionary.select("How many card do you need ?", choices=[Choice(title="One Card", value=1), Choice(title="Two Cards", value=2), ]).ask())

            # Check if the requested GPU type and number of cards are available
            gpu_available = check_gpu_availablity(gpu_type, no_of_gpu)

            if gpu_available:
                username_accept = False
                counter = 0

                # Ask for username and validate it
                while username_accept is False:
                    if counter > 0:
                        print("\x1b[2A\x1b[0J", end="")
                    username = questionary.text("Please enter username", validate=lambda text: len(text) > 0).ask()
                    username_accept = questionary.confirm(f"Are you sure username is {username} ?").ask()
                    counter = counter + 1

                # Ask for duration and image type
                duration = questionary.text("For how long you want GPU ?", validate=lambda x: 0 < int(x) < 9 if x.isdigit() else False).ask()
                image_type = questionary.select("Please select image type", choices=[Choice(title="gpu-image-v1:latest", value="gpu-image-v1:latest"), Choice(title="pytorch:v1", value="pytorch:v1"), ]).ask()
                clear_terminal()

                # Confirm the container creation
                confirm_creation = questionary.confirm(f"Do you want to create a container with {gpu_type} ({no_of_gpu})for {username} ({duration} days) ?").ask()

                if(confirm_creation):
                    find_and_assign_gpu(gpu_type, no_of_gpu, image_type, username, duration)
                else:
                    main_menu()

            elif gpu_available is False:
                print(f"{gpu_type} with {no_of_gpu} is not currently available.")
                print("\nThank You!")

        # Function to renew a container
def renewContainer():
            clear_terminal()
            print("Let's renew a container\n")
            if connect_db.is_connected():
                try:
                    cursor = connect_db.cursor()
                    query = f"SELECT DISTINCT CONTAINER_NAME FROM {CARDS_TABLE} WHERE AVAILABILITY IN (0x00, 0x10)"
                    container_list = []
                    cursor.execute(query)
                    container_data = cursor.fetchall()
                    cursor.close()

                    for gpu_name in container_data:
                        container_list.append(gpu_name[0])

                    if len(container_list) == 0:
                        print("No Container to renew!!")
                        return 0

                    # Ask for the container name, renewal starting date, and duration
                    container_name = questionary.autocomplete(
                        'Enter name of container to renew...\n',
                        choices=container_list,
                        style=style_fancy
                    ).ask()
                    container_renewal_date = questionary.text("Enter renewal starting date in YYYY-MM-DD?").ask()
                    duration = questionary.text("For how long you want GPU ?", validate=lambda x: 0 < int(x) < 9 if x.isdigit() else False).ask()

                    # Update the container details in the cards table
                    update_query = f"UPDATE {CARDS_TABLE} SET ASSIGNED_DATE = '{container_renewal_date}', EXP_DATE = DATE_ADD('{container_renewal_date}', INTERVAL {duration} DAY), requested_days = {duration}, AVAILABILITY = 0x10 WHERE CONTAINER_NAME = '{container_name}'"
                    cursor = connect_db.cursor()
                    cursor.execute(update_query)
                    connect_db.commit()

                    print(f"Renewing container {container_name}...")
                    print("Renewal successful!")

                except Exception as e:
                    print(f"Error occurred during renewal: {e}")
                    raise

# Function to delete a container
def deleteContainer():
            clear_terminal()
            print("Let's delete a container\n")
            if connect_db.is_connected():
                cursor = connect_db.cursor()
                query = f"SELECT DISTINCT CONTAINER_NAME FROM {CARDS_TABLE} WHERE AVAILABILITY IN (0x00, 0x10)"
                container_list = []
                cursor.execute(query)
                container_data = cursor.fetchall()
                cursor.close()

                for gpu_name in container_data:
                    container_list.append(gpu_name[0])

                if len(container_list) == 0:
                    print("No Container to delete!!")
                    return 0
                container_name = questionary.autocomplete('Enter name of container to be deleted...\n', choices=container_list, style=style_fancy).ask()

                if container_name in container_list:
                    cursor = connect_db.cursor()
                    container_query = f"SELECT * FROM {CARDS_TABLE} WHERE CONTAINER_NAME = '{container_name}'"
                    cursor.execute(container_query)
                    query_data = cursor.fetchall()
                    number_of_gpu = len(query_data)
                    server_id = query_data[0][1]

                    host_query = f"SELECT * FROM {SERVER_TABLE} WHERE SERVER_ID ={server_id}"
                    cursor.execute(host_query)
                    server_data = cursor.fetchall()
                    gpu_hostname = server_data[0][1]
                    delete_cards = f"UPDATE {CARDS_TABLE} SET availability = 0x01, username = NULL , container_name = NULL ,ASSIGNED_DATE = NULL,EXP_DATE= NULL, requested_days = NULL , port_no =NULL where CONTAINER_NAME='{container_name}'"
                    update_gpu = f"UPDATE {SERVER_TABLE} SET AVAILABLE_GPU = AVAILABLE_GPU+{number_of_gpu} WHERE SERVER_ID = {server_id}"

                    # Delete the container
                    host = gpu_hostname + "." + "cse.iitk.ac.in"
                    password = "@LinTrix#"
                    client = paramiko.client.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(host, port=22, username="admin", password=password)
                    command = f"sudo docker stop {container_name} && sudo docker rm {container_name}"

                    confirm_removal = questionary.confirm(f"Are you sure to delete {container_name} from server.").ask()
                    if (confirm_removal):
                        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
                        outlines = ssh_stdout.readlines()
                        resp = ''.join(outlines)
                        ret = resp.find(container_name)
                        if (ret != -1):
                            print("Removed from Server.\n")
                            cursor.execute(delete_cards)
                            connect_db.commit()
                            cursor.close()
                            cursor = connect_db.cursor()
                            cursor.execute(update_gpu)
                            connect_db.commit()
                            cursor.close()
                            print(f'{container_name} deleted successfully!')
                        else:
                            print("Failed to remove container.\nNote: Please do it urgently Now\n")
                            confirm_deletion = questionary.confirm(f"Do you want to delete entry from database.").ask()
                            if (confirm_deletion):
                                cursor.execute(delete_cards)
                                connect_db.commit()
                                cursor.close()
                                cursor = connect_db.cursor()
                                cursor.execute(update_gpu)
                                connect_db.commit()
                                cursor.close()
                                print(f'{container_name} deleted successfully from database!')

                else:
                    print(f'Invalid container name!')

# Main menu function
def main_menu():
    main_menu_choice = None

    while main_menu_choice is None:
        clear_terminal()
        print("Docker Allocation\n\nChoose What You Want to Do:\n")
        main_menu_choice = questionary.select(
        "What do you want to do?",
        choices=[Choice(title="Create a Conatiner", value=1), Choice(title="Delete a Container", value=2), Choice(title="Renew a container", value=3), Choice(title="Exit", value=-1), ]).ask()

        if main_menu_choice == 1:
            createContainer()
        elif main_menu_choice == 2:
                deleteContainer()
        elif main_menu_choice == 3:
                renewContainer()
        elif main_menu_choice == -1:
                print("Thank You !")
                sys.exit()

        if __name__ == '__main__':
            main_menu()
