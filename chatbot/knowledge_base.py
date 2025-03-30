class KnowledgeBase:
    def __init__(self):
        self.exchange_info = self._load_exchange_info()
        self.account_management = self._load_account_management()
        self.trading_info = self._load_trading_info()
        self.wallet_operations = self._load_wallet_operations()
        self.technical_support = self._load_technical_support()
        self.crypto_education = self._load_crypto_education()
        
    def _load_exchange_info(self):
        return {
            "trading_hours": {
                "trading": "24/7, 365 days a year",
                "maintenance": "Every Tuesday, 3:00-4:00 AM GMT +2",
                "support_hours": "Monday-Friday, 9:00 AM-6:00 PM",
                "emergency_support": "24/7 for security-related issues"
            },
            "supported_cryptocurrencies": {
                "major_cryptos": ["BTC", "ETH", "XRP", "LTC", "SOL", "ADA", "DOT", "AVAX"],
                "stablecoins": ["USDT", "USDC", "DAI", "BUSD"],
                "fiat_pairs": ["USD/BTC", "USD/ETH", "USD/USDT", "EUR/BTC", "EUR/ETH", "GBP/BTC"],
                "popular_pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BTC/ETH"]
            },
            "fee_structure": {
                "trading": {
                    "maker": 0.001,  # 0.1%
                    "taker": 0.0015,  # 0.15%
                    "volume_discounts": {
                        "100000": {"maker": 0.0008, "taker": 0.0012},
                        "500000": {"maker": 0.0006, "taker": 0.001},
                        "1000000": {"maker": 0.0004, "taker": 0.0008},
                        "5000000": {"maker": 0.0002, "taker": 0.0005}
                    },
                    "new_user_discount": "50% trading fee discount for first 30 days"
                },
                "withdrawal": {
                    "BTC": 0.0005,
                    "ETH": 0.005,
                    "XRP": 0.1,
                    "LTC": 0.01,
                    "SOL": 0.01,
                    "ADA": 1.0,
                    "DOT": 0.1,
                    "AVAX": 0.01,
                    "USDT": 2.0,
                    "USDC": 2.0,
                    "DAI": 2.0,
                    "BUSD": 0.5
                },
                "deposit": {
                    "crypto": "Free",
                    "fiat": "1% of deposit amount"
                }
            },
            "kyc_requirements": {
                "tier1": {
                    "requirements": ["Email verification", "Phone verification", "Name", "Date of Birth"],
                    "limits": {"daily_trading": 2000, "daily_withdrawal": 1000}
                },
                "tier2": {
                    "requirements": ["Tier 1 requirements", "Government ID", "Proof of address"],
                    "limits": {"daily_trading": 10000, "daily_withdrawal": 5000}
                },
                "tier3": {
                    "requirements": ["Tier 2 requirements", "Video verification call"],
                    "limits": {"daily_trading": 50000, "daily_withdrawal": 25000}
                },
                "corporate": {
                    "requirements": ["Company registration documents", "Director IDs", "Proof of address", "Ownership structure"],
                    "limits": {"daily_trading": 200000, "daily_withdrawal": 100000}
                }
            },
            "company_info": {
                "name": "Aster Exchange",
                "jurisdiction": "Lagos, Nigeria",
                "founded": "2018",
                "registration_number": "CRY123456789",
                "license_type": "Virtual Currency Business License",
                "security": {
                    "cold_storage": "95% of funds",
                    "audits": "Quarterly by SecureBlock Auditors",
                    "insurance": "$5 million insurance fund for security incidents"
                },
                "compliance": {
                    "aml_policy": "https://asterex.example/legal/aml",
                    "privacy_policy": "https://asterex.example/legal/privacy",
                    "terms_of_service": "https://asterex.example/legal/terms"
                }
            }
        }
    
    def _load_account_management(self):
        return {
            "registration": {
                "steps": [
                    "Visit asterex.example/register",
                    "Enter email and create password",
                    "Verify email via confirmation link",
                    "Set up 2FA (Google Authenticator or SMS)",
                    "Complete basic profile information"
                ],
                "requirements": {
                    "password": "Minimum 12 characters, with letters, numbers, and special characters",
                    "email": "Valid email address required",
                    "location": "Service not available in restricted jurisdictions"
                }
            },
            "security": {
                "2fa_options": ["Google Authenticator", "SMS verification", "Email verification"],
                "login_protection": "IP tracking, unusual activity detection, email alerts",
                "api_keys": {
                    "creation": "Available after Tier 2 verification",
                    "permissions": ["Read-only", "Trading", "Withdrawal"],
                    "management": "https://asterex.example/account/api"
                }
            },
            "account_recovery": {
                "forgotten_password": [
                    "Click 'Forgot Password' on login page",
                    "Enter registered email",
                    "Follow instructions in recovery email",
                    "Set new password",
                    "Re-verify 2FA"
                ],
                "lost_2fa": [
                    "Contact support with ID verification",
                    "Complete security questionnaire",
                    "Wait for 24-hour security hold",
                    "Set up new 2FA device"
                ]
            },
            "verification_levels": {
                "upgrade_process": "Upload required documents through Account > Verification section",
                "processing_time": "1-3 business days for Tier 2, 3-5 business days for Tier 3",
                "rejection_reasons": [
                    "Blurry or incomplete documents",
                    "Information mismatch",
                    "Expired documents",
                    "Unsupported jurisdiction"
                ]
            }
        }
    
    def _load_trading_info(self):
        return {
            "order_types": {
                "market": {
                    "description": "Execute immediately at current market price",
                    "pros": ["Immediate execution", "Guaranteed to be filled"],
                    "cons": ["No price guarantee", "May experience slippage"]
                },
                "limit": {
                    "description": "Set specific price for buy/sell",
                    "pros": ["Price control", "Lower fees (maker)"],
                    "cons": ["No guarantee of execution", "May miss fast-moving markets"]
                },
                "stop_limit": {
                    "description": "Trigger a limit order when price reaches stop price",
                    "pros": ["Automated risk management", "Precise exit strategy"],
                    "cons": ["Complex to set up", "May not trigger in volatile markets"]
                }
            },
            "chart_analysis": {
                "available_indicators": ["Moving Averages", "RSI", "MACD", "Bollinger Bands", "Volume"],
                "timeframes": ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"],
                "drawing_tools": ["Trend lines", "Fibonacci retracement", "Support/resistance", "Channels"]
            },
            "trading_pairs": {
                "quote_currencies": ["BTC", "ETH", "USDT", "USD"],
                "minimum_orders": {
                    "BTC": 0.0001,
                    "ETH": 0.001,
                    "XRP": 10,
                    "LTC": 0.1,
                    "USDT": 10
                },
                "price_precision": {
                    "BTC": 2,  # Decimal places for price display
                    "ETH": 2,
                    "XRP": 5,
                    "LTC": 2,
                    "SOL": 2
                }
            },
            "market_terminology": {
                "bull_market": "Upward-trending market with rising prices",
                "bear_market": "Downward-trending market with falling prices",
                "resistance": "Price level where selling pressure may overcome buying pressure",
                "support": "Price level where buying pressure may overcome selling pressure",
                "volume": "Amount of assets traded during a specific period",
                "market_cap": "Total value of all coins (price x circulating supply)",
                "liquidity": "Ability to buy/sell without causing significant price change"
            }
        }
    
    def _load_wallet_operations(self):
        return {
            "deposits": {
                "crypto": {
                    "process": [
                        "Go to Wallet > Deposit",
                        "Select cryptocurrency",
                        "Copy deposit address or scan QR code",
                        "Send funds from external wallet to displayed address",
                        "Wait for blockchain confirmations"
                    ],
                    "confirmations_required": {
                        "BTC": 3,
                        "ETH": 15,
                        "XRP": 1,
                        "LTC": 6,
                        "SOL": 32,
                        "ADA": 20,
                        "DOT": 20,
                        "AVAX": 20,
                        "USDT": 15,
                        "USDC": 15
                    },
                    "expected_time": {
                        "BTC": "10-60 minutes",
                        "ETH": "5-10 minutes",
                        "XRP": "1-2 minutes",
                        "LTC": "10-30 minutes"
                    }
                },
                "fiat": {
                    "methods": ["Bank transfer", "Credit/debit card", "Digital wallets"],
                    "processing_time": {
                        "Bank transfer": "1-3 business days",
                        "Credit/debit card": "Instant to 24 hours",
                        "Digital wallets": "Usually instant"
                    },
                    "limits": {
                        "Bank transfer": {"min": 100, "max": 50000},
                        "Credit/debit card": {"min": 20, "max": 5000},
                        "Digital wallets": {"min": 20, "max": 2000}
                    }
                }
            },
            "withdrawals": {
                "crypto": {
                    "process": [
                        "Go to Wallet > Withdraw",
                        "Select cryptocurrency",
                        "Enter recipient address (double-check)",
                        "Enter amount",
                        "Confirm with 2FA",
                        "Wait for processing and blockchain confirmation"
                    ],
                    "withdrawal_times": {
                        "processing": "Up to 12 hours",
                        "blockchain": "Depends on network congestion and fees paid"
                    },
                    "networks": {
                        "ETH": ["Ethereum (ERC-20)", "Polygon", "Arbitrum"],
                        "USDT": ["Ethereum (ERC-20)", "Tron (TRC-20)", "Solana"],
                        "BTC": ["Bitcoin"]
                    }
                },
                "fiat": {
                    "methods": ["Bank transfer", "Digital wallets"],
                    "processing_time": {
                        "Bank transfer": "1-5 business days",
                        "Digital wallets": "1-2 business days"
                    },
                    "limits": {
                        "Bank transfer": {"min": 100, "max": "Based on verification level"},
                        "Digital wallets": {"min": 20, "max": 2000}
                    },
                    "fees": {
                        "fiat": {
                            "bank_transfer": "1% of withdrawal amount",
                            "digital_wallets": "0.5% of withdrawal amount"
                        },
                        "crypto": {
                            "BTC": 0.0005,
                            "ETH": 0.005,
                            "XRP": 0.1,
                            "LTC": 0.01
                        }
                    },
                    "requirements": "Fiat withdrawal requires Tier 2 verification"
                }
            },
            "wallet_security": {
                "best_practices": [
                    "Enable all security features (2FA, email alerts, etc.)",
                    "Use whitelisted withdrawal addresses",
                    "Set withdrawal limits",
                    "Regularly check login history",
                    "Don't share account details"
                ],
                "address_whitelist": {
                    "setup": "Account > Security > Whitelist Management",
                    "approval_time": "24-hour waiting period for new addresses",
                    "limit": "Maximum of 10 whitelisted addresses per cryptocurrency"
                }
            },
            "network_fees": {
                "explanation": "Blockchain transaction fees paid to miners/validators",
                "fee_types": {
                    "BTC": "Satoshis per byte, based on network congestion",
                    "ETH": "Gas fees, based on network congestion and operation complexity",
                    "SOL": "Fixed low fees regardless of congestion"
                },
                "fee_estimation": "Platform automatically sets optimal fees for timely confirmation",
                "custom_fees": "Available for BTC and ETH withdrawals in advanced mode"
            }
        }
    
    def _load_technical_support(self):
        return {
            "contact_methods": {
                "live_chat": {
                    "availability": "Monday-Friday, 9:00 AM-6:00 PM",
                    "response_time": "Usually within 5 minutes",
                    "access": "Via website or mobile app"
                },
                "email": {
                    "address": "support@asterex.example",
                    "response_time": "Within 24 hours",
                    "recommended_for": "Detailed issues requiring investigation"
                },
                "ticket_system": {
                    "access": "Account > Support > New Ticket",
                    "response_time": "Within 24-48 hours",
                    "tracking": "Track status in Account > Support > My Tickets"
                },
                "phone": {
                    "availability": "For security-related emergencies only",
                    "access": "Available to Tier 3 verified users"
                }
            },
            "common_issues": {
                "login_problems": [
                    "Check correct email and password",
                    "Ensure 2FA device is synced with correct time",
                    "Try clearing browser cache or using private browsing",
                    "Check if account is locked due to multiple failed attempts"
                ],
                "deposit_issues": [
                    "Verify correct deposit address",
                    "Check if minimum deposit amount was met",
                    "Confirm transaction has required confirmations on blockchain",
                    "Ensure deposited asset is supported"
                ],
                "withdrawal_issues": [
                    "Verify sufficient balance (including fees)",
                    "Check withdrawal address format",
                    "Confirm 2FA is working properly",
                    "Verify withdrawal limits haven't been reached"
                ],
                "trading_issues": [
                    "Check for sufficient trading balance",
                    "Verify minimum order size is met",
                    "Check for any trading restrictions on account",
                    "Confirm price is within reasonable range of market price"
                ]
            },
            "escalation_process": {
                "initial_support": "First response from Level 1 support team",
                "escalation_criteria": "Issue unresolved after 48 hours or complex technical problems",
                "priority_cases": "Account security, missing funds, verification urgent for large transfers",
                "management_review": "Available by request for unresolved issues >5 days old"
            },
            "system_status": {
                "status_page": "status.asterex.example",
                "notifications": "Email and app push notifications for major outages",
                "scheduled_maintenance": "Announced at least 24 hours in advance",
                "historical_incidents": "Viewable on status page for past 30 days"
            }
        }
    
    def _load_crypto_education(self):
        return {
            "cryptocurrency_basics": {
                "blockchain": "Distributed ledger technology that records all transactions",
                "private_keys": "Secret codes that allow spending of cryptocurrency",
                "public_keys": "Addresses derived from private keys for receiving funds",
                "consensus_mechanisms": {
                    "proof_of_work": "Used by Bitcoin, miners solve complex puzzles",
                    "proof_of_stake": "Used by Ethereum 2.0, validators stake coins"
                },
                "wallets": {
                    "hot_wallets": "Connected to internet, convenient but less secure",
                    "cold_storage": "Offline storage, more secure for large amounts",
                    "types": ["Hardware wallets", "Paper wallets", "Mobile wallets", "Desktop wallets"]
                }
            },
            "crypto_assets": {
                "bitcoin": "First cryptocurrency, store of value, limited supply of 21 million",
                "ethereum": "Smart contract platform enabling dApps and DeFi",
                "stablecoins": "Cryptocurrencies designed to maintain stable value, usually pegged to USD",
                "altcoins": "Alternative cryptocurrencies besides Bitcoin",
                "tokens": "Assets built on existing blockchains like Ethereum"
            },
            "trading_education": {
                "analysis_types": {
                    "fundamental": "Evaluating project utility, team, tokenomics",
                    "technical": "Using charts and indicators to identify patterns"
                },
                "risk_management": {
                    "portfolio_diversification": "Spreading investments across multiple assets",
                    "position_sizing": "Limiting amount invested in any single trade",
                    "stop_losses": "Setting automatic sell orders to limit potential losses"
                },
                "trading_psychology": [
                    "Emotional control during market volatility",
                    "Avoiding FOMO (Fear Of Missing Out)",
                    "Setting realistic expectations",
                    "Developing and sticking to a trading plan"
                ]
            },
            "security_best_practices": {
                "personal_security": [
                    "Use unique passwords for each platform",
                    "Enable 2FA on all accounts",
                    "Be wary of phishing attempts",
                    "Don't share screen during trading",
                    "Use secure networks"
                ],
                "common_scams": {
                    "phishing": "Fake websites or emails that steal login information",
                    "giveaway_scams": "Promises of free cryptocurrency for sending coins first",
                    "pump_and_dump": "Artificial inflation of coin prices followed by mass selling",
                    "fake_ICOs": "Fraudulent initial coin offerings with no real product"
                }
            },
            "tax_implications": {
                "disclaimer": "General guidance only, consult tax professional",
                "taxable_events": [
                    "Selling cryptocurrency for fiat",
                    "Trading one cryptocurrency for another",
                    "Using cryptocurrency to purchase goods/services",
                    "Mining or staking rewards"
                ],
                "record_keeping": "Importance of maintaining detailed transaction records",
                "tax_tools": ["CryptoTax", "TokenTax", "CoinTracker", "Koinly"]
            }
        }
        