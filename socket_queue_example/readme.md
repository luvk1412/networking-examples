We try to see the socket/accept/listen queue size on the server. These are different names for same queue

When an incoming request come to a server, request first go to a syn queue and then when an ack is received from client the request goes to a accept queue
We are trying to see if we can see the size of this accept queue.

Below command wil run in linux only as i couldnt find any command to measure size of accept queue on mac.
You can bring up linux using docker
```
docker run -d --name p310 python:3.10-alpine3.18 tail -f /dev/null
```

Enter the container using
```
docker exec -it p310 /bin/sh
```

Open the socket in container using
```
python socket.py
```

Now you can establish connection using
```
nc localhost 12345
```

and can observe Read-Q size using
```
ss -tnl
```

install ss using "apk add ss"

We can also observe that even though if cancel nc comand the count of Read-Q doesnt decrease