import dns.resolver
import dns.reversename

print('====')
answers = dns.resolver.resolve('google.com', 'SOA')
print('query qname:', answers.qname, ' num ans.', len(answers))
for rdata in answers:
    print(' serial: %s  tech: %s' % (rdata.serial, rdata.rname))
    print(' refresh: %s  retry: %s' % (rdata.refresh, rdata.retry))
    print(' expire: %s  minimum: %s' % (rdata.expire, rdata.minimum))
    print(' mname: %s' % (rdata.mname))

domain_address = dns.reversename.from_address('8.8.4.4')
print(domain_address)
domain_name = str(dns.resolver.resolve(domain_address,"PTR")[0])
print(domain_name)
# TXT records
answers = dns.resolver.resolve('google.com', 'TXT')
print(' query qname:', answers.qname, ' num ans.', len(answers))
for rdata in answers:
    for txt_string in rdata.strings:
      print(' TXT:', txt_string)
print('====')