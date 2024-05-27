from dotenv import load_dotenv
from termcolor import colored
from openai import OpenAI, AsyncOpenAI
import time
import json

load_dotenv()

class GPT_calls:
    def __init__(self,
                 name = "GPT chat",
                 model = "gpt-3.5-turbo",
                 max_history_words = 10000,
                 max_words_per_message = None,
                 json_mode = False,
                 stream = True,
                 use_async = False,
                 max_retry = 10):
        
        self.name = name
        self.model = model
        self.history = []
        self.max_history_words = max_history_words
        self.max_words_per_message = max_words_per_message
        self.json_mode = json_mode
        self.stream = stream
        self.use_async = use_async
        self.max_retry = max_retry


        print(colored(f"{self.name} initialized with json_mode = {json_mode}, stream = {stream}, use_async = {use_async}, max_history_words = {max_history_words}, max_words_per_message = {max_words_per_message}", "red"))
        

        if use_async:
            self.client = AsyncOpenAI()
        if not use_async:
            self. client = OpenAI()

    def add_message(self, role, content):
        if role == "user" and self.max_words_per_message:
            self.history.append({"role": role, "content": str(content)
                                  + f"please use {self.max_words_per_message} words or less"})
        elif role == "user" and self.max_words_per_message is None:
            self.history.append({"role": role, "content": str(content)})
        else:
            self.history.append({"role": role, "content": str(content)})

    def print_history_length(self):
        history_length = [len(str(message["content"]).split()) for message in self.history]
        print("\n")
        print(f"current history length is {sum(history_length)} words")

    def clear_history(self):
        #clear everything except systm message if it exists
        if len(self.history) > 1:
            self.history = self.history[:1]
        else:
            self.history.clear()

    def chat(self, question, **kwargs):
        self.add_message("user", question)
        return self.get_response_generator(**kwargs)
    
    def trim_history(self):
        words_count = sum(len(str(message["content"]).split()) for message in self.history if message ["role"] != "system")
        while words_count > self.max_history_words and len(self.history) > 1:
            self.history.pop(1) # Remove 2nd msg cuz 1st is always system msg
            
    def get_response_generator(self, color = "green", should_print = True, **kwargs):
        retries = 0
        while retries < self.max_retry:
            try:
                response = self.client.chat.completions.create(
                    model = self.model,
                    messages= self.history,
                    stream = True if self.stream else False,
                    **kwargs
                )

                if self.stream:
                    for chunk in response:
                        if chunk.choices[0].delta.content:
                            text_chunk = chunk.choices[0].delta.content
                            print(colored(text_chunk, color), end = "", flush = True)
                            yield text_chunk

                else:
                    assistant_response = response.choices[0].message.content
                    self.add_message("assistant", str(assistant_response))
                    self.trim_history()
                    yield assistant_response
                break
            except Exception as e:
                print(f"Error: {e}")
                retries = retries + 1
                time.sleep(1)
                continue