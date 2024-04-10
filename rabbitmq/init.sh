cat "$RABBITMQ_SSL_CERTFILE" "$RABBITMQ_SSL_KEYFILE" > /tmp/combined.pem
chmod 0400 /tmp/combined.pem
export ERL_SSL_PATH="$(erl -eval 'io:format("~p", [code:lib_dir(ssl, ebin)]),halt().' -noshell)"
export RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-pa '$ERL_SSL_PATH' -proto_dist inet_tls -ssl_dist_opt server_certfile /tmp/combined.pem -ssl_dist_opt server_secure_renegotiate true client_secure_renegotiate true"
export RABBITMQ_CTL_ERL_ARGS="$RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS"
rabbitmqctl list_users