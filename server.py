import NKSERVER
import time

# Variables to which ID is occupied or not
id_1_occupied = False
id_2_occupied = False

# Positioning variables
p1_pos = '(100, 100)'
p2_pos = '(200, 200)'

# When false, the game is waiting for 2 people to connect
clients_ready = False

# Queue of players who have sent their position
queue = 0

# Ip adress and port of the server
ip = 'add your ip here'
port = 5555

# Start the server
serv = NKSERVER.server(ip, port)
print('Server Started')

# Listen for connections
serv.listen(2)

# Make a loop to connect both clients and establish an ID for each
while not clients_ready:
    # Accept our first connection and assign the address as player 1
    conn, addr = serv.server.accept()
    print('New connection @', addr)

    player_1 = NKSERVER.new_client(addr)
    p1_addr = player_1.addr

    # Now, wait to accept our second connection and assign the address as player 2
    conn2, addr2 = serv.server.accept()
    print('New connection @', addr2)

    player_2 = NKSERVER.new_client(addr2)
    p2_addr = player_2.addr

    print('Player 1:', p1_addr)
    print('Player 2', p2_addr)

    # Since both clients are ready, start the game
    serv.send_to('StartPosUpdate', p1_addr, conn)
    time.sleep(1)

    serv.send_to('StartPosUpdate', p2_addr, conn2)
    time.sleep(1)

    clients_ready = True


while clients_ready:
    recv1 = conn.recv(2048)
    recv_data1 = recv1.decode('utf-8')

    recv2 = conn2.recv(2048)
    recv_data2 = recv2.decode('utf-8')

    # Add "CheckStat" in case our client did not receive "StartPosUpdate"
    if recv_data1 == 'CheckStat':
        serv.send_to('StartPosUpdate', p1_addr, conn)

    # Check if a client has quit on their side and close the connection
    if recv_data1 == 'Quit':
        serv.send_to('QUIT', addr, conn)
        serv.send_to('QUIT', addr2, conn2)
        conn.close()
        conn2.close()
        clients_ready = False
        break

    # Once our clients are ready, deal with updating player positions
    if recv_data1 != 'CheckStat':
        if recv_data1 != 'ClientReqId':
            if recv_data1 != 'Quit':
                if clients_ready == True:
                    if queue < 2:
                        if addr == p1_addr:
                            p1_pos = str(recv_data1)
                            queue += 1

    '''
    Now, we check the if statements on our second client and see what client 2 requests.
    This makes sure both clients receive seperate requests if needed.
    '''


    # Add "CheckStat" in case our client did not receive "StartPosUpdate"
    if recv_data2 == 'CheckStat':
        serv.send_to('StartPosUpdate', addr2, conn2)

    # Check if a client has quit on their side and close the connection
    if recv_data2 == 'Quit':
        serv.send_to('QUIT', addr, conn)
        serv.send_to('QUIT', addr2, conn2)
        conn.close()
        conn2.close()
        clients_ready = False

    # Once our clients are ready, deal with updating player positions
    if recv_data2 != 'CheckStat':
        if recv_data2 != 'ClientReqId':
            if recv_data2 != 'Quit':
                if clients_ready == True:
                    if queue < 2:
                        if addr2 == p2_addr:
                            p2_pos = str(recv_data2)
                            queue += 1

    if queue == 2:
        serv.send_to(p1_pos, p2_addr, conn2)
        serv.send_to(p2_pos, p1_addr, conn)
        queue = 0

# Once all loops finish, confirm it with printing "SERVER CLOSED"
print('SERVER CLOSED')
