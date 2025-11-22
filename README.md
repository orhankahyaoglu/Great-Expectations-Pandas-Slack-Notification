# Great Expectations - Pandas + Slack Notification

A comprehensive data quality validation project implementing Great Expectations for data validation with Pandas and Slack notifications.

## 🚀 Features

- **Great Expectations** data validation with 5 custom expectations
- **Slack notifications** for validation results
- **Pandas** for data manipulation
- **Comprehensive validation reporting**

## 📊 Validation Rules

1. ✅ `order_id` must not be null
2. ✅ `order_id` must be unique  
3. ✅ `qty` ≥ 0
4. ✅ `amount` ≥ 0
5. ✅ `status` must be in allowed set: `["delivered", "shipped", "processing", "cancelled"]`

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/orhankahyaoglu/Great-Expectations-Pandas-Slack-Notification.git
cd Great-Expectations-Pandas-Slack-Notification

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

📁 Project Structure
text
Great-Expectations-Pandas-Slack-Notification/
├── great_expectations_validator.py  # Main validation script
├── pydantic_validator.py           # Schema validation examples
├── config_schema.py                # Configuration validation
├── requirements.txt                # Project dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file

🎯 Usage
Basic Validation
python
python great_expectations_validator.py
With Slack Notifications
Get Slack webhook URL from https://api.slack.com/apps

Update SLACK_WEBHOOK_URL in the script

Run the validator

Expected Output
text
🚀 Starting Great Expectations Validation Pipeline...
✅ Dataset loaded successfully!
🎯 Creating and running expectations...
1. order_id not null: ✅ PASS
2. order_id unique: ✅ PASS
3. qty ≥ 0: ✅ PASS  
4. amount ≥ 0: ✅ PASS
5. status in allowed set: ✅ PASS
✅ Slack notification sent successfully!
🔧 Technologies Used
Great Expectations v0.15.50 - Data validation

Pandas - Data manipulation

Slack API - Notifications

Pydantic - Schema validation

📋 Requirements
Python 3.8+

Great Expectations 0.15.50

Pandas 1.5+

Requests 2.28+

👨‍💻 Author
Orhan Kahyaoglu

GitHub: @orhankahyaoglu
