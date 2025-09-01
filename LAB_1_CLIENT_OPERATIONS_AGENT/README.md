## Instructions

1. Please create an agent called `client_operation_agent`

![alt text](images/agent.png)

with the following description

```
This agent manages external-facing tasks and client communications, such as sending emails and scheduling meetings via Google services, and placing order for products to store in google sheets. Use it for client coordination and operational support.
```

2. upload the openapi json file that is provided called `openapi_tools/automation_openapi.json` and add google calendar and send gmail tools.

![alt text](images/openapi.png)


You should see that the tools have been added.

![alt text](images/tools.png)



3. Please choose `meta-llama/llama-3-405b-instruct` and test the agent with following queries:

**Testing Queries**


- สวัสดีครับช่วยส่งอีเมลหา `replace_with_your_email` มีหัวข้อเกี่ยวกับ "self introduction" และเนื้อหาคือ "Hello how are you"
- ช่วยยิงนัดกับ `replace_with_your_email` หน่อยวันที่ 11 ธันวาคม 2025, 11:00-12:00 ว่า "Self Introduction"
- ช่วยสั่งสินค้า 'ABC' จำนวน 1 ชิ้น ด้วย voucher ABCD

You can view the results of placed order here:

[Click to see Order placed in sheets](https://docs.google.com/spreadsheets/d/1JVyvsmVnxRarCXDWmyu1_beTxMzkKdXn6O2msz_aaAE/edit?usp=sharing)

To improve the model performance in Thai even further, watsonx Orchestrate supports using external models through feature called `AI gateway`. Read more later at: https://developer.watson-orchestrate.ibm.com/llm/managing_llm


4. Our goal is to add `google/gemini-2.5-flash` to watsonx Orchestrate. Rename `env-template` to `.env` and add in your `GOOGLE_API_KEY`.Please visit https://aistudio.google.com and click generate an API key to get your API key.

![alt text](images/getapikey.png)
![alt text](images/success.png)

NOTE:
If you are unable to create api key, it means you haven't enabled Gemini API in Google cloud console and created a project. Hence please, enable gemini API and create a project.

![alt text](images/unabletocreatekey.png)
Enabling Gemini API
![alt text](images/enablegemini.png)
Creating Project
![alt text](images/create-gcpproject.png)


5. Ensure you have completed the instructions in `00_SETUP`. Now that you have all credentials, add the model as follows. Choose to follow either UI or ADK.

    ### UI (Simplified instructions)

    Please navigate to the connections tab. And add a connection.
    ![alt text](images/gateway_1.png)

    Here you can create a connection called `gg_creds_UI`

    ![alt text](images/gateway_2.png)

    For draft environment, select the `Key Value Pair` and add the key value pair in. The key is `api_key` and the value is the API key from Gemini API you got earlier.

    ![alt text](images/gateway_3.png)

    Please repeat the same of live environment,
    The key is `api_key` and the value is the API key from Gemini API you got earlier.
    ![alt text](images/gateway_4.png)

    Once added connections, please navigate to your powershell/ terminal and type in the following command. This steps assumed you have completed `00_SETUP`

    Here is the comamnd
    ```
    orchestrate models add --name google/gemini-2.5-flash --app-id gg_creds_UI
    ```
    You should see gemini-2.5-flash model being added.

    ![alt text](images/added_gemini.png)

    
    **NOTE**: Additionally, watsonx Orchestrate provides the ability for developers to perform end to end connections creation to adding model with the ADK. Feel free to try this out at home.

    ## End of Labs
    ---

    ### End to end using ADK (Optional)

	**For Linux/macOS:**
	1. Open a terminal and navigate to the `AI_gateway/` folder.
	2. Make the scripts executable (run this once):
		```bash
		chmod +x set_connections.sh add_models.sh
		```
	3. Run the scripts:
		```bash
		./set_connections.sh
		./add_models.sh
		```

	**For Windows (PowerShell):**
	1. Open PowerShell and navigate to the `AI_gateway` folder.
	2. If you haven't already, allow running local scripts:
		```powershell
		Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
		```
		Then restart PowerShell.
	3. Run the scripts:
		```powershell
		./set_connections.ps1
		./add_models.ps1
		```
	4. If you get an error that the script is not digitally signed (i.e., it does not have a trusted publisher's signature and was downloaded or created locally), run the following to unblock the files, then try again:
		```powershell
		Unblock-File -Path .\set_connections.ps1
		Unblock-File -Path .\add_models.ps1
		```

	You should see the model being added.

![alt text](images/added_gemini.png)
