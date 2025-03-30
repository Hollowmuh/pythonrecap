import nltk
import re
from nltk.chat.util import Chat, reflections
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Define a set of patterns and responses
pairs = [
    [r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']],
    [r'how are you?', ['I am fine, thank you!', 'Doing well, how about you?']],
    [r'what is your name?', ['I am a chatbot created to assist you.', 'You can call me Chatbot.']],
    [r'what can you do?', ['I can chat with you, answer questions, and provide information.']],
    [r'help', ['How can I assist you?', 'What do you need help with?']],
    [r'bye|exit|quit', ['Goodbye!', 'See you later!', 'Take care!']],
    [r'(.*) your name?', ['My name is Chatbot.']],
    [r'(.*) (location|city) ?', ['I am based in the digital world.']],
    [r'(.*) created you?', ['I was created by a team of developers.']],
    [r'(.*) (weather|temperature) ?', ['I am not sure about the weather, but you can check online.']],    
    [r"(.*)", ["I'm sorry, I didn't understand that. Could you rephrase?", "Could you please elaborate?"]],
    [r"tell me a joke", ["Why don't skeletons fight each other? They don't have the guts!"]],
    [r"what is cryptocurrency|what are cryptos", 
        ["Cryptocurrency is a digital or virtual currency that uses cryptography for security and is decentralized, meaning it isn't controlled by any government or institution.",
         "Cryptocurrencies are digital assets that use cryptography for security and are decentralized, meaning they aren't controlled by any central authority."]],
    [r"how does crypto work|how cryptocurrency works", 
        ["Cryptocurrency works through a technology called blockchain, which is a public ledger that records all transactions. It's maintained by a network of computers worldwide rather than a central authority.",
         "Cryptocurrencies work using blockchain technology, which creates a secure, transparent record of all transactions across a network of computers."]],

    [r"what is blockchain|what are blockchains", 
        ["A blockchain is a digital ledger that records transactions across a network of computers. It's the underlying technology that enables cryptocurrencies to work in a secure and transparent way.",
         "Blockchain is a decentralized, digital ledger that records transactions across many computers in a way that's secure and transparent."]],
    [r"how to register|sign up|create account", 
        ["To register, go to our website and click 'Sign Up'. Enter your email and create a strong password. You'll receive a verification email to confirm your account.",
         "Account creation requires a valid email address and password. Make sure to use a strong, unique password and enable 2FA for security."]],

    [r"how to verify|kyc process|identity verification", 
        ["Verification (KYC) requires government-issued ID and proof of address. This is a security measure required by law to prevent fraud.",
         "The KYC process typically involves uploading clear photos of your ID and proof of address. Processing usually takes 1-3 business days."]],

    [r"forgot password|reset password|password recovery", 
        ["Use the 'Forgot Password' option on the login page. Make sure you have access to your recovery email.",
         "Click 'Forgot Password' and follow the email instructions. Never share your recovery information with anyone."]],
    [r"how to buy crypto|how to purchase cryptocurrency", 
        ["To buy cryptocurrency, deposit your local currency, select the crypto you want to buy, and place a market or limit order.",
         "First deposit your local currency, then use the trading interface to select your desired cryptocurrency and amount."]],

    [r"how to sell crypto|how to cash out", 
        ["To sell cryptocurrency, select the crypto you want to sell, choose your local currency, and place a sell order.",
         "Ensure you have sufficient balance before selling. Transaction processing times vary by currency."]],

    [r"what is trading|what is trading crypto", 
        ["Trading involves exchanging one cryptocurrency for another or for traditional currency. It's similar to foreign exchange markets but operates 24/7.",
         "Cryptocurrency trading is the act of exchanging one digital currency for another or for traditional currency."]],
    [r"how to secure account|account security", 
        ["Enable 2FA, use strong passwords, and never share your private keys or seed phrases. Monitor your account regularly.",
         "Keep your private keys offline, use hardware wallets for large amounts, and enable all available security features."]],

    [r"what is 2fa|two factor authentication", 
        ["Two-factor authentication adds an extra layer of security. Use authenticator apps instead of SMS when possible.",
         "2FA requires both your password and a second form of verification, like an authenticator app or email code."]],

    [r"account hacked|funds stolen|security breach", 
        ["IMMEDIATE ACTION REQUIRED: Contact support immediately, change all passwords, and enable 2FA if not already active.",
         "SECURITY ALERT: Freeze your accounts and contact support right away. Do not attempt to trade."]],
    [r"(.*\?$)", 
        ["I'm not sure about that. Could you please provide more details?",
         "I didn't quite understand. Could you rephrase your question?"]],

    [r"(.*)", 
        ["I'm sorry, I didn't understand that. Could you rephrase?",
         "Could you please elaborate?"]]
]

class RuleBasedChatbot:
    def __init__(self):
        self.chatbot = Chat(pairs, reflections)

    def respond(self, message):
        return self.chatbot.respond(message)
    
    def chat_with_bot(self):
        print("Hello, I am your chatbot! Type 'exit' to end the conversation.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Chatbot: Goodbye! Have a nice day!")
                break
            response = self.respond(user_input)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    chatbot = RuleBasedChatbot()
    chatbot.chat_with_bot()

