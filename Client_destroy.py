

def client_destroy(*clients):
    for client in clients:
        client.destroy()
