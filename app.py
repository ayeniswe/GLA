from plugins.transformer.sip_transformer import SipTransformer

s = SipTransformer()
r = s._transform("172 1275930743.699 r r REGISTER-1 sip:example.com 198.51.100.10:5060:udp 198.51.100.1:5060:udp sip:example.com sip:alice@example.com;tag=76yhh f81-d4-f6@example.com - - c-tr-1")
print(r)