from logging import root
from model import get_ai_content
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import json


def get_email_intent(body):

    prompt = f"""
You are an insurance claim email classification assistant.
You will be given the body of an email. Your task is to determine the intent **only if the email is from the customer** in response to a claim-related communication.

## Classification Rules:
1. Ignore and return "SystemMessage" if the email is clearly from the company/system 
   (e.g., claim registration confirmation, automated status updates, disclaimers) and not from the customer.
2. If the email is from the customer:
   - Return "Proceed" if the customer is explicitly asking to move forward with the claim process 
     or confirming they want it processed.
       Examples: "Please proceed", "Yes, go ahead", "I want to file this claim", 
       "Continue with the process", "Proceed with my claim", "Please start the process".
   - Return "Acknowledge" if the customer is simply thanking, acknowledging receipt, 
     or expressing appreciation without requesting further action.
       Examples: "Thank you", "Got it", "I appreciate your help", "Noted", "Thanks for letting me know".

## Few-Shot Examples:
Email: "Please proceed with my claim, I agree with your assessment."
Output: "Proceed"

Email: "Thanks for letting me know about the duplicate claim."
Output: "Acknowledge"

Email: "I understand there might be a duplicate, but I want to go ahead with the claim."
Output: "Proceed"

Email: "Claim Number: 000-00-004665 has been successfully registered."
Output: "SystemMessage"

Email: "I appreciate your quick response."
Output: "Acknowledge"

Email: "Yes, go ahead and file it."
Output: "Proceed"

## Output format:
Return only one of these strings exactly:
- "SystemMessage"
- "Proceed"
- "Acknowledge"

## Email Body:
{body}
"""
    
    response = get_ai_content(prompt)
    print("Intent Response:", response)  
    return response.strip()


def verify_policy_details(policy_details):
    try:
        # If policy_details is JSON with [ "xmlstring" ]
        if policy_details.strip().startswith("["):
            xml_list = json.loads(policy_details)
            xml_string = xml_list[0]
        else:
            xml_string = policy_details

        # Register namespace
        ns = {'ns': 'http://guidewire.com/pc/gx/gw.webservice.pc.pc1000.gxmodel.policyperiodmodel'}

        # Parse XML
        root = ET.fromstring(xml_string)
        print("✅ XML parsed successfully")

        # Extract Period End
        period_end = root.find('ns:PeriodEnd', ns)
        if period_end is not None:
            period_end_dt = datetime.fromisoformat(period_end.text.replace("Z", "+00:00"))
            print(f"📌 Period End Date: {period_end_dt}")
        else:
            print("⚠️ PeriodEnd not found")
            return None, None, None, None

        # Extract Effective Date
        effective_date = root.find('ns:Policy/ns:OriginalEffectiveDate', ns)
        if effective_date is not None:
            effective_date_dt = datetime.fromisoformat(effective_date.text.replace("Z", "+00:00"))
            print(f"📌 Original Effective Date: {effective_date_dt}")
        else:
            effective_date_dt = None

        # Extract Policy Type
        policy_type = None
        for elem in root.iter():
            if elem.tag.endswith("PolicyType"):
                policy_type = elem.text
                break

        # Extract Policy Number
        policy_number = root.find('ns:PolicyNumber', ns)
        policy_number = policy_number.text if policy_number is not None else None

        # Today's date (UTC)
        today = datetime.now(timezone.utc)
        status = "Expired" if today > period_end_dt else "Inforce"

        return status, policy_type

    except Exception as e:
        print(f"❌ Error while parsing XML: {e}")
        return None, None