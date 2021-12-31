#--------------------------------
#boot.py
#--------------------------------
try:
  import usocket as socket
except:
  import socket
  
from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'ESP32_Team'
password = '123456789'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

a=Pin(15,Pin.OUT)
b=Pin(2,Pin.OUT)
c=Pin(4,Pin.OUT)
d=Pin(5,Pin.OUT)
e=Pin(18,Pin.OUT)
f=Pin(19,Pin.OUT)
g=Pin(21,Pin.OUT)

#--------------------------------
#main.py
#--------------------------------
from machine import Pin , Timer
from time import sleep
def zerodisplay():
    a.value(1)
    b.value(1)
    c.value(1)
    d.value(1)
    e.value(1)
    f.value(1)
    g.value(0)
def onedisplay():
    a.value(0)
    b.value(1)
    c.value(1)
    d.value(0)
    e.value(0)
    f.value(0)
    g.value(0)
def twodisplay():
    a.value(1)
    b.value(1)
    c.value(0)
    d.value(1)
    e.value(1)
    f.value(0)
    g.value(1)
def threedisplay():
    a.value(1)
    b.value(1)
    c.value(1)
    d.value(1)
    e.value(0)
    f.value(0)
    g.value(1)
def fourdisplay():
    a.value(0)
    b.value(1)
    c.value(1)
    d.value(0)
    e.value(0)
    f.value(1)
    g.value(1)
def fivedisplay():
    a.value(1)
    b.value(0)
    c.value(1)
    d.value(1)
    e.value(0)
    f.value(1)
    g.value(1)
def sixdisplay():
    a.value(1)
    b.value(0)
    c.value(1)
    d.value(1)
    e.value(1)
    f.value(1)
    g.value(1)
def sevendisplay():
    a.value(1)
    b.value(1)
    c.value(1)
    d.value(0)
    e.value(0)
    f.value(0)
    g.value(0)
def eightdisplay():
    a.value(1)
    b.value(1)
    c.value(1)
    d.value(1)
    e.value(1)
    f.value(1)
    g.value(1)
def ninedisplay():
    a.value(1)
    b.value(1)
    c.value(1)
    d.value(1)
    e.value(0)
    f.value(1)
    g.value(1)

def button(m):
    sleep(0.25)
    global n
    if m == 0:
        zerodisplay()
    elif m == 1:
        onedisplay()
    elif m == 2:
        twodisplay()
    elif m == 3:
        threedisplay()
    elif m == 4:
        fourdisplay()
    elif m == 5:
        fivedisplay()
    elif m == 6:
        sixdisplay()
    elif m == 7:
        sevendisplay()
    elif m == 8:
        eightdisplay()
    elif m == 9:
        ninedisplay()
    print('m',m)  
def increment(Button11):
        global m,n
        print('m,n',m,n)
        if m==9:
            m= 0
            button(m)
        else:
            m += 1 
            button(m)
        n=m-1 
def decrement(Button22):
        global m,n
        print('n',n)
        if m==0:
            m = 9
            n=m-1
            button(m)
        else:
            m=n
            n -= 1
            button(m) 
def reset(Button33):
  global m,n
  zerodisplay()
  n, m = 9, 0
def debounce(pin):
  timer.init(mode=Timer.ONE_SHOT, period=200 , callback = increment)
  
def debounce1(pin):
  timer.init(mode=Timer.ONE_SHOT, period=200 , callback = decrement)  
  
def debounce2(pin):
  timer.init(mode=Timer.ONE_SHOT, period=200 , callback = reset)      


#--------------------------------
#main loop
#--------------------------------
n, m = 9, -1
button1 = Pin(34,Pin.IN)
button2 = Pin(35,Pin.IN)
button3 = Pin(32,Pin.IN)
a=Pin(15,Pin.OUT)
b=Pin(2,Pin.OUT)
c=Pin(4,Pin.OUT)
d=Pin(5,Pin.OUT)
e=Pin(18,Pin.OUT)
f=Pin(19,Pin.OUT)
g=Pin(21,Pin.OUT)
a.value(0)
b.value(0)
c.value(0)
d.value(0)
e.value(0)
f.value(0)
g.value(0)
timer = Timer(0)
#--------------------------------
#interrupt
#--------------------------------
button1.irq(trigger = Pin.IRQ_FALLING , handler = debounce)
button2.irq(trigger = Pin.IRQ_FALLING , handler = debounce1)
button3.irq(trigger = Pin.IRQ_FALLING , handler = debounce2)
#--------------------------------
#web server & mobile app
#--------------------------------
def web_page():  
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #e7bd3b;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>Number is : <strong>""" + str(m) + """</strong></p><p><a href="/?Button1=inc"><button class="button">INC</button></a></p>
  <p><a href="/?Button2=dec"><button class="button button2">DEC</button></a></p>
  <p><a href="/?Button3=res"><button class="button button3">RES</button></a></p></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  Button1 = request.find('/?Button1=inc')
  Button2 = request.find('/?Button2=dec')
  Button3 = request.find('/?Button3=res')
  if Button1 == 6:
        print('inc')
        increment(m)
  if Button2 == 6:
        print('DEC')
        decrement(m)
  if Button3 == 6:
         print('RES')
         reset(m)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

