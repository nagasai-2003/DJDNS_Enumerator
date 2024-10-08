# Importing the necessary subtools
from SubTools.Brute_Force_Subdomain_Enumeration import brute_force_subdomains as subdomain_enumerator
from SubTools.Zone_Transfer import zone_transfer as zone_transfer
from SubTools.DNSSEC_Validation import validate_dnssec as dnssec_validation
from SubTools.Reverse_DNS_Lookup import reverse_dns_lookup_from_domain as reverse_dns

# ... existing imports ...

# Dictionary that maps user input to the specific DNS scan functions
dns_scans = {
    1: subdomain_enumerator,
    2: zone_transfer,
    3: dnssec_validation,
    4: reverse_dns
}

# Dictionary that maps user input to the specific DNS scan functions
dns_scans = {
    1: subdomain_enumerator,
    2: zone_transfer,
    3: dnssec_validation,
    4: reverse_dns
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
    
    while True:
        try:
            sel = int(input("Select (1 or 2): "))
            if sel in [1, 2]:
                break
            print("Invalid option. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if sel == 1:
        return list(dns_scans.values())
    else:
        print("Select DNS scan options:")
        for key, value in dns_scans.items():
            print(f"{key}: {value.__name__}")
        while True:
            try:
                choose = list(map(int, input("Enter your choices (space-separated numbers): ").split()))
                return [dns_scans[i] for i in choose if i in dns_scans]
            except ValueError:
                print("Invalid input. Please enter numbers separated by spaces.")

if __name__ == "__main__":
    domain = get_domain()
    
    loop = True
    while loop:
        selected_scans = select_scans()

        # Display selected scans and ask for confirmation
        print("\nSelected scans:")
        for i, scan in enumerate(selected_scans, 1):
            print(f"{i}: {scan.__name__}")
        
        confirm = input("\nDo you want to execute these scans? (y/n): ").lower().strip()
        if confirm == 'y':
            for scan in selected_scans:
                scan(domain)
            print("DNS scanning completed.")
        else:
            print("Scan execution cancelled.")

        # ... existing code for asking to scan again ...

print("Thank you for using the DNS enumeration tool.")