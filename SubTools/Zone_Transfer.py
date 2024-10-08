import dns.query
import dns.zone
import dns.resolver

def get_nameservers(domain):
    """Retrieve the nameservers for the given domain."""
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        return [str(ns.target).strip('.') for ns in ns_records]
    except Exception as e:
        print(f"Failed to retrieve nameservers: {e}")
        return []

def attempt_zone_transfer(domain, nameserver):
    """Attempt zone transfer (AXFR) for the domain from the given nameserver."""
    try:
        # Attempt zone transfer
        zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
        names = zone.nodes.keys()
        print(f"Zone transfer successful on {nameserver}")
        for name in names:
            print(zone[name].to_text(name))
    except Exception as e:
        print(f"Zone transfer failed on {nameserver}: {e}")
def zone_transfer(domain):
    nameservers = get_nameservers(domain)
    if not nameservers:
        print(f"No nameservers found for {domain}.")
    else:
        print(f"Nameservers for {domain}: {nameservers}")
        # Attempt zone transfer on each nameserver
        for ns in nameservers:
            print(f"\nAttempting zone transfer on nameserver: {ns}")
            attempt_zone_transfer(domain, ns)
if __name__ == "__main__":
    domain = input("Enter the domain: ")
    zone_transfer(domain)