import requests
import json

NGROK_URL = "https://3d0ddbe02059.ngrok-free.app/api/v1/hackrx/run"
AUTH_TOKEN = "e6722c98521d93e48a741430431ac4a42b2de812838206df9cc46a4fe6795b5b"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}"
}

test_cases = [
    {
        "documents": "BAJHLIP23020V012223.pdf",
        "questions": [
            "What is the waiting period for maternity benefits?",
            "Is AYUSH treatment covered under this policy?",
            "What is the sub-limit for cataract surgery?",
            "Does this policy cover robotic surgeries?",
            "What room rent is allowed under Plan B?"
        ]
    },
    {
        "documents": "Arogya Sanjeevani Policy - CIN - U10200WB1906GOI001713 1.pdf",
        "questions": [
            "What is the maximum sum insured under this policy?",
            "What are the conditions for cataract treatment coverage?",
            "Is daycare procedure covered under this plan?",
            "How is a hospital defined in this document?",
            "What is the copayment clause?"
        ]
    },
    {
        "documents": "HDFHLIP23024V072223.pdf",
        "questions": [
            "What are the eligibility criteria for family coverage?",
            "What is the renewal condition after 65 years?",
            "How long is the grace period for premium payment?",
            "Does the policy cover fertility treatment?",
            "What are the exclusions for pre-existing diseases?"
        ]
    },
    {
        "documents": "EDLHLGA23009V012223.pdf",
        "questions": [
            "What treatments require prior authorization?",
            "What is the NCB clause and how is it calculated?",
            "Does this policy offer international treatment coverage?",
            "Is there any waiting period for heart-related procedures?",
            "How does the policy define day care treatment?"
        ]
    },
    {
        "documents": "ICIHLIP22012V012223.pdf",
        "questions": [
            "What are the exclusions listed for lifestyle diseases?",
            "Does the policy offer a health checkup benefit?",
            "How is a pre-existing condition handled under this policy?",
            "Are ambulance charges reimbursed?",
            "What is the cashless claim procedure?"
        ]
    },
    {
        "documents": "CHOTGDP23004V012223.pdf",
        "questions": [
            "Is organ donation surgery covered?",
            "What is the waiting period for joint replacement?",
            "What diseases are permanently excluded?",
            "Does this policy allow add-on covers?",
            "Is hospital cash benefit included?"
        ]
    }
]

for idx, case in enumerate(test_cases, 1):
    print(f"\n\n▶ Running test case {idx}...")
    response = requests.post(NGROK_URL, headers=HEADERS, json=case)
    print(f"Status Code: {response.status_code}")
    try:
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print("Failed to parse JSON response:", response.text)
