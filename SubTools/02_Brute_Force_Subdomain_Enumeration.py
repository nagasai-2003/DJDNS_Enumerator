import dns.resolver
import concurrent.futures

# Function to resolve a single subdomain
def resolve_subdomain(subdomain, domain):
    full_domain = f"{subdomain}.{domain}"
    try:
        answers = dns.resolver.resolve(full_domain, 'A', lifetime=2)  # Timeout set to 2 seconds
        return full_domain, [rdata.to_text() for rdata in answers]
    except dns.resolver.NXDOMAIN:
        return None
    except dns.resolver.Timeout:
        return None
    except Exception as e:
        print(f"Error resolving {full_domain}: {e}")
        return None

# Brute-force function with multithreading
def brute_force_subdomains(domain):
    print("Choose a wordlist for brute forcing subdomains")
    print("1. Top 5000 Subdomains")
    print("2. Top 20000 Subdomains")
    print("3. Top 110000 Subdomains")
    print("4. Custom Wordlist")
    choice = input("Enter the number of the wordlist to use: ")

    if choice == '1':
        wordlist_path = "Resources/Subdomain_Lists/Top_5000.txt"
    elif choice == '2':
        wordlist_path = "Resources/Subdomain_Lists/Top_20000.txt"
    elif choice == '3':
        wordlist_path = "Resources/Subdomain_Lists/Top_110000.txt"
    else:
        wordlist_path = input("Enter the path to your custom wordlist: ")

    # Read the subdomain wordlist
    with open(wordlist_path, 'r') as wordlist:
        subdomains = [line.strip() for line in wordlist]

    # Multithreading: resolve subdomains in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_subdomain = {executor.submit(resolve_subdomain, sub, domain): sub for sub in subdomains}

        for future in concurrent.futures.as_completed(future_to_subdomain):
            result = future.result()
            if result:
                full_domain, ip_addresses = result
                print(f"Found subdomain: {full_domain}")
                for ip in ip_addresses:
                    print(f"IP Address: {ip}")

# Usage:
brute_force_subdomains("Quickplay.com")
