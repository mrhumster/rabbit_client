# Пример конфигурации RabbitMQ TLS

## Сертификаты и ключи

Генерировал по [инструкции](https://www.rabbitmq.com/ssl.html#manual-certificate-generation) 

*Содержимое файла `.env`*
```
RABBITMQ_USERNAME=user
RABBITMQ_PASSWORD=user
RABBITMQ_USER_PERMISSIONS=.*\ .*\. .*\
RABBITMQ_SSL_CACERTFILE=/etc/ssl/certs/ca_certificate.pem
RABBITMQ_SSL_CERTFILE=/etc/ssl/certs/server_certificate.pem
RABBITMQ_SSL_KEYFILE=/etc/ssl/private_key.pem
RABBITMQ_MANAGEMENT_SSL_CACERTFILE=/etc/ssl/certs/ca_certificate.pem
RABBITMQ_MANAGEMENT_SSL_CERTFILE=/etc/ssl/certs/server_certificate.pem
RABBITMQ_MANAGEMENT_SSL_KEYFILE=/etc/ssl/private_key.pem
RABBITMQ_SSL_VERIFY=verify_none
RABBITMQ_SSL_FAIL_IF_NO_PEER_CERT=false
```

## Тестирование

1. Запуск `docker-compose up -d`

```
...
2023-07-06 04:44:36.155866+00:00 [info] <0.749.0> started TCP listener on [::]:5672
2023-07-06T04:44:36.158535344Z 2023-07-06 04:44:36.158299+00:00 [info] <0.769.0> started TLS (SSL) listener on [::]:5671
...

```

2. Приемник `python receive.py`

```
/home/omra/PycharmProjects/rabbit_client/venv/bin/python /home/omra/PycharmProjects/rabbit_client/receive.py 
 [*] Waiting for messages. To exit press CTRL+C
```

3. Отправитель `python send.py`

```
/home/omra/PycharmProjects/rabbit_client/venv/bin/python /home/omra/PycharmProjects/rabbit_client/send.py 
 [x] Sent 'Hello World!'
```

4. Результат

```
/home/omra/PycharmProjects/rabbit_client/venv/bin/python /home/omra/PycharmProjects/rabbit_client/receive.py 
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received b'Hello World!'
```

```
2023-07-06 04:57:34.890650+00:00 [info] <0.954.0> accepting AMQP connection <0.954.0> (192.168.224.1:35886 -> 192.168.224.2:5671)
2023-07-06T04:57:34.894180967Z 2023-07-06 04:57:34.893529+00:00 [info] <0.954.0> connection <0.954.0> (192.168.224.1:35886 -> 192.168.224.2:5671): user 'user' authenticated and granted access to vhost '/'
2023-07-06T04:57:34.897128504Z 2023-07-06 04:57:34.896635+00:00 [info] <0.954.0> closing AMQP connection <0.954.0> (192.168.224.1:35886 -> 192.168.224.2:5671, vhost: '/', user: 'user')
```

## Проблемы

* managment plugin не заработал. 

*WEB ERROR*
```
Этот сайт не может обеспечить безопасное соединение.
Ваш сертификат отклонен сайтом omra-laptop или не был выдан.
Обратитесь за помощью к системному администратору.
ERR_BAD_SSL_CLIENT_AUTH_CERT
```

*RABBITMQ LOG*
```
2023-07-06 05:01:33.525838+00:00 [notice] <0.999.0> TLS server: In state wait_cert at tls_handshake_1_3.erl:443 generated SERVER ALERT: Fatal - Certificate required
2023-07-06T05:01:33.526670138Z 2023-07-06 05:01:33.525838+00:00 [notice] <0.999.0>  - certificate_required
```

*Тестирование соединения через openssl*
```
omra@omra-laptop:~/PycharmProjects/rabbit_client$ openssl s_client -connect localhost:5671 -cert client/client_certificate.pem -key client/private_key.pem -CAfile testca/ca_certificate.pem
CONNECTED(00000003)
Can't use SSL_get_servername
depth=1 CN = XOMRKOB_CA
verify return:1
depth=0 CN = omra-laptop, O = server
verify return:1
---
Certificate chain
 0 s:CN = omra-laptop, O = server
   i:CN = XOMRKOB_CA
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Jul  5 17:04:34 2023 GMT; NotAfter: Jul  4 17:04:34 2024 GMT
 1 s:CN = XOMRKOB_CA
   i:CN = XOMRKOB_CA
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Jul  5 17:01:40 2023 GMT; NotAfter: Jul  4 17:01:40 2024 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDJjCCAg6gAwIBAgIBATANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDDApYT01S
S09CX0NBMB4XDTIzMDcwNTE3MDQzNFoXDTI0MDcwNDE3MDQzNFowJzEUMBIGA1UE
AwwLb21yYS1sYXB0b3AxDzANBgNVBAoMBnNlcnZlcjCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBANL5GcI4O+611rr2Q94MmKrTBP7/iDkGkQJ8LEPMEHyP
PKif7++RvlYaHkRDNgPNMf3/c92seBiLZtL+omUOV/AGlY92KNrOYbc2PWJn26A7
OwXJIobJ+8TPxJT5uYS8wxE6RYbNfCP+gnbu6zjiGmv+QHWz9l8T96zBHSG3jNZS
OjWXSklh9fP9N9hkxWIOmuNc01AoQ5SIqftQxnHnFAf6DoySIQX7D+hxm9BYFEYL
PwxAiVFT18kdOopGbVuxOgJfuIq3YZdsMFa11GsF9ZcLDRfUfEs6dulCFQwqE2w2
3vq15FEVj92schLz2vdEwfZ6UxZlF4/EqQx5F0ccpJUCAwEAAaNvMG0wCQYDVR0T
BAIwADALBgNVHQ8EBAMCBaAwEwYDVR0lBAwwCgYIKwYBBQUHAwEwHQYDVR0OBBYE
FKBU0t0qq5a5y4vEXmtfHP5iPtWiMB8GA1UdIwQYMBaAFLZu8VJffOfj42ObIwd1
ltZj/GLqMA0GCSqGSIb3DQEBCwUAA4IBAQBvCbRljnGyKf7/Fif4OSStBhJFOSh6
NVsbD9CaxO5iUZzA6qWkK5+LqC41lHeG7uDKlFLu/wulbUo5Rbp1k0514Tnjk81/
GqMjOKaqcywjqzgeiQfMEUAQV22IJD+ppZK8NN0dFgwrUtvv/gk5Lew5Q/NYYzGg
NUy0nPL5I4/JOvn2ZwGq2GCpGkPmnySCj0kD+GBUX7gjTjuVpZul0L6iEHi/iFg/
e9pZP+rtGSxOxIP4u7URbqPt2AaJrlNtdoKsI48HKxwq26h1/kJPH6bxFBbRoXkt
Gn0TD9Il1+ZZDHv9dut2WHKlzYM4dreSgDp1/6cgLNrOXfqM3TSG+7cA
-----END CERTIFICATE-----
subject=CN = omra-laptop, O = server
issuer=CN = XOMRKOB_CA
---
No client certificate CA names sent
Peer signing digest: SHA256
Peer signature type: RSA-PSS
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 2131 bytes and written 373 bytes
Verification: OK
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Server public key is 2048 bit
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 0 (ok)
---
closed

```