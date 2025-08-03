from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_products() -> str:
    """
    ดึงข้อมูลรายการสินค้าที่มีอยู่ทั้งหมด รวมถึงชื่อสินค้า รายละเอียด ราคา และหมวดหมู่

    This tool returns a predefined catalog of products available for internal lookup or recommendation.
    It includes:
    - Product ID
    - Name
    - Category
    - Price
    - Description
    - Inventory stock count (for internal reference only)

    The data is returned as a JSON-formatted string for easy parsing or display in markdown-friendly tools.

    :returns: A JSON string containing a list of available products and their details.
    """
    try:
        appointment_data = """\
[
  {
    "id": "th-001",
    "name": "ระบบจัดการร้านอาหาร POS",
    "category": "ซอฟต์แวร์",
    "price": 29000,
    "stock": 10,
    "description": "ระบบ POS สำหรับร้านอาหาร พร้อมรายงานยอดขายและสต็อก"
  },
  {
    "id": "th-002",
    "name": "กล้องวงจรปิด Hikvision",
    "category": "ฮาร์ดแวร์",
    "price": 4900,
    "stock": 25,
    "description": "กล้องวงจรปิดความละเอียดสูง ดูออนไลน์ได้"
  },
  {
    "id": "th-003",
    "name": "โซลูชันจัดเก็บข้อมูลบนคลาวด์",
    "category": "คลาวด์",
    "price": 15000,
    "stock": 15,
    "description": "บริการ Cloud Storage แบบปลอดภัยสำหรับธุรกิจ"
  },
  {
    "id": "th-004",
    "name": "เครื่องอ่านบัตรประชาชน",
    "category": "อุปกรณ์",
    "price": 2200,
    "stock": 30,
    "description": "เครื่องอ่านบัตรสมาร์ทการ์ด มาตรฐานกรมการปกครอง"
  },
  {
    "id": "th-005",
    "name": "ระบบเช็คอินพนักงานด้วย QR Code",
    "category": "ซอฟต์แวร์",
    "price": 6500,
    "stock": 12,
    "description": "ระบบลงเวลาทำงานผ่านมือถือและ QR Code"
  },
  {
    "id": "th-006",
    "name": "ลำโพงประชุม Logitech",
    "category": "อุปกรณ์เสริม",
    "price": 8900,
    "stock": 18,
    "description": "ลำโพงไมค์สำหรับประชุม Zoom/Teams"
  },
  {
    "id": "th-007",
    "name": "ระบบวิเคราะห์ลูกค้า CRM",
    "category": "ซอฟต์แวร์",
    "price": 35000,
    "stock": 8,
    "description": "CRM วิเคราะห์พฤติกรรมลูกค้าและสร้างแคมเปญการตลาด"
  },
  {
    "id": "th-008",
    "name": "กล้องติดรถยนต์ Xiaomi",
    "category": "ฮาร์ดแวร์",
    "price": 2600,
    "stock": 50,
    "description": "กล้องติดรถยนต์พร้อม Night Vision"
  },
  {
    "id": "th-009",
    "name": "โปรแกรมบัญชีออนไลน์",
    "category": "ซอฟต์แวร์",
    "price": 12000,
    "stock": 20,
    "description": "โปรแกรมบัญชีสำหรับ SME ใช้งานง่าย"
  },
  {
    "id": "th-010",
    "name": "บริการให้คำปรึกษาด้าน AI",
    "category": "บริการ",
    "price": 20000,
    "stock": 5,
    "description": "บริการวิเคราะห์และปรับใช้ AI ในองค์กร"
  }
]"""
        return appointment_data
    except Exception as e:
        return f"❌ ไม่สามารถดึงข้อมูลการนัดหมายได้: {str(e)}"
    # return appointment_data