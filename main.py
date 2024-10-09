import os
import json
import datetime
from SubTools.DNS_Record_Lookup import dns_lookup as dns_record_lookup
from SubTools.Brute_Force_Subdomain_Enumeration import brute_force_subdomains as subdomain_enumerator
from SubTools.Zone_Transfer import zone_transfer as zone_transfer
from SubTools.DNSSEC_Validation import validate_dnssec as dnssec_validation
from SubTools.Reverse_DNS_Lookup import reverse_dns_lookup_from_domain as reverse_dns

# Dictionary that maps user input to the specific DNS scan functions
dns_scans = {
    1: dns_record_lookup,
    2: subdomain_enumerator,
    3: zone_transfer,
    4: dnssec_validation,
    5: reverse_dns
}

def get_domain():
    while True:
        domain = input("Enter the domain name to scan: ").strip()
        if domain:
            return domain
        print("Domain name cannot be empty. Please try again.")

def get_json_filename(domain):
    while True:
        print("Enter the full path for the output JSON file (e.g., /path/to/filename.json)")
        print("Or just press enter to save in the same directory as the script")
        file_path = input().strip()

        # If the user presses enter, default to the current directory with domain name
        if file_path == '':
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_path = os.path.join(os.path.dirname(__file__), 'JSON_Dumps', f'{domain}_{current_datetime}.json')
            # file_path = os.path.join(os.path.dirname(__file__), 'JSON_Dump', f'{domain}.json')

        # Ensure the file has a .json extension if not provided
        if not file_path.endswith('.json'):
            file_path += '.json'

        # Validate the directory
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            print(f"Directory {directory} does not exist. Please enter a valid path.")
        else:
            return file_path


def select_scans():
    print("Do you want a full DNS scan or a custom scan?")
    print("1: Full Scan")
    print("2: Custom Scan")
    print("3: Exit")
    
    while True:
        try:
            sel = int(input("Select (1 or 2 or 3): "))
            if sel in [1, 2]:
                break
            elif sel == 3:
                print("Results saved in Json File.")
                print("Thank you for using the DJSAI DNS enumeration tool.")
                print("Exiting...")
                exit()
            else:
                print("Invalid option. Please enter 1 or 2 or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if sel == 1:
        return list(dns_scans.values())
    elif sel == 2:
        print("Select DNS scan options:")
        for key, value in dns_scans.items():
            print(f"{key}: {value.__name__}")
        while True:
            try:
                choose = list(map(int, input("Enter your choices (space-separated numbers): ").split()))
                return [dns_scans[i] for i in choose if i in dns_scans]
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")
    elif sel == 3:
        print("Results saved in Json File.")
        print("Thank you for using the DJSAI DNS enumeration tool.")
        print("Exiting...")
        exit()
    else:
        print("Invalid input. Please enter 1 or 2 or 3.")

def write_to_json(output_data, file_path):
    # Append results to the specified JSON file
    try:
        with open(file_path, "r") as file:
            # Load existing data
            data = json.load(file)
    except FileNotFoundError:
        # File does not exist, start with an empty list
        data = []

    data.append(output_data)  # Append new result

    # Write updated data back to the file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    domain = get_domain()
    json_file = get_json_filename(domain)

    loop = True
    while loop:
        selected_scans = select_scans()
        if selected_scans:
            # Display selected scans and ask for confirmation
            print("\nSelected scans:")
            for i, scan in enumerate(selected_scans, 1):
                print(f"{i}: {scan.__name__}")
        
        confirm = input("\nDo you want to execute these scans? (y/n or any key to exit): ").lower().strip()
        if confirm == 'y':
            for scan in selected_scans:
                # Each scan returns a dictionary or list, append to JSON
                scan_result = scan(domain)
                write_to_json(scan_result, json_file)
                print(f"Scan completed: {scan.__name__}")
        else:
            print("Scan execution cancelled.")
            break

    print(f"Results saved in {json_file}.")
    print("Thank you for using the DJSAI DNS enumeration tool.")
