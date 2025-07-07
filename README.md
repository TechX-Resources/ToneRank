# ToneRank

Tone Rank reads emails in an inbox and splits emails into two categories: emails which are from institutions, businesses, or organizations, and emails which are from individuals. Each category is ordered by tone and urgency, then the two sorted categories are presented in order; the first category first, and the second (personal email) category second.

<img width="795" alt="Screenshot 2025-07-06 at 2 04 37 PM" src="https://github.com/user-attachments/assets/647581c5-c55b-4db7-bbfd-9e29db4b193e" />

1. The Gmail API is used to retrieve all emails sent to the user's email address in the past 24 hours
2. The emails are divided into Category 0 (emails whitelisted by the user), Category 1 (businesses, organizations, and institutions) and Category 2 (personal)
3. These categories are used as input for Llama 3 (accessed via the Groq API)
4. An internal query is used to prompt Llama 3 to sort each category by urgency
5. The emails are outputted in ranked order of Category 0, followed by ranked order of Category 1, and then ranked order of Category 2
6. A priority report is delivered to the user

Cited Sources:
1. email-verify.my-addr.com/list-of-most-popular-email-domains.php (list of top 100 public email domains)
