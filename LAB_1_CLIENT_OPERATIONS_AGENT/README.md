## Instructions

1. Please create an agent called `client_operation_agent`

![alt text](images/agent.png)

2. upload the openapi json file that is provided called `openapi_tools/automation_openapi.json` and add google calendar and send gmail tools.

![alt text](images/openapi.png)

You should see that the tools have been added.

![alt text](images/tools.png)

## Queries

- สวัสดีครับช่วยส่งอีเมลหา `replace_with_your_email` มีหัวข้อเกี่ยวกับการแนะนำตัว และเนื้อหาคือ "สวัสดีเป็นยังไงบ้าง"
- ช่วยยิงนัดกับ `replace_with_your_email` หน่อยวันที่ 11 ธันวาคม 2025, 11-12AM ว่า "ทำการรู้จักกัน"

## AI Gateway
3. Now let's try to add `google/gemini-2.5-flash` and `google/gemini-embedding-001`. Rename `env-template` to `.env` and add in your `GOOGLE_API_KEY`.

4. Run `set_connections.sh` followed by `add_models.sh`