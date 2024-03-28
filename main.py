import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
# import requests
import httpx
from string import Template
# import json

controller = Controller()

message = "The weblink is not accessible!!!     Error: "

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {"model": "mistral:7b-instruct-v0.2-q4_K_S",
                 "keep_alive": "5m",
                 "stream": False
                 }

PROMPT_TEMPLATE = Template(
    """Fix all typos, casing, punctuations and grammatical errors in this text, but preserve all new line characters.
    
    $text

    Return only the corrected text. Don't return a preamble.
    """
)

def fix_text(text): 
    # return text[::-1] -> Returns the reverse string
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    # print(prompt)
    response = httpx.post(
        OLLAMA_ENDPOINT,
        json={"prompt":prompt, **OLLAMA_CONFIG},
        headers={"Content-Type":"application/json"},
        timeout=10)
    # response = requests.get("http://google.com")
    # print(response.status_code)
    # print(response.json())
    # print(response.json()['rcesponse'].strip())

    if response.status_code != 200:
        return message+str(response.status_code)
    
    # strip will remove any white spaces from the start or end of the response/string 
    return response.json()['response'].strip()

def fix_current_line():
    # Cmd + Shift + Left Arrow
    controller.press(Key.cmd)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.cmd)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection()

def fix_selection():

    # 1. Copy to the clipboard (Cmd+C)
    with controller.pressed(Key.cmd):
        # the press and release fucntions can be replaced by a utility function tap()
        # controller.press('c')
        # controller.release('c')
        controller.tap('c')

    # 2. Get text from clipboard
        # Add a delay of 0.1 secs to ensure operations are successful. We may not need it as well. Just in case.
        time.sleep(0.1) 
        text = pyperclip.paste()
        # print(text)

    # 3. Fix the typo in text using LLM
        if not text:
            return
        fixed_text = fix_text(text)
        # print(fixed_text)

        if fixed_text[:len(message)] == message:
            print(fixed_text)
        else:            
    # 4. Copy back to the clipboard
            pyperclip.copy(fixed_text)
            time.sleep(0.1) 

    # 5. Insert the text (Cmd+V)
            with controller.pressed(Key.cmd):
                controller.tap('v')

def on_f1():
    fix_current_line()

def on_f2():
    fix_selection()

# The following prints the values associated with keys f7 and f9
# from pynput.keyboard import Key 
# print(Key.f1.value, Key.f2.value)
# Key.f7.value = <98>
# Key.f9.value = <101>
# Key.f1.value = <122>
# Key.f2.value = <120>

with keyboard.GlobalHotKeys({
        '<122>': on_f1,
        '<120>': on_f2}) as h:
    h.join()