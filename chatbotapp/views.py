from django.shortcuts import redirect, render
from chatbotapp.models import ChatMessage
import google.generativeai as genai
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Настраиваем прокси
proxies = {
    "http": "http://104.223.103.111",
    "https": "http://104.223.103.111",
}

# Патчим requests внутри google.generativeai
class ProxyAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.proxies = kwargs.pop("proxies", None)
        super().__init__(*args, **kwargs)

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        if self.proxies:
            proxy = self.proxies.get("https" if "https://" in proxy else "http")
        return super().proxy_manager_for(proxy, **proxy_kwargs)

# Настраиваем прокси для Google API
session = requests.Session()
adapter = ProxyAdapter(proxies=proxies)
retry = Retry(total=3, backoff_factor=0.1)
adapter.max_retries = retry

session.mount("http://", adapter)
session.mount("https://", adapter)

# Патчим HTTP-запросы в библиотеке Google
genai._session = session

def send_message(request):
    if request.method == 'POST':
        genai.configure(api_key="AIzaSyBnbyKawS5nYQHcneOFPrrTkskx6suyljI")
        model = genai.GenerativeModel("gemini-2.0-flash-lite")

        user_message = request.POST.get('user_message')
        try:
            bot_response = model.generate_content(user_message)
            ChatMessage.objects.create(user_message=user_message, bot_response=bot_response.text)
        except Exception as e:
            ChatMessage.objects.create(user_message=user_message, bot_response=f"Error: {str(e)}")

    return redirect('chatbot:list_messages')

def list_messages(request):
    messages = ChatMessage.objects.all()
    return render(request, 'chatbot/list_messages.html', {'messages': messages})
