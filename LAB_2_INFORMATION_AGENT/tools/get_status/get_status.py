from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_status() -> str:
    """
    ดึงข้อมูลโปรโมชั่นและส่วนลดที่มีอยู่ทั้งหมดสำหรับเฟอร์นิเจอร์

    This tool returns a comprehensive list of active promotions and discount codes 
    available for furniture purchases. It includes:
    - Promotion ID and title
    - Discount percentage or fixed amount
    - Conditions and requirements (in Thai)
    - Applicable categories or specific products
    - Valid date ranges
    - Usage limits and current status

    Types of promotions available:
    - Category-specific discounts (chairs, tables, beds, etc.)
    - New customer welcome offers
    - Product-specific deals
    - Minimum purchase amount rewards
    - Bundle discounts for multiple items
    - Special occasion sales (weekends, student discounts)
    - Free shipping promotions

    The data is returned as a JSON-formatted string containing 9 active promotions.

    :returns: A JSON string containing a list of active furniture promotions with 
              Thai conditions, discount details, and validity periods.
    """
    try:
        status_data = """\
[
  {
    "furniture_id": "FU-009",
    "furniture_name": "เก้าอี้รับประทานอาหารซอฟี",
    "quantity": 1,
    "order_date": "2024-12-11",
    "location": "เพชรบุรี",
    "status": "delivered"
  },
  {
    "furniture_id": "FU-001",
    "furniture_name": "โต๊ะมอนิกา",
    "quantity": 1,
    "order_date": "2024-12-12",
    "location": "ตาก",
    "status": "pending"
  },
  {
    "furniture_id": "FU-004",
    "furniture_name": "โซฟาเลโอนาร์โด",
    "quantity": 1,
    "order_date": "2024-12-13",
    "location": "ยะลา",
    "status": "cancelled"
  },
  {
    "furniture_id": "FU-011",
    "furniture_name": "เก้าอี้แดงคาร์มิน",
    "quantity": 1,
    "order_date": "2024-12-14",
    "location": "นครศรีธรรมราช",
    "status": "processing"
  }
]"""
        return status_data
    except Exception as e:
        return f"❌ ไม่สามารถดึงข้อมูลการนัดหมายได้: {str(e)}"