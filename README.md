# Explanation: Current UI State

## Overview

Hi everyone,

I wanted to provide some context regarding the current state of our user interface (UI) within this repository. As you might have noticed, the UI is currently in an unstyled phase, lacking visual design and formatting.

## Details

### What's Missing?

At the moment:

- **Aesthetic Elements**: The UI lacks color schemes, fonts, and overall visual appeal.
- **Layout and Presentation**: Elements might seem disorganized or without an optimized layout.

### Impact

- **User Experience**: The lack of styling might affect user engagement and ease of use.
- **Perception**: It might convey an unfinished impression to contributors and users.

## Plan of Action

### Importance of Styling

It's crucial to understand that styling the UI is pivotal because it:

- Enhances user interaction and satisfaction.
- Reflects the project's professionalism and quality.
- Aligns with our brand and design ethos.

### Steps Ahead

1. **Design Phase**: Let's focus on incorporating UI/UX elements into the project roadmap.
   
# Setting Up a Django Web App with Daraja API

This guide will help you set up a Django web application to integrate with the Safaricom Daraja API for M-Pesa transactions.

## Daraja API Configuration

Configure your Daraja API settings in the Django project's settings file (`settings.py`):

### MPESA Environment
- `MPESA_ENVIRONMENT`: Specifies whether the environment is in sandbox or production.

### API Credentials
- `MPESA_CONSUMER_KEY`: Your M-Pesa API consumer key.
- `MPESA_CONSUMER_SECRET`: Your M-Pesa API consumer secret.
- `MPESA_PASSKEY`: Passkey for the M-Pesa API authentication.
- `MPESA_SHORT_CODE`: Your M-Pesa short code.

### Initiator Information
- `MPESA_INITIATOR_NAME`: Username for the API initiator.
- `MPESA_INITIATOR_PASSWORD`: Password for the API initiator.

### Callback URLs
- `MPESA_RESULT_URL`: URL to receive transaction result callbacks.
- `MPESA_QUEUE_TIMEOUT_URL`: URL to receive queue timeout callbacks.
- `MPESA_CALLBACK_URL`: URL for general API callbacks.

### Account Balance URLs
- `MPESA_ACCOUNT_BALANCE_TIMEOUT`: URL to receive account balance queue timeouts.
- `MPESA_ACCOUNT_BALANCE_RESULT`: URL to receive account balance results.

---

Styling our UI is essential to create an engaging and visually appealing experience. Your involvement and feedback are valuable as we move towards enhancing the project's user interface.

Thank you for your attention and support.

Best regards,

**Brian Gitau**
