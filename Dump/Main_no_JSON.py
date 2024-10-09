# Importing the necessary subtools
from SubTools.DNS_Record_Lookup import dns_lookup as dns_record_lookup
from SubTools.Brute_Force_Subdomain_Enumeration import brute_force_subdomains as subdomain_enumerator
from SubTools.Zone_Transfer import zone_transfer as zone_transfer
from SubTools.DNSSEC_Validation import validate_dnssec as dnssec_validation
from SubTools.Reverse_DNS_Lookup import reverse_dns_lookup_from_domain as reverse_dns

# ... existing imports ...

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
        print("Exiting...")
        exit()
    else:
        print("Invalid input. Please enter 1 or 2 or 3.")

if __name__ == "__main__":
    domain = get_domain()
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
                scan(domain)
                print("DNS scanning completed.")
        else:
            print("Scan execution cancelled.")

print("Thank you for using the DNS enumeration tool.")