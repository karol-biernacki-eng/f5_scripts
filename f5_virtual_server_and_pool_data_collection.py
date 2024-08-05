import requests
import csv

# Disable requests module warning
requests.packages.urllib3.disable_warnings()

def collect_f5_data():
    device = "192.168.0.65"
    url = f"https://{device}/mgmt/tm/ltm/virtual"
    username = "admin"
    password = "karol1985"

    try:
        response = requests.get(url, auth=(username, password), verify=False)
        response.raise_for_status()
        data = response.json()

        with open('f5_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device','Virtual Server', 'IP Address', 'Port', 'Pool', 'Partition', 'Pool Members'])

            for virtual_server in data['items']:
                name = virtual_server['name']
                port = virtual_server['destination'].split(':')[1]
                partition = virtual_server['partition']
                ip_address = virtual_server['destination'].split(':')[0].split('/')[2]  # Remove partition name

                if 'pool' in virtual_server:
                    pool_name_clean = virtual_server['pool']
                    #  Remove partition name from pool name
                    pool_name_clean = pool_name_clean.split('/')[1]
                    pool = virtual_server['pool']
                    # Create pool variable in correct format : ~Partition1~Test_Pool1
                    pool = pool.replace('/', '~')
                    pool_members = get_pool_members(pool, username, password)  # Call get_pool_members() function
                else:
                    pool = "N/A"
                    pool_name_clean = "N/A"
                    pool_members = []

                writer.writerow([device, name, ip_address, port, pool_name_clean, partition, pool_members])

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def get_pool_members(pool, username, password):

    url = f"https://192.168.0.65/mgmt/tm/ltm/pool/{pool}/members"

    try:
        response = requests.get(url, auth=(username, password), verify=False)
        response.raise_for_status()
        data = response.json()

        pool_members = []
        for member in data['items']:
            pool_members.append(member['name'])

        return pool_members

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    collect_f5_data()
