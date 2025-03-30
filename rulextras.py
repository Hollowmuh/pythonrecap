def get_info(self, category, subcategory=None, topic=None, subtopic=None):
        """
        Retrieve information from the knowledge base.
        
        Args:
            category (str): Main category (e.g., 'exchange_info', 'account_management')
            subcategory (str, optional): Subcategory within main category
            topic (str, optional): Specific topic within subcategory
            subtopic (str, optional): Specific subtopic within topic
            
        Returns:
            dict or str: Requested information
        """
        if not hasattr(self, category):
            return f"Category '{category}' not found in knowledge base."
            
        data = getattr(self, category)
        
        if subcategory is None:
            return data
            
        if subcategory not in data:
            return f"Subcategory '{subcategory}' not found in {category}."
            
        result = data[subcategory]
        
        if topic is not None:
            if topic not in result:
                return f"Topic '{topic}' not found in {category}.{subcategory}."
            result = result[topic]
            
            if subtopic is not None:
                if subtopic not in result:
                    return f"Subtopic '{subtopic}' not found in {category}.{subcategory}.{topic}."
                result = result[subtopic]
                
        return result
        
    def search(self, query):
        """
        Simple search function to find information across all categories.
        
        Args:
            query (str): Search term
            
        Returns:
            list: List of matches with their paths
        """
        query = query.lower()
        results = []
        
        def search_recursive(data, path=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_path = f"{path}.{key}" if path else key
                    
                    # Check if key matches
                    if query in key.lower():
                        results.append({
                            "path": new_path,
                            "value": value
                        })
                    
                    # Recurse into nested structures
                    search_recursive(value, new_path)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    new_path = f"{path}[{i}]"
                    
                    # Check if string item matches
                    if isinstance(item, str) and query in item.lower():
                        results.append({
                            "path": new_path,
                            "value": item
                        })
                    
                    # Recurse into nested structures
                    if isinstance(item, (dict, list)):
                        search_recursive(item, new_path)
            elif isinstance(data, str) and query in data.lower():
                results.append({
                    "path": path,
                    "value": data
                })
                
        # Search each main category
        for category in ["exchange_info", "account_management", "trading_info", 
                        "wallet_operations", "technical_support", "crypto_education"]:
            search_recursive(getattr(self, category), category)
            
        return results

# Example usage
if __name__ == "__main__":
    kb = KnowledgeBase()
    
    # Example 1: Get information about trading fees
    print("=== Trading Fees ===")
    trading_fees = kb.get_info("exchange_info", "fee_structure", "trading")
    print(trading_fees)
    print()
    
    # Example 2: Get information about Bitcoin deposit confirmations
    print("=== BTC Deposit Confirmations ===")
    btc_confirms = kb.get_info("wallet_operations", "deposits", "crypto", "confirmations_required")["BTC"]
    print(f"Bitcoin requires {btc_confirms} confirmations")
    print()
    
    # Example 3: Search for information about "2FA"
    print("=== Search Results for '2FA' ===")
    results = kb.search("2FA")
    for i, result in enumerate(results[:3]):  # Show first 3 results
        print(f"Result {i+1}: {result['path']}")
    print(f"Total results: {len(results)}")