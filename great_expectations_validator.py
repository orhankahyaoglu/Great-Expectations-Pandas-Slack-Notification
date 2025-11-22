# great_expectations_validator.py
import pandas as pd
import great_expectations as ge
from great_expectations.dataset import PandasDataset
import requests
import json
from datetime import datetime
import os

class GreatExpectationsValidator:
    def __init__(self, csv_file_path, slack_webhook_url=None):
        self.csv_file_path = csv_file_path
        self.slack_webhook_url = slack_webhook_url
        self.df = None
        self.dataset = None
        
    def load_data(self):
        """Load and inspect the dataset"""
        try:
            self.df = pd.read_csv(self.csv_file_path)
            # PandasDataset'a dönüştür
            self.dataset = PandasDataset(self.df)
            print("✅ Dataset loaded successfully!")
            print(f"📊 Dataset shape: {self.df.shape}")
            print("\n📋 Dataset columns:")
            print(self.df.columns.tolist())
            print("\n🔍 First 5 rows:")
            print(self.df.head())
            return True
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    
    def create_and_run_expectations(self):
        """Create and run expectations directly"""
        try:
            print("🎯 Creating and running expectations...")
            
            # 1. order_id must not be null
            result1 = self.dataset.expect_column_values_to_not_be_null("order_id")
            print(f"1. order_id not null: {'✅ PASS' if result1.success else '❌ FAIL'}")
            
            # 2. order_id must be unique
            result2 = self.dataset.expect_column_values_to_be_unique("order_id")
            print(f"2. order_id unique: {'✅ PASS' if result2.success else '❌ FAIL'}")
            
            # 3. qty ≥ 0
            result3 = self.dataset.expect_column_values_to_be_between("qty", min_value=0)
            print(f"3. qty ≥ 0: {'✅ PASS' if result3.success else '❌ FAIL'}")
            
            # 4. amount ≥ 0
            result4 = self.dataset.expect_column_values_to_be_between("amount", min_value=0)
            print(f"4. amount ≥ 0: {'✅ PASS' if result4.success else '❌ FAIL'}")
            
            # 5. status must be inside an allowed set
            allowed_statuses = ["delivered", "shipped", "processing", "cancelled"]
            result5 = self.dataset.expect_column_values_to_be_in_set("status", allowed_statuses)
            print(f"5. status in allowed set: {'✅ PASS' if result5.success else '❌ FAIL'}")
            
            # Tüm sonuçları topla
            results = {
                'success': all([result1.success, result2.success, result3.success, 
                              result4.success, result5.success]),
                'results': [result1, result2, result3, result4, result5],
                'statistics': {
                    'total_expectations': 5,
                    'successful_expectations': sum([result1.success, result2.success, 
                                                   result3.success, result4.success, result5.success]),
                    'failed_expectations': 5 - sum([result1.success, result2.success, 
                                                  result3.success, result4.success, result5.success])
                }
            }
            
            return results
            
        except Exception as e:
            print(f"❌ Error running expectations: {e}")
            return None
    
    def send_slack_notification(self, validation_results):
        """Send Slack notification with validation results"""
        if not self.slack_webhook_url:
            print("⚠️  No Slack webhook URL provided. Skipping notification.")
            return
        
        try:
            stats = validation_results['statistics']
            success = validation_results['success']
            
            # Create Slack message
            color = "#36a64f" if success else "#ff0000"
            status_icon = "✅" if success else "❌"
            
            message = {
                "attachments": [
                    {
                        "color": color,
                        "title": f"{status_icon} Great Expectations Validation Report",
                        "fields": [
                            {
                                "title": "Overall Status",
                                "value": "SUCCESS" if success else "FAILED",
                                "short": True
                            },
                            {
                                "title": "Total Expectations",
                                "value": str(stats['total_expectations']),
                                "short": True
                            },
                            {
                                "title": "Passed",
                                "value": str(stats['successful_expectations']),
                                "short": True
                            },
                            {
                                "title": "Failed",
                                "value": str(stats['failed_expectations']),
                                "short": True
                            }
                        ],
                        "ts": datetime.now().timestamp()
                    }
                ]
            }
            
            # Add failed expectations details
            failed_expectations = []
            unexpected_values = {}
            
            for i, result in enumerate(validation_results['results']):
                if not result.success:
                    expectation_name = result.expectation_config.expectation_type
                    failed_expectations.append(f"{i+1}. {expectation_name}")
                    
                    # Collect unexpected values
                    if hasattr(result, 'result') and 'unexpected_count' in result.result:
                        unexpected_count = result.result.get('unexpected_count', 0)
                        if unexpected_count > 0:
                            col_name = result.expectation_config.kwargs.get('column', 'unknown')
                            unexpected_values[col_name] = unexpected_count
            
            if failed_expectations:
                failed_details = "\n".join(failed_expectations)
                message["attachments"][0]["fields"].append({
                    "title": "Failed Expectations",
                    "value": failed_details,
                    "short": False
                })
            
            if unexpected_values:
                unexpected_details = "\n".join([f"• {col}: {count} unexpected values" 
                                              for col, count in unexpected_values.items()])
                message["attachments"][0]["fields"].append({
                    "title": "Unexpected Values",
                    "value": unexpected_details,
                    "short": False
                })
            
            # Send to Slack
            response = requests.post(
                self.slack_webhook_url,
                data=json.dumps(message),
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print("✅ Slack notification sent successfully!")
            else:
                print(f"❌ Failed to send Slack notification: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error sending Slack notification: {e}")
    
    def run_full_validation(self):
        """Run complete validation pipeline"""
        print("🚀 Starting Great Expectations Validation Pipeline...")
        
        # Step 1: Load data
        if not self.load_data():
            return
        
        # Step 2: Run expectations
        results = self.create_and_run_expectations()
        if results is None:
            return
        
        # Step 3: Display results
        print("\n" + "="*50)
        print("📊 VALIDATION RESULTS")
        print("="*50)
        print(f"Overall Success: {results['success']}")
        print(f"Total Expectations: {results['statistics']['total_expectations']}")
        print(f"Passed: {results['statistics']['successful_expectations']}")
        print(f"Failed: {results['statistics']['failed_expectations']}")
        
        # Step 4: Send Slack notification
        self.send_slack_notification(results)
        
        return results

def create_sample_data():
    """Create sample Amazon orders data for testing"""
    sample_data = {
        'order_id': ['ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005'],
        'qty': [2, 1, 3, 0, 2],
        'amount': [29.99, 15.50, 45.00, 0.00, 39.98],
        'status': ['delivered', 'shipped', 'processing', 'cancelled', 'delivered']
    }
    
    # Ayrıca bazı invalid data da ekleyelim
    invalid_data = {
        'order_id': ['ORD006', 'ORD007', None, 'ORD002'],  # Null ve duplicate
        'qty': [1, -1, 2, 3],  # Negative value
        'amount': [10.0, -5.0, 20.0, 15.0],  # Negative value
        'status': ['shipped', 'unknown', 'delivered', 'invalid']  # Invalid status
    }
    
    df_valid = pd.DataFrame(sample_data)
    df_invalid = pd.DataFrame(invalid_data)
    df_combined = pd.concat([df_valid, df_invalid], ignore_index=True)
    
    df_combined.to_csv('amazon_orders.csv', index=False)
    print("✅ Sample data created: amazon_orders.csv")
    print("📝 Contains both valid and invalid data for testing")
    return df_combined

# Main execution
if __name__ == "__main__":
    # Create sample data
    create_sample_data()
    
    # Replace with your actual Slack webhook URL or set to None
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
    # Initialize validator
    validator = GreatExpectationsValidator(
        csv_file_path="amazon_orders.csv",
        slack_webhook_url=SLACK_WEBHOOK_URL
    )
    
    # Run full validation
    results = validator.run_full_validation()