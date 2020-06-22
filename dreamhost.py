import uuid, requests

#--------------------------------
# Start of config
API_Key = ""
domain = ""
check_ipv6 = False
# End of config
# -------------------------------

domain_records = []
domain_ip = None
rec_type = 'A'

# Get the current public IP address of the user
if check_ipv6:
    ipv6_addr = requests.get('http://api6.ipify.org').content.decode('UTF-8')
ip = requests.get('http://api.ipify.org').content.decode('UTF-8')


def dreamhost_command(command):
    return(requests.get('https://api.dreamhost.com/?key={}&cmd={}&unique_id={}'.format(API_Key, command, uuid.uuid4())).content.decode('UTF-8'))

# Get the DNS records for the given domain
body = dreamhost_command('dns-list_records')

# Format the DNS records into individual lines
for i in body.splitlines():
    if domain in i:
        domain_records.append(i.expandtabs().split())
print('All relevant DNS Records for {}: \n {}'.format(domain, body))


if check_ipv6:
    rec_type = 'AAAA'

# Find the IP address of the remote server
for i in domain_records:
    if (i[2] == domain and i[3] == rec_type):
        print('Found a type {} record for {} at: {}'.format(rec_type, domain, i[4]))
        domain_ip = i[4]
    else:
        print('No type {} record found for {}'.format(rec_type, domain))

# Updates the DNS records for the domain if the two addresses (domain_ip and ip) are different
if (domain_ip != ip):
    if (domain_ip == None):
        dreamhost_command('dns-add_record&record={}&type={}&value={}'.format(domain, rec_type, domain_ip))
        print('Added a type {} record for {} ip {}'.format(rec_type, domain, domain_ip))
    else:
        dreamhost_command('dns-remove_record&record={}&type={}&value={}'.format(domain, rec_type, domain_ip))
        print('Removed a type {} record for {} ip {}'.format(rec_type, domain, domain_ip))
        dreamhost_command('dns-add_record&record={}&type={}&value={}'.format(domain, rec_type, domain_ip))
        print('Added a type {} record for {} ip {}'.format(rec_type, domain, domain_ip))
else:
    print('Current ip ({}) and server ip ({}) match, no action necessary'.format(ip, domain_ip))
