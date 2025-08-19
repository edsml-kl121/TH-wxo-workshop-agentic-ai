from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="Furniture Store API", version="1.0.0")

# Response models for better API documentation
class Promotion(BaseModel):
    id: str
    title: str
    discount_percentage: Optional[int] = None
    discount_amount: Optional[int] = None
    condition: str
    applicable_category: Optional[List[str]] = None
    applicable_products: Optional[List[str]] = None
    valid_from: str
    valid_until: str
    usage_limit: int
    status: str
    min_quantity: Optional[int] = None

class Product(BaseModel):
    id: str
    name: str
    category: str
    description: str
    price: int

class OrderStatus(BaseModel):
    furniture_id: str
    furniture_name: str
    quantity: int
    order_date: str
    location: str
    status: str

class PromotionsResponse(BaseModel):
    promotions: List[Promotion]

class ProductsResponse(BaseModel):
    products: List[Product]

class OrderStatusResponse(BaseModel):
    orders: List[OrderStatus]

def get_promotions() -> str:
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
        promotion_data = """\
[
  {
    "id": "CHAIRLOVER30",
    "title": "Chair Lover Special",
    "discount_percentage": 30,
    "condition": "สามารถใช้ได้กับเก้าอี้ทุกรุ่น",
    "applicable_category": ["เก้าอี้"],
    "valid_from": "2024-11-01",
    "valid_until": "2026-12-31",
    "usage_limit": 100,
    "status": "active"
  },
  {
    "id": "NEWBIE10",
    "title": "Welcome New Customer",
    "discount_percentage": 10,
    "condition": "สำหรับลูกค้าใหม่เท่านั้น",
    "applicable_category": ["โต๊ะ","เก้าอี้", "ตู้", "โซฟา", "ชั้น", "เตียง"],
    "valid_from": "2024-11-01",
    "valid_until": "2026-03-31",
    "usage_limit": 500,
    "status": "active"
  },
  {
    "id": "SCARLET20",
    "title": "Red Scarlet Exclusive",
    "discount_percentage": 20,
    "condition": "ใช้ได้เฉพาะเก้าอี้แดงสการ์เล็ตเท่านั้น",
    "applicable_products": ["FU-012"],
    "valid_from": "2024-12-01",
    "valid_until": "2026-12-25",
    "usage_limit": 50,
    "status": "active"
  },
  {
    "id": "BIG50K",
    "title": "Big Spender Reward",
    "discount_amount": 5000,
    "condition": "ซื้อครบ 50,000 บาท ลดทันที 5,000 บาท",
    "applicable_category": ["โต๊ะ", "ตู้", "โซฟา", "ชั้น", "เตียง"],
    "valid_from": "2024-11-15",
    "valid_until": "2026-01-15",
    "usage_limit": 200,
    "status": "active"
  },
  {
    "id": "BEDROOM25",
    "title": "Bedroom Makeover",
    "discount_percentage": 25,
    "condition": "ใช้ได้กับเตียง ตู้เสื้อผ้า และโต๊ะเครื่องแป้ง",
    "applicable_products": ["FU-003", "FU-006", "FU-010"],
    "valid_from": "2024-12-01",
    "valid_until": "2025-02-28",
    "usage_limit": 75,
    "status": "active"
  },
  {
    "id": "FREESHIP",
    "title": "Free Delivery Special",
    "discount_amount": 1500,
    "condition": "ฟรีค่าจัดส่ง สำหรับการสั่งซื้อครั้งแรกของสมาชิก VIP",
    "applicable_category": ["โต๊ะ", "เก้าอี้", "ตู้", "โซฟา", "ชั้น", "เตียง"],
    "valid_from": "2024-11-01",
    "valid_until": "2025-06-30",
    "usage_limit": 300,
    "status": "active"
  },
  {
    "id": "WEEKEND15",
    "title": "Weekend Flash Sale",
    "discount_percentage": 15,
    "condition": "ใช้ได้เฉพาะวันเสาร์-อาทิตย์ กับโซฟาและโต๊ะกาแฟ",
    "applicable_products": ["FU-004", "FU-007"],
    "valid_from": "2024-11-02",
    "valid_until": "2025-12-31",
    "usage_limit": 150,
    "status": "active"
  },
  {
    "id": "STUDENT12",
    "title": "Student Discount",
    "discount_percentage": 12,
    "condition": "ส่วนลดพิเศษสำหรับนักเรียน นักศึกษา (ต้องแสดงบัตรนักเรียน)",
    "applicable_category": ["โต๊ะ", "ชั้น"],
    "valid_from": "2024-11-01",
    "valid_until": "2025-05-31",
    "usage_limit": 400,
    "status": "active"
  },
  {
    "id": "BUNDLE35",
    "title": "Complete Set Bonus",
    "discount_percentage": 35,
    "condition": "ซื้อครบ 3 ชิ้นขึ้นไปในคำสั่งซื้อเดียวกัน",
    "applicable_category": ["โต๊ะ", "ชั้น"],
    "valid_from": "2024-11-20",
    "valid_until": "2026-01-20",
    "min_quantity": 3,
    "usage_limit": 80,
    "status": "active"
  }
]"""
        return promotion_data
    except Exception as e:
        return f"❌ ไม่สามารถดึงข้อมูลโปรโมชั่นได้: {str(e)}"

def get_products() -> str:
    """
    ดึงข้อมูลรายการเฟอร์นิเจอร์ที่มีอยู่ทั้งหมด รวมถึงชื่อสินค้า รายละเอียดสินค้า(เช่น วัสดุ, สี, การใช้งาน) ราคา และหมวดหมู่

    This tool returns a comprehensive catalog of furniture products available in the store.
    It includes Thai furniture items with the following information:
    - Product ID (format: FU-XXX)
    - Thai product names
    - Category (โต๊ะ, เก้าอี้, ตู้, โซฟา, ชั้น, เตียง)
    - Detailed Thai descriptions including materials and intended use
    - Prices in Thai Baht (THB)

    Categories available:
    - โต๊ะ (Tables): Work desks, coffee tables, vanity tables
    - เก้าอี้ (Chairs): Office chairs, dining chairs, accent chairs  
    - ตู้ (Cabinets): Wardrobes, display cabinets
    - โซฟา (Sofas): Living room sofas
    - ชั้น (Shelves): Bookshelves
    - เตียง (Beds): Bedroom beds

    :returns: A JSON string containing a list of furniture products with Thai names, descriptions, categories, and prices.
    """
    try:
        product_data = """\
[
 {
   "id": "FU-001",
   "name": "โต๊ะมอนิกา",
   "category": "โต๊ะ",
   "description": "โต๊ะทำงาน/โต๊ะอ่านหนังสือ ไม้โอ๊ค",
   "price": 12500
 },
 {
   "id": "FU-002",
   "name": "เก้าอี้เซบาสเตียน",
   "category": "เก้าอี้",
   "description": "เก้าอี้สำนักงาน/เก้าอี้ผู้บริหาร หนังแท้และโครงเหล็ก",
   "price": 18900
 },
 {
   "id": "FU-003",
   "name": "ตู้เสื้อผ้าอเล็กซานดรา",
   "category": "ตู้",
   "description": "เก็บเสื้อผ้าในห้องนอน ไม้สนและกระจกเทมเปอร์",
   "price": 24800
 },
 {
   "id": "FU-004",
   "name": "โซฟาเลโอนาร์โด",
   "category": "โซฟา",
   "description": "นั่งพักผ่อนในห้องนั่งเล่น ผ้าลินินและโฟมหนาแน่นสูง",
   "price": 32000
 },
 {
   "id": "FU-005",
   "name": "ชั้นหนังสือคลาร่า",
   "category": "ชั้น",
   "description": "จัดเก็บหนังสือและของตกแต่ง ไม้ยางพาราและเหล็กดำ",
   "price": 8750
 },
 {
   "id": "FU-006",
   "name": "เตียงนอนอีธาน",
   "category": "เตียง",
   "description": "เตียงนอนสำหรับห้องนอนใหญ่ ไม้มะฮอกกานีและหัวเตียงบุนวม",
   "price": 28600
 },
 {
   "id": "FU-007",
   "name": "โต๊ะกาแฟอิซาเบลลา",
   "category": "โต๊ะ",
   "description": "โต๊ะกลางสำหรับห้องรับแขก หินอ่อนคาราร่าและขาทองเหลือง",
   "price": 16200
 },
 {
   "id": "FU-008",
   "name": "ตู้โชว์วิคตอเรีย",
   "category": "ตู้",
   "description": "จัดแสดงของสะสมและเครื่องแก้ว ไม้เชอร์รี่และกระจกใส",
   "price": 21400
 },
 {
   "id": "FU-009",
   "name": "เก้าอี้รับประทานอาหารซอฟี",
   "category": "เก้าอี้",
   "description": "เก้าอี้สำหรับโต๊ะอาหาร (ขายเป็นชุด 4 ตัว) ไม้บีชและเบาะหนังสังเคราะห์",
   "price": 14000
 },
 {
   "id": "FU-010",
   "name": "โต๊ะเครื่องแป้งอเดลีน",
   "category": "โต๊ะ",
   "description": "โต๊ะเครื่องแป้งพร้อมกระจกส่องหน้า ไม้สักและกระจกบรอนซ์",
   "price": 19750
 },
 {
   "id": "FU-011",
   "name": "เก้าอี้แดงคาร์มิน",
   "category": "เก้าอี้",
   "description": "เก้าอี้รับประทานอาหารหรือเก้าอี้ตกแต่ง หนัง PU สีแดงและขาไม้โอ๊ค",
   "price": 7800
 },
 {
   "id": "FU-012",
   "name": "เก้าอี้แดงสการ์เล็ต",
   "category": "เก้าอี้",
   "description": "เก้าอี้โมเดิร์นสำหรับห้องนั่งเล่นหรือสำนักงาน ผ้ากำมะหยี่สีแดงและโครงเหล็กชุบโครเมียม",
   "price": 11500
 }
]"""
        return product_data
    except Exception as e:
        return f"❌ ไม่สามารถดึงข้อมูลสินค้าได้: {str(e)}"

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
        return f"❌ ไม่สามารถดึงข้อมูลสถานะคำสั่งซื้อได้: {str(e)}"

@app.get("/")
async def root():
    return {"message": "Furniture Store API", "version": "1.0.0"}

@app.post("/promotions", response_model=PromotionsResponse)
async def get_all_promotions():
    """
    Get all available furniture promotions and discounts
    
    Returns a list of active promotions including:
    - Promotion codes and titles
    - Discount percentages or fixed amounts
    - Conditions and requirements (in Thai)
    - Applicable categories or products
    - Valid date ranges
    - Usage limits
    """
    try:
        promotions_json = get_promotions()
        
        if promotions_json.startswith("❌"):
            raise HTTPException(status_code=500, detail=promotions_json)
        
        promotions_data = json.loads(promotions_json)
        return {"promotions": promotions_data}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse promotions data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/products", response_model=ProductsResponse)
async def get_all_products():
    """
    Get all available furniture products
    
    Returns a comprehensive catalog including:
    - Product IDs and Thai names
    - Categories (โต๊ะ, เก้าอี้, ตู้, โซฟา, ชั้น, เตียง)
    - Detailed descriptions with materials
    - Prices in Thai Baht
    """
    try:
        products_json = get_products()
        
        if products_json.startswith("❌"):
            raise HTTPException(status_code=500, detail=products_json)
        
        products_data = json.loads(products_json)
        return {"products": products_data}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse products data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/orders/status", response_model=OrderStatusResponse)
async def get_order_status():
    """
    Get status of all furniture orders
    
    Returns order information including:
    - Furniture IDs and names
    - Quantities ordered
    - Order dates
    - Delivery locations
    - Current status (delivered, pending, cancelled, processing)
    """
    try:
        status_json = get_status()
        
        if status_json.startswith("❌"):
            raise HTTPException(status_code=500, detail=status_json)
        
        status_data = json.loads(status_json)
        return {"orders": status_data}
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse order status data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)