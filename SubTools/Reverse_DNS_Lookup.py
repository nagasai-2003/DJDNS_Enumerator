import dns.resolver
import dns.reversename

def resolve_domain_to_ip(domain):
    try:
        # Resolve the domain to an IPv4 address (A record)
        answers = dns.resolver.resolve(domain, 'A')
        ip_address = answers[0].to_text()  # Take the first IP in the list
        return ip_address
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
    except Exception as e:
        print(f"Error resolving domain {domain}: {e}")

def reverse_dns_lookup_from_domain(domain):
    ip_address = resolve_domain_to_ip(domain)
    if ip_address:
        try:
            # Convert the IP address into the reverse DNS query format (PTR record)
            reverse_name = dns.reversename.from_address(ip_address)
            
            # Query the PTR record for the IP address
            domain_name = dns.resolver.resolve(reverse_name, "PTR")[0].to_text()
            
            print(f"The domain name for IP {ip_address} is: {domain_name}")
            
        except dns.resolver.NXDOMAIN:
            print(f"No PTR record found for IP {ip_address}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    reverse_dns_lookup_from_domain("quickplay.com")