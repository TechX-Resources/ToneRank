# ToneRank

Tone Rank reads emails in an inbox and splits emails into two categories: emails which are from institutions, businesses, or organizations, and emails which are from individuals. Each category is ordered by tone and urgency, then the two sorted categories are presented in order; the first category first, and the second (personal email) category second.

<img width="1006" alt="ToneRank Architecture" src="https://github.com/user-attachments/assets/55576f0a-1e99-4821-93a2-42906907437e" />

1. The Gmail API is used to retrieve all emails sent to the user's email address in the past 24 hours
2. The emails are divided into Category 1 (businesses, organizations, and institutions) and Category 2 (personal)
3. Both categories are used as input for Llama 3 (accessed via the Groq API)
4. An internal query is used to prompt Llama 3 to sort both categories by urgency
5. The emails are outputted in ranked order of Category 1 followed by ranked order of Category 2
6. A priority report is delivered to the user

Cited Sources:
1. email-verify.my-addr.com/list-of-most-popular-email-domains.php (list of top 100 public email domains)
