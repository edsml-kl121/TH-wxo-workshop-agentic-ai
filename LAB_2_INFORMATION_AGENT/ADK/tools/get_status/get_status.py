from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_status() -> str:
    """
    ดึงสถานะคำสั่งซื้อเฟอร์นิเจอร์

    This tool returns the current status of furniture orders, including details such as:
    - Furniture ID and name
    - Quantity ordered
    - Order date
    - Delivery location
    - Current order status (e.g., delivered, pending, cancelled, processing)

    The data is returned as a JSON-formatted string containing multiple orders.

    :returns: A JSON string containing a list of furniture orders with their details
              and current status.
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