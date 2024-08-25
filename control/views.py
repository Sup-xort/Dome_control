from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
from .camera import gen_frames  # 방금 작성한 gen_frames 함수를 가져옵니다
from django.contrib import messages
import serial.tools.list_ports

import serial
import time

port = None
connected = False

def connect(request):
    global port
    global connected

    if request.method == 'POST':
        selected_port = request.POST.get('port')
        available_ports = [p.device for p in serial.tools.list_ports.comports()]

        if selected_port in available_ports:
            try:
                port = serial.Serial(selected_port, 9600)
                connected = True
                messages.success(request, f"Connected to {selected_port} successfully.")
            except serial.SerialException as e:
                messages.error(request, f"Failed to connect to {selected_port}: {e}")
        else:
            messages.warning(request, f"Port {selected_port} is not available.")

    return redirect('home')

def disconnect(request):
    global port
    global connected

    if connected:
        port.close()
        connected = False
        port = None
        messages.success(request, "Disconnected successfully.")
    else:
        messages.warning(request, "Already disconnected")

    return redirect('home')

def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
def home(request):
    f = open('./state.txt', 'r')
    p, s = map(int, f.readline().strip())

    available_ports = serial.tools.list_ports.comports()

    context = {
        'p': 'ON' if p == 1 else 'OFF',
        'o': 'OPEN' if s == 1 else 'CLOSED',
        'available_ports': available_ports,
        'tf': connected
    }
    return render(request, 'control/home.html', context)

def dopen(request):
    global port
    global connected

    if connected:
        f = open('./state.txt', 'r')
        p, s = map(int, f.readline().strip())
        f.close()

        port.flushInput()  # 입력 버퍼 비우기
        port.flushOutput()  # 출력 버퍼 비우기

        if p == 0:
            port.write(b'p')
            time.sleep(0.1)
            port.write(b'o')
        elif s == 0:
            port.write(b'o')


        f = open('./state.txt', 'w')
        f.write('11')
        f.close()
    else:
        messages.warning(request, f"Not connected")

    return redirect('home')


def close(request):

    if connected:
        f = open('./state.txt', 'r')
        p, s = map(int, f.readline().strip())
        f.close()

        port.flushInput()  # 입력 버퍼 비우기
        port.flushOutput()  # 출력 버퍼 비우기

        if p == 0:
            port.write(b'p')
            p = 1
            time.sleep(0.1)
            port.write(b'c')
        elif s == 1:
            port.write(b'c')

        f = open('./state.txt', 'w')
        f.write(f'{p}0')
        f.close()
    else:
        messages.warning(request, f"Not connected")

    return redirect('home')


def power(request):
    if connected:
        f = open('./state.txt', 'r')
        p, s = map(int, f.readline().strip())
        f.close()

        port.flushInput()  # 입력 버퍼 비우기
        port.flushOutput()  # 출력 버퍼 비우기

        port.write('p'.encode())  # 'p' 명령어 전송
        time.sleep(0.1)  # 데이터 전송 후 잠시 대기

        p = 1 - p

        f = open('./state.txt', 'w')
        f.write(f'{p}{s}')
        f.close()
    else:
        messages.warning(request, f"Not connected")

    return redirect('home')
