# AI powered typing assistant with Ollama

What did I do here?
    1. Installed required Python libraries like
        a. pynput -> to capture the keys pressed on the keyboard.
        b. pyperclip -> to perform copy and paste operation to and fom the clipboard.
        c. string teamplate -> to store the prompt template for a LLM (here Ollama -> mistral:7b-instruct-v0.2-q4_K_S)
        d. httpx -> to request the localhost to generate and respond the output of the LLM.
    2. Identified the #'s associated with the desired keys.
    3. Upon pressing the expected keys, the LLM model is triggered for a predefined prompt and a response is received, which is then replaces the original input.

Reference: https://www.youtube.com/watch?v=IUTFrexghsQ&t=1076s 

NOTE: I have followed the above reference video diligently, but the script does through errors at times, but works perfectly fine the other time, without any changes. It seems like happening because of unavalability of Ollama localhost at times.
