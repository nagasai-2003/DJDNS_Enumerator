import dns.resolver
import dns.dnssec
import dns.name
import dns.message
import dns.query

def validate_dnssec(domain):
    try:
        # Resolve the domain's DNSKEY record (this is the public key)
        dnskey_response = dns.resolver.resolve(domain, 'DNSKEY')
        
        # Get the DNS response for A records (or any other records)
        a_response = dns.resolver.resolve(domain, 'A')

        # Extract DNSSEC signature (RRSIG record) for the A record
        rrsig_response = dns.resolver.resolve(domain, 'RRSIG')
        
        # Validate the DNSSEC signature
        dns.dnssec.validate(a_response.rrset, rrsig_response.rrset, {dns.name.from_text(domain): dnskey_response.rrset})
        
        print(f"DNSSEC is properly configured for {domain} and the records are valid.")
        
    except dns.resolver.NoAnswer:
        print(f"DNSSEC records not found for {domain}")
    except dns.dnssec.ValidationFailure:
        print(f"DNSSEC validation failed for {domain}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example:
if __name__ == "__main__":
    validate_dnssec("example.com")