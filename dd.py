import requests

LABEL_STUDIO_HOST = 'http://localhost:8085'
API_KEY = 'a0fd6ea3c7c5ebda8098385045c44f9fa3d8a1f6'

PROJECT_A_ID = 2  # Source project
PROJECT_B_ID = 14  # Target project

headers = {
    'Authorization': f'Token {API_KEY}'
}

# 🔁 Pagination loop to fetch all tasks
all_tasks = []
page = 1
page_size = 50

while True:
    response = requests.get(
        f'{LABEL_STUDIO_HOST}/api/projects/{PROJECT_A_ID}/tasks?page={page}&page_size={page_size}',
        headers=headers
    )

    if response.status_code != 200:
        print("❌ Failed to fetch tasks:", response.text)
        break

    page_tasks = response.json()
    if not page_tasks:
        break

    all_tasks.extend(page_tasks)
    print(f"📥 Fetched page {page}, {len(page_tasks)} tasks")
    page += 1

print(f"✅ Total tasks fetched: {len(all_tasks)}")

# 📨 Send each to Project B
for task in all_tasks:
    text_value = task.get("data", {}).get("text", "")
    if not text_value:
        continue

    data = {
        "data": {
            "text": text_value
        }
    }

    r = requests.post(
        f'{LABEL_STUDIO_HOST}/api/projects/{PROJECT_B_ID}/import',
        headers=headers,
        json=[data]
    )

    print(f'📤 Imported to Project B (NER_Test): {r.status_code}')
