import dns.resolver
import dns.reversename

def dns_lookup(domain_or_ip):
    try:
        print(f"DNS Lookup for {domain_or_ip}:")

        # A and AAAA Records (IPv4 and IPv6 addresses)
        for rtype in ['A', 'AAAA']:
            try:
                answers = dns.resolver.resolve(domain_or_ip, rtype)
                print(f"\n{rtype} Records:")
                for answer in answers:
                    print(answer)
            except dns.resolver.NoAnswer:
                print(f"No {rtype} records found.")

        # MX Records (Mail Servers)
        try:
            answers = dns.resolver.resolve(domain_or_ip, 'MX')
            print("\nMX Records:")
            for answer in answers:
                print(f"Mail Server: {answer.exchange}, Priority: {answer.preference}")
        except dns.resolver.NoAnswer:
            print("No MX records found.")

        # NS Records (Nameservers)
        try:
            answers = dns.resolver.resolve(domain_or_ip, 'NS')
            print("\nNS Records:")
            for answer in answers:
                print(f"Nameserver: {answer.target}")
        except dns.resolver.NoAnswer:
            print("No NS records found.")

        # SOA Record (Start of Authority)
        try:
            answer = dns.resolver.resolve(domain_or_ip, 'SOA')
            print("\nSOA Record:")
            for data in answer:
                print(f"Primary NS: {data.mname}, Admin Email: {data.rname}")
        except dns.resolver.NoAnswer:
            print("No SOA records found.")

        # CNAME Records (Canonical Name)
        try:
            answers = dns.resolver.resolve(domain_or_ip, 'CNAME')
            print("\nCNAME Records:")
            for answer in answers:
                print(f"Alias: {answer.target}")
        except dns.resolver.NoAnswer:
            print("No CNAME records found.")

        # TXT Records (Text Records)
        try:
            answers = dns.resolver.resolve(domain_or_ip, 'TXT')
            print("\nTXT Records:")
            for answer in answers:
                print(f"TXT Record: {answer}")
        except dns.resolver.NoAnswer:
            print("No TXT records found.")

        # SRV Records (Service Records)
        try:
            answers = dns.resolver.resolve(domain_or_ip, 'SRV')
            print("\nSRV Records:")
            for answer in answers:
                print(f"Service: {answer.target}, Port: {answer.port}, Priority: {answer.priority}")
        except dns.resolver.NoAnswer:
            print("No SRV records found.")

        # PTR Record (Reverse DNS Lookup)
        try:
            reverse_name = dns.reversename.from_address(domain_or_ip)
            answer = dns.resolver.resolve(reverse_name, 'PTR')
            print("\nPTR Record (Reverse DNS):")
            for data in answer:
                print(f"PTR Record: {data}")
        except dns.exception.DNSException:
            print("No PTR records found or invalid IP for reverse lookup.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage:
dns_lookup("apsfl.in")  # Or you can pass an IP for PTR lookups
