# Legal Email Assistant - Virtuon Technologies

A modular Python-based system for analyzing legal emails and drafting professional replies using an agent-based architecture.

## Overview

This Legal Email Assistant helps law firms automatically:

1. **Analyze** incoming legal emails to extract structured information
2. **Draft** professional legal reply emails based on contract clauses

## Architecture

The system follows a clean, modular architecture with:

- **EmailAnalyzer**: Analyzes raw emails and extracts structured data
- **ReplyDrafter**: Generates professional legal replies
- **LegalEmailAgent**: Orchestrates the workflow (agent-based pattern)
- **Data Models**: Type-safe data structures using dataclasses

```
┌─────────────────────────────────────┐
│     LegalEmailAgent                 │
│     (Orchestrator)                  │
└────────┬────────────────────┬───────┘
         │                    │
    ┌────▼─────┐        ┌────▼─────┐
    │ Email    │        │ Reply    │
    │ Analyzer │        │ Drafter  │
    └──────────┘        └──────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses only Python standard library)

### Setup

```bash
# Clone or download the repository
cd legal-email-assistant

# No pip install needed - uses only standard library
python email_assistant.py
```

## Usage

### Basic Usage

```python
from email_assistant import analyze_email, draft_reply

# Sample email text
email_text = """
Subject: Termination of Services under MSA
Dear Counsel,
We refer to the Master Services Agreement dated 10 March 2023...
"""

# Sample contract clauses
contract_text = """
Clause 9 – Termination for Cause
9.1 Either Party may terminate this Agreement...
"""

# Part 1: Analyze Email
analysis = analyze_email(email_text)
print(analysis)

# Part 2: Draft Reply
reply = draft_reply(email_text, analysis, contract_text)
print(reply)
```

### Using the Agent Orchestrator

```python
from email_assistant import LegalEmailAgent

# Initialize agent
agent = LegalEmailAgent()

# Process email end-to-end
result = agent.process_email(email_text, contract_text)

# Access results
analysis = result['analysis']
draft_reply = result['draft_reply']
```

## API Reference

### `analyze_email(email_text: str) -> dict`

Analyzes a raw email and returns structured JSON output.

**Parameters:**

- `email_text` (str): Raw email text including subject and body

**Returns:**

- Dictionary with structure:
  - `intent` (str): Primary intent (e.g., "legal_advice_request")
  - `primary_topic` (str): Main legal topic
  - `parties` (dict): Client and counterparty names
  - `agreement_reference` (dict): Agreement type and date
  - `questions` (list): Extracted questions
  - `requested_due_date` (str): Due date if mentioned
  - `urgency_level` (str): "low", "medium", or "high"

### `draft_reply(email_text: str, analysis: dict, contract_text: str) -> str`

Drafts a professional legal reply email.

**Parameters:**

- `email_text` (str): Original email text
- `analysis` (dict): Structured analysis from `analyze_email()`
- `contract_text` (str): Relevant contract clauses

**Returns:**

- String containing formatted reply email

## Example Output

### Analysis Output (JSON)

```json
{
  "intent": "legal_advice_request",
  "primary_topic": "termination_for_cause",
  "parties": {
    "client": "Acme Technologies Pvt. Ltd.",
    "counterparty": "Brightwave Solutions LLP"
  },
  "agreement_reference": {
    "type": "Master Services Agreement",
    "date": "10 March 2023"
  },
  "questions": [
    "Whether we are contractually entitled to terminate for cause on the basis of repeated delays in delivery?",
    "The minimum notice period required?"
  ],
  "requested_due_date": "18 November 2025",
  "urgency_level": "medium"
}
```

### Draft Reply Output

```
Subject: Re: Termination For Cause

Dear Ms. Sharma,

Thank you for your email regarding the Master Services Agreement dated 10 March 2023.

Based on our review of the agreement:

1. Regarding termination for cause: Under Clause 9.2, repeated failure to meet delivery timelines constitutes a material breach. Therefore, pursuant to Clause 9.1, termination for cause is contractually supported based on the performance issues you have described.

2. Regarding notice period: Under Clause 9.1 read with Clause 10.2, a minimum of thirty (30) days' prior written notice is required for termination. The notice must be in writing and shall be effective upon receipt as per Clause 10.1.

Please note that this analysis is based on the contract clauses provided. We recommend reviewing the complete agreement and considering any other relevant provisions or circumstances before proceeding with termination.

Please let us know if you would like us to prepare a draft termination notice or if you require any further clarification on this matter.

Regards,
Your Legal Team
```

## Features

### Email Analysis

- ✅ Intent detection (advice request, termination notice, breach notification, etc.)
- ✅ Topic extraction (termination, breach, performance issues, etc.)
- ✅ Party identification with abbreviation handling
- ✅ Agreement reference extraction (type and date)
- ✅ Multi-pattern question extraction
- ✅ Due date detection
- ✅ Urgency level determination

### Reply Drafting

- ✅ Professional legal tone
- ✅ Proper addressee formatting
- ✅ Contract clause citation
- ✅ Structured answers to questions
- ✅ Liability disclaimers
- ✅ Call-to-action closing

## Design Decisions & Assumptions

### Assumptions

1. **Email Format**: Emails follow standard business format with subject, body, and signature
2. **Party Naming**: Companies include legal entity indicators (Pvt. Ltd., LLP, Inc., etc.)
3. **Date Formats**: Dates can be in various formats (DD Month YYYY, Month DD, YYYY, etc.)
4. **Contract Structure**: Contracts have numbered clauses with titles
5. **Language**: All communications are in English

### Design Decisions

1. **No External Dependencies**: Uses only Python standard library for easier deployment
2. **Modular Architecture**: Separate classes for analysis and drafting enables easy testing and extension
3. **Agent Pattern**: Central orchestrator (LegalEmailAgent) coordinates workflow
4. **Type Safety**: Uses dataclasses for structured data with type hints
5. **Regex-Based Extraction**: Pattern matching for reliable information extraction
6. **Professional Tone**: Conservative language to avoid liability issues

## Testing

Run the built-in demo:

```bash
python email_assistant.py
```

This will process the sample email from the assignment and display both the analysis and draft reply.

## Extension Points

The system is designed to be easily extensible:

1. **Add New Intent Types**: Update `intent_keywords` in `EmailAnalyzer`
2. **Custom Reply Templates**: Modify `_build_reply_structure()` in `ReplyDrafter`
3. **Contract Clause Matching**: Enhance `_extract_relevant_clauses()` with ML-based matching
4. **Integration**: Add LangChain/LangGraph for more complex workflows
5. **Storage**: Add database layer for email/contract management
6. **API**: Wrap in Flask/FastAPI for web service deployment

## Potential Enhancements

- [ ] Machine learning for better intent classification
- [ ] LangChain integration for LLM-powered analysis
- [ ] Database integration for contract clause retrieval
- [ ] REST API endpoint
- [ ] Multi-language support
- [ ] Email thread handling
- [ ] Attachment processing
- [ ] Calendar integration for due dates

## File Structure

```
legal-email-assistant/
│
├── email_assistant.py    # Main application code
├── README.md            # This file
└── test_assistant.py    # Unit tests (optional)
```

## License

Proprietary - Virtuon Technologies

## Contact

For questions or support, please contact the Virtuon Technologies development team.

---

**Version**: 1.0.0  
**Last Updated**: November 2025
