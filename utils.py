from model import get_ai_content

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