from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
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
        return f"❌ ไม่สามารถดึงข้อมูลการนัดหมายได้: {str(e)}"
