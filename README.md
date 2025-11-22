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
