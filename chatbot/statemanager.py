import re
import json
import datetime
import random
from typing import Dict, List, Tuple, Any, Optional, Union

# Import our Knowledge Base
from knowledge_base import KnowledgeBase

class StateManager:
    """Manages conversation context and user session state"""
    
    def __init__(self):
        self.sessions = {}  # Dictionary to store session data for multiple users
    
    def create_session(self, user_id: str) -> None:
        """
        Initialize a new user session.

        Args:
            user_id (str): The unique identifier for the user whose session is being created.
        """
        self.sessions[user_id] = {
            "created_at": datetime.datetime.now(),
            "last_active": datetime.datetime.now(),
            "conversation_history": [],
            "current_context": None,
            "entity_memory": {},
            "preferences": {},
            "verification_level": "unknown",
            "last_intent": None,
            "flags": {
                "needs_human": False,
                "has_pending_query": False,
                "is_new_user": True
            },
            "active_flows": [],  # For multi-step processes like registration, verification, etc.
            "flow_states": {}    # State data for active flows
        }
    
    def get_session(self, user_id: str) -> Dict:
        """Get a user's session data, creating it if it doesn't exist"""
        if user_id not in self.sessions:
            self.create_session(user_id)
        
        # Update last active timestamp
        self.sessions[user_id]["last_active"] = datetime.datetime.now()
        return self.sessions[user_id]
    
    def update_conversation_history(self, user_id: str, user_message: str, bot_response: str) -> None:
        """Add a message exchange to the conversation history"""
        session = self.get_session(user_id)
        session["conversation_history"].append({
            "timestamp": datetime.datetime.now(),
            "user_message": user_message,
            "bot_response": bot_response
        })
        
        # Limit history size to prevent memory issues
        if len(session["conversation_history"]) > 20:
            session["conversation_history"] = session["conversation_history"][-20:]
    
    def set_context(self, user_id: str, context: str, data: Dict = None) -> None:
        """Set the current conversation context"""
        session = self.get_session(user_id)
        session["current_context"] = context
        
        # Store any context-specific data
        if data:
            if "context_data" not in session:
                session["context_data"] = {}
            session["context_data"][context] = data
    
    def get_context(self, user_id: str) -> str:
        """Get the current conversation context"""
        return self.get_session(user_id).get("current_context")
    
    def set_entity(self, user_id: str, entity_type: str, entity_value: Any) -> None:
        """Remember an entity mentioned by the user"""
        session = self.get_session(user_id)
        session["entity_memory"][entity_type] = entity_value
    
    def get_entity(self, user_id: str, entity_type: str) -> Any:
        """Retrieve a remembered entity"""
        return self.get_session(user_id).get("entity_memory", {}).get(entity_type)
    
    def set_flag(self, user_id: str, flag_name: str, value: bool) -> None:
        """Set a state flag"""
        session = self.get_session(user_id)
        session["flags"][flag_name] = value
    
    def get_flag(self, user_id: str, flag_name: str) -> bool:
        """Get a state flag value"""
        return self.get_session(user_id).get("flags", {}).get(flag_name, False)
    
    def set_preference(self, user_id: str, preference: str, value: Any) -> None:
        """Set a user preference"""
        session = self.get_session(user_id)
        session["preferences"][preference] = value
    
    def get_preference(self, user_id: str, preference: str, default: Any = None) -> Any:
        """Get a user preference"""
        return self.get_session(user_id).get("preferences", {}).get(preference, default)
    
    def start_flow(self, user_id: str, flow_name: str, initial_state: Dict = None) -> None:
        """Start a multi-step conversation flow"""
        session = self.get_session(user_id)
        if flow_name not in session["active_flows"]:
            session["active_flows"].append(flow_name)
        
        session["flow_states"][flow_name] = initial_state or {"step": 0}
        
        # Set current context to this flow
        self.set_context(user_id, flow_name)
    
    def update_flow_state(self, user_id: str, flow_name: str, state_updates: Dict) -> None:
        """Update the state of an active flow"""
        session = self.get_session(user_id)
        if flow_name in session["flow_states"]:
            session["flow_states"][flow_name].update(state_updates)
    
    def get_flow_state(self, user_id: str, flow_name: str) -> Dict:
        """Get the current state of an active flow"""
        return self.get_session(user_id).get("flow_states", {}).get(flow_name, {})
    
    def end_flow(self, user_id: str, flow_name: str) -> None:
        """End a multi-step conversation flow"""
        session = self.get_session(user_id)
        if flow_name in session["active_flows"]:
            session["active_flows"].remove(flow_name)
        
        if flow_name in session.get("flow_states", {}):
            del session["flow_states"][flow_name]
        
        # If this was the current context, reset it
        if self.get_context(user_id) == flow_name:
            self.set_context(user_id, None)
    
    def set_last_intent(self, user_id: str, intent: str) -> None:
        """Set the last detected user intent"""
        session = self.get_session(user_id)
        session["last_intent"] = intent
    
    def get_last_intent(self, user_id: str) -> str:
        """Get the last detected user intent"""
        return self.get_session(user_id).get("last_intent")
    
    def get_session_age(self, user_id: str) -> datetime.timedelta:
        """Get the age of the current session"""
        session = self.get_session(user_id)
        return datetime.datetime.now() - session["created_at"]
    
    def get_inactive_time(self, user_id: str) -> datetime.timedelta:
        """Get the time since the user was last active"""
        session = self.get_session(user_id)
        return datetime.datetime.now() - session["last_active"]
    
    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """Remove sessions older than the specified age"""
        current_time = datetime.datetime.now()
        old_sessions = []
        
        for user_id, session in self.sessions.items():
            if current_time - session["last_active"] > datetime.timedelta(hours=max_age_hours):
                old_sessions.append(user_id)
        
        for user_id in old_sessions:
            del self.sessions[user_id]
        
        return len(old_sessions)


class PatternMatcher:
    """Identifies patterns in user input to determine intent and extract entities"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.patterns = self._load_patterns()
        self.entity_extractors = self._load_entity_extractors()
    
    def _load_patterns(self) -> Dict[str, Dict]:
        """Load intent patterns - in real implementation, this could come from a file or database"""
        return {
            # General patterns
            "greeting": {
                "patterns": [
                    r"^(hi|hello|hey|greetings)[\s\.,!]*$",
                    r"^good (morning|afternoon|evening)[\s\.,!]*$"
                ],
                "priority": 1,
                "context_independent": True
            },
            "farewell": {
                "patterns": [
                    r"^(bye|goodbye|see you|farewell)[\s\.,!]*$",
                    r"^(talk to you later|thanks bye|thank you bye)[\s\.,!]*$"
                ],
                "priority": 1,
                "context_independent": True
            },
            "thanks": {
                "patterns": [
                    r"^(thanks|thank you|thx|ty)[\s\.,!]*$",
                    r"(appreciate|grateful)[\s\.,!]*$"
                ],
                "priority": 1,
                "context_independent": True
            },
            "help": {
                "patterns": [
                    r"^help[\s\.,!]*$",
                    r"^(i need|can i get) (some|) help[\s\.,!?]*$",
                    r"^what can you (do|help with|assist with)[\s\.,!?]*$"
                ],
                "priority": 2,
                "context_independent": True
            },
            "human_support": {
                "patterns": [
                    r"(speak|talk) (to|with) (a human|an agent|real person|support)",
                    r"(human|live|real) (support|agent|assistance)",
                    r"i want to talk to a person"
                ],
                "priority": 3,
                "context_independent": True
            },
            
            # Exchange Info patterns
            "trading_hours": {
                "patterns": [
                    r"(what are|tell me) (the|your) (trading hours|hours of operation)",
                    r"(when|what time) (is|are) (the exchange|you|trading) open",
                    r"(are you open|can i trade) (24\/7|all the time)",
                    r"(downtime|maintenance) (schedule|time|hours)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "exchange_info",
                "subcategory": "trading_hours"
            },
            "supported_crypto": {
                "patterns": [
                    r"(what|which) (cryptocurrencies|coins|tokens) (do you support|can i trade)",
                    r"(do you support|can i trade) ([a-zA-Z]+)",
                    r"(list of|all) (available|supported) (cryptocurrencies|coins)",
                    r"(trading pairs|markets) (available|supported|listed)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "exchange_info",
                "subcategory": "supported_cryptocurrencies"
            },
            "fees": {
                "patterns": [
                    r"(what are|tell me about) (the|your) (fees|fee structure)",
                    r"(trading|withdrawal|deposit) fees",
                    r"how much (does it cost|are the fees) (to|for) (trade|withdraw|deposit)",
                    r"(fee discounts|volume discounts|lower fees)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "exchange_info",
                "subcategory": "fee_structure"
            },
            "verification_info": {
                "patterns": [
                    r"(kyc|know your customer|identity verification) (requirements|process)",
                    r"(verification|account) (levels|tiers)",
                    r"(how to|steps to) (verify|get verified)",
                    r"(what are|tell me) (the|about) (verification|kyc) (requirements|steps)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "exchange_info", 
                "subcategory": "kyc_requirements"
            },
            
            # Account Management patterns
            "create_account": {
                "patterns": [
                    r"(how (do|can) i|steps to) (create|register|open) (an|a) account",
                    r"(sign up|registration) (process|steps)",
                    r"i want to (create|open) (an|a) account"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "account_management",
                "subcategory": "registration"
            },
            "account_security": {
                "patterns": [
                    r"(how (do|can) i|steps to) (secure|protect) my account",
                    r"(account|wallet) security (tips|measures|best practices)",
                    r"(2fa|two-factor authentication) (setup|enable)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "account_management",
                "subcategory": "security"
            },
            "reset_password": {
                "patterns": [
                    r"(how (do|can) i|steps to) (reset|change|recover) (my|the) password",
                    r"(forgot|lost|reset) (my|the) password",
                    r"(password recovery|password reset) (process|steps)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "account_management",
                "subcategory": "account_recovery",
                "topic": "forgotten_password"
            },
            
            # Trading patterns
            "how_to_trade": {
                "patterns": [
                    r"(how (do|can) i|steps to) (trade|buy|sell) (cryptocurrency|crypto|coins|bitcoin|eth)",
                    r"(how to|guide to) (place|execute) (a|an) (order|trade)",
                    r"(explain|tell me about) (limit|market|stop) orders"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "trading_info",
                "subcategory": "order_types"
            },
            "trading_terms": {
                "patterns": [
                    r"(what is|define|explain) (a|an) ([a-zA-Z\s]+) (in crypto|in trading)",
                    r"(explain|tell me about) ([a-zA-Z\s]+) (term|concept)",
                    r"(meaning of|definition of) ([a-zA-Z\s]+)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "trading_info",
                "subcategory": "market_terminology"
            },
            
            # Wallet operations patterns
            "deposit_info": {
                "patterns": [
                    r"(how (do|can) i|steps to) (deposit|send) (cryptocurrency|crypto|coins|bitcoin|eth)",
                    r"(deposit|send) (instructions|steps|process)",
                    r"(how long|time) (for|to) (deposit|transaction) (confirmation|to arrive)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "wallet_operations",
                "subcategory": "deposits"
            },
            "withdrawal_info": {
                "patterns": [
                    r"(how (do|can) i|steps to) (withdraw|send out) (cryptocurrency|crypto|coins|bitcoin|eth)",
                    r"(withdrawal|send out) (instructions|steps|process|fees)",
                    r"(how long|time) (for|to) (withdrawal|transaction) (processing|to complete)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "wallet_operations",
                "subcategory": "withdrawals"
            },
            
            # Support patterns
            "contact_support": {
                "patterns": [
                    r"(how (do|can) i|ways to) (contact|reach) (support|customer service)",
                    r"(support|help) (contact|email|phone|chat)",
                    r"(is there|do you have) (live|human) support"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "technical_support",
                "subcategory": "contact_methods"
            },
            "common_problem": {
                "patterns": [
                    r"(having|experience) (a|an) (problem|issue|trouble) with",
                    r"(not working|problem with|issue with) (login|deposit|withdrawal|trading)"
                ],
                "priority": 3,
                "context_independent": True,
                "category": "technical_support",
                "subcategory": "common_issues"
            },
            
            # Educational patterns
            "crypto_explanation": {
                "patterns": [
                    r"(what is|explain|tell me about) (cryptocurrency|blockchain|bitcoin|ethereum)",
                    r"(how (does|do)) (cryptocurrency|blockchain|bitcoin|ethereum) work",
                    r"(basics|fundamentals) of (crypto|cryptocurrency)"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "crypto_education",
                "subcategory": "cryptocurrency_basics"
            },
            "trading_education": {
                "patterns": [
                    r"(tips|advice|strategies) for (trading|investing)",
                    r"(how to|guide to) (analyze|read) (charts|markets)",
                    r"(explain|tell me about) (technical|fundamental) analysis"
                ],
                "priority": 2,
                "context_independent": True,
                "category": "crypto_education",
                "subcategory": "trading_education"
            }
        }
    
    def _load_entity_extractors(self) -> Dict[str, Dict]:
        """Load entity extractors - functions to extract entities from text"""
        return {
            "cryptocurrency": {
                "pattern": r"(bitcoin|btc|ethereum|eth|ripple|xrp|litecoin|ltc|solana|sol|cardano|ada|polkadot|dot|avalanche|avax|usdt|usdc|dai|busd)",
                "transform": lambda match: match.group(0).lower()
            },
            "verification_tier": {
                "pattern": r"(tier|level)\s*(\d+)",
                "transform": lambda match: f"tier{match.group(2)}"
            },
            "amount": {
                "pattern":                 git remote add origin <your-repository-url>
                "transform": lambda match: {
                    "value": float(match.group(1)),
                    "currency": match.group(2).lower()
                }
            },
            "time_period": {
                "pattern": r"(\d+)\s*(day|days|week|weeks|month|months|year|years|hour|hours|minute|minutes)",
                "transform": lambda match: {
                    "value": int(match.group(1)),
                    "unit": match.group(2).lower()
                }
            },
            "order_type": {
                "pattern": r"(market|limit|stop|stop-limit|oco|trailing stop)\s*order",
                "transform": lambda match: match.group(1).lower()
            }
        }
    
    def match_intent(self, user_input: str, current_context: str = None) -> Tuple[str, float]:
        """
        Match user input against patterns to determine intent
        
        Args:
            user_input: The user's message
            current_context: The current conversation context, if any
            
        Returns:
            Tuple of (intent_name, confidence_score)
        """
        user_input = user_input.lower().strip()
        matches = []
        
        # Check each intent pattern
        for intent_name, intent_data in self.patterns.items():
            # Skip context-dependent patterns if they don't match the current context
            if not intent_data.get("context_independent", False) and current_context != intent_name:
                continue
                
            # Try each pattern for this intent
            for pattern in intent_data["patterns"]:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    # Calculate a confidence score based on how much of the input was matched
                    match_length = match.end() - match.start()
                    coverage = match_length / len(user_input)
                    # Adjust by pattern priority
                    confidence = coverage * intent_data.get("priority", 1)
                    
                    matches.append((intent_name, confidence))
                    break  # Found a match for this intent, move to next intent
        
        if not matches:
            return ("unknown", 0.0)
            
        # Return the intent with highest confidence
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches[0]
    
    def extract_entities(self, user_input: str) -> Dict[str, Any]:
        """
        Extract entities from user input
        
        Args:
            user_input: The user's message
            
        Returns:
            Dictionary of entity_type -> entity_value
        """
        user_input = user_input.lower()
        entities = {}
        
        for entity_type, extractor in self.entity_extractors.items():
            matches = re.finditer(extractor["pattern"], user_input, re.IGNORECASE)
            
            for match in matches:
                # Transform the match using the entity-specific transform function
                value = extractor["transform"](match)
                
                # If we already have this entity type, make it a list
                if entity_type in entities:
                    if not isinstance(entities[entity_type], list):
                        entities[entity_type] = [entities[entity_type]]
                    entities[entity_type].append(value)
                else:
                    entities[entity_type] = value
        
        return entities
    
    def get_knowledge_base_info(self, intent: str) -> Dict:
        """Get relevant knowledge base information for an intent"""
        intent_data = self.patterns.get(intent, {})
        
        if "category" in intent_data:
            category = intent_data["category"]
            subcategory = intent_data.get("subcategory")
            topic = intent_data.get("topic")
            
            return {
                "category": category,
                "subcategory": subcategory,
                "topic": topic,
                "kb_data": self.kb.get_info(category, subcategory, topic)
            }
        
        return None


class ResponseGenerator:
    """Generates appropriate responses based on intent, entities, and context"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict:
        """Load response templates - in a real system, this could come from a file or database"""
        return {
            # General templates
            "greeting": [
                "Hello! Welcome to CryptoLocal Exchange. How can I assist you today?",
                "Hi there! I'm your CryptoLocal assistant. What can I help you with?",
                "Welcome to CryptoLocal! I'm here to help with all your crypto trading needs."
            ],
            "farewell": [
                "Thank you for chatting with CryptoLocal Exchange. Have a great day!",
                "Goodbye! Feel free to reach out if you have more questions.",
                "Thanks for using CryptoLocal. We look forward to serving you again soon."
            ],
            "thanks": [
                "You're welcome! Is there anything else I can help with?",
                "Happy to help! Let me know if you need assistance with anything else.",
                "My pleasure! If you have other questions, I'm here to help."
            ],
            "help": [
                "I can help with:\n- Information about our exchange\n- Account setup and security\n- Trading procedures\n- Deposits and withdrawals\n- Technical support\n- Cryptocurrency education\n\nWhat would you like to know more about?"
            ],
            "human_support": [
                "I'd be happy to connect you with our support team. You can reach them via live chat on our website during business hours (Monday-Friday, 9:00 AM-6:00 PM), or by email at support@cryptolocal.example. For urgent assistance, please use the live chat option."
            ],
            "unknown": [
                "I'm not sure I understand. Could you please rephrase your question?",
                "I don't have information on that. Could you try asking in a different way?",
                "I'm still learning and didn't quite catch that. Can you rephrase your question?"
            ],
            
            # Templates with dynamic content will be handled in get_response
        }
    
    def get_response(self, intent: str, entities: Dict, kb_info: Dict = None, context: str = None) -> str:
        """
        Generate a response based on intent, entities, knowledge base info, and context
        
        Args:
            intent: The identified user intent
            entities: Extracted entities from user input
            kb_info: Relevant knowledge base information
            context: Current conversation context
            
        Returns:
            Generated response text
        """
        # Check if we have a template for this intent
        if intent in self.templates:
            templates = self.templates[intent]
            # For simple templates, just return a random one
            if isinstance(templates, list) and all(isinstance(t, str) for t in templates):
                return random.choice(templates)
        
        # Handle dynamic responses based on intent
        if intent == "trading_hours":
            trading_hours = kb_info["kb_data"]["trading"]
            maintenance = kb_info["kb_data"]["maintenance"]
            return f"CryptoLocal Exchange is open for trading {trading_hours}. Our scheduled maintenance window is {maintenance}."
        
        elif intent == "supported_crypto":
            cryptos = kb_info["kb_data"]["major_cryptos"]
            stablecoins = kb_info["kb_data"]["stablecoins"]
            
            # If a specific cryptocurrency was mentioned, check if we support it
            if "cryptocurrency" in entities:
                crypto = entities["cryptocurrency"]
                if isinstance(crypto, list):
                    crypto = crypto[0]  # Just take the first one if multiple were mentioned
                
                # Check if it's in our supported list
                all_supported = cryptos + stablecoins
                if crypto.lower() in [c.lower() for c in all_supported]:
                    return f"Yes, we do support {crypto.upper()}! You can trade it on our exchange."
                else:
                    return f"I'm sorry, we don't currently support {crypto.upper()} on our exchange. We regularly add new cryptocurrencies, so please check back for updates."
            
            # Otherwise, give general information
            return f"CryptoLocal Exchange supports major cryptocurrencies including {', '.join(cryptos[:3])} and more. We also support stablecoins such as {', '.join(stablecoins[:2])}. Would you like to see the full list of supported cryptocurrencies?"
        
        elif intent == "fees":
            trading_fees = kb_info["kb_data"]["trading"]
            withdrawal = kb_info["kb_data"]["withdrawal"]
            
            # If the user asked about a specific fee type
            if "fee_type" in entities:
                fee_type = entities["fee_type"]
                if fee_type == "trading":
                    return f"Our trading fees are {trading_fees['maker']*100}% for maker orders and {trading_fees['taker']*100}% for taker orders. Volume discounts are available for high-volume traders."
                elif fee_type == "withdrawal":
                    # If they asked about a specific cryptocurrency's withdrawal fee
                    if "cryptocurrency" in entities:
                        crypto = entities["cryptocurrency"]
                        if isinstance(crypto, list):
                            crypto = crypto[0]
                        
                        if crypto.upper() in withdrawal:
                            fee = withdrawal[crypto.upper()]
                            return f"The withdrawal fee for {crypto.upper()} is {fee} {crypto.upper()}."
                        else:
                            return f"I don't have the specific withdrawal fee for {crypto.upper()}. Please check our fee schedule on the website or contact support."
                    else:
                        return "Our withdrawal fees vary by cryptocurrency. For example, BTC withdrawal fee is 0.0005 BTC. Would you like to know about a specific cryptocurrency's withdrawal fee?"
            
            # General fee information
            return "CryptoLocal Exchange offers competitive fees. Trading fees start at 0.1% maker / 0.15% taker with volume discounts available. Withdrawal fees vary by cryptocurrency. Would you like more specific information about a particular fee type?"
        
        elif intent == "verification_info":
            tiers = kb_info["kb_data"]
            
            # If they asked about a specific tier
            if "verification_tier" in entities:
                tier = entities["verification_tier"]
                if tier in tiers:
                    tier_info = tiers[tier]
                    requirements = ", ".join(tier_info["requirements"])
                    limits = tier_info["limits"]
                    return f"{tier.capitalize()} verification requires: {requirements}. With this level, your daily trading limit is ${limits['daily_trading']} and daily withdrawal limit is ${limits['daily_withdrawal']}."
                else:
                    return f"I don't have information about {tier}. Our verification levels include Tier 1 (Basic), Tier 2 (Verified), and Tier 3 (Enhanced)."
            
            # General verification information
            return "CryptoLocal Exchange has 3 verification tiers. Tier 1 (Basic) requires email and phone verification with a $2,000 daily limit. Tier 2 requires ID and proof of address with a $10,000 daily limit. Tier 3 adds a verification call with a $50,000 daily limit. Would you like more details about a specific tier?"
        
        # Handle other intents similarly...
        
        # For intents without specific handling or templates, use KB data directly with a generic template
        if kb_info and "kb_data" in kb_info:
            # Create a response based on KB data - this is simplified and would be more sophisticated in a real system
            if isinstance(kb_info["kb_data"], dict):
                keys = list(kb_info["kb_data"].keys())[:3]  # Just use first few keys to avoid overwhelming
                return f"Here's what I know about {intent.replace('_', ' ')}: " + ", ".join([f"{key}: {str(kb_info['kb_data'][key])[:50]}..." for key in keys])
            elif isinstance(kb_info["kb_data"], list):
                items = kb_info["kb_data"][:3]  # Just use first few items to avoid overwhelming
                return f"Here's what I know about {intent.replace('_', ' ')}: " + ", ".join([str(item) for item in items])
            else:
                return f"About {intent.replace('_', ' ')}: {str(kb_info['kb_data'])}"
        
        # Fallback response if no specific handling is available
        return "I understand you're asking about " + intent.replace("_", " ") + ". Let me look into that for you."
        
    def generate_flow_response(self, flow_name: str, flow_state: Dict) -> str:
        """Generate a response for an active conversation flow"""
        if flow_name == "account_registration":
            step = flow_state.get("step", 0)
            if step == 0:
                return "I'll help you create an account! First, could you provide your email address?"
            elif step == 1:
                return "Great! Now, please create a strong password. It should be at least 12 characters with letters, numbers, and special characters."
            elif step == 2:
                return "Now I'll need your full name