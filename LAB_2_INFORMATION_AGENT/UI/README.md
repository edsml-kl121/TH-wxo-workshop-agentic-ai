## Part 1: Create the Agent

1. **Create an agent** called `information_agent`.
2. **Agent Description:**
	 > This agent handles internal tasks such as product information lookup, promotion or voucher lookup, getting the status of the product, and websearch to research support. It is not client-facing but works behind the scenes to provide accurate internal knowledge for decision-making and client support.
3. **Upload** the `information_openapi.json` file.
4. **Select the following endpoints:**
	 - `get_products`
	 - `get_status`
	 - `get_promotions`

	 ![Agent OpenAPI Upload](images/image.png)

5. **Test the endpoints:**
	 - **get_products:**
		 > ร้านนี้มีเก้าอี้สีแดงขายบ้างไหม
	 - **get_promotions:**
		 > มี voucher อะไรที่ใช้ลดราคาสินค้านี้ได้บ้าง
	 - **get_status:**
		 > ที่เคยสั่งเก้าอี้สีแดงไว้ ตอนนนี้อยู่ที่ไหนแล้ว

---

## Part 2: Add MCP Tools (Tavily)

1. Visit the [Tavily website](https://www.tavily.com/) and **sign up or log in**.
   
	 ![Tavily Website](images/image3.png)

2. **Copy your API key** (you will use this in the next steps).
   
	 ![Tavily API Key](images/image4.png)

3. Go to **Manage > Connections** and add a new connection:
	 - ![Add Connection](images/image6.png)
	 - Enter a **connection ID** and **display name**.
		 ![Connection ID](images/image7.png)
	 - For draft connection:
		 - Set authentication type to **Key Value Pair**
		 - Choose credential type **"team"**
		 ![Draft Config](images/image8.png)
		 - Add Key `TAVILY_API_KEY` and paste your API key from step 2 as the value, then click **Connect**.
		 ![Add Key](images/image9.png)
	 - Repeat the above for the **live connection**, then click **Add Connection**.
		 ![Live Connection 1](images/image10.png)
		 ![Live Connection 2](images/image11.png)

4. Go back to your **agent toolkits** and **import external tool** from MCP server:
	 - ![Import Tool](images/image12.png)
	 - Click **Add MCP Server** and enter:
		 - Server name
		 - Previously added connection (from step 3)
		 - Install command: `npx -y tavily-mcp`
		 ![Add MCP Server](images/image13.png)
	 - Toggle the **Tavily Search Tool**
		 ![Toggle Tool](images/image14.png)

5. **Test the agent's web search tool** with the prompt:
	 > ลองค้นหาหน่อยว่าต้องใช้เวลานานแค่ไหนในการส่งสินค้าทางรถจากนครศรีธรรมราชมากรุงเทพ
	 ![Test Search](images/image15.png)
