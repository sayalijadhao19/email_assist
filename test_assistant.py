"""
Unit Tests for Legal Email Assistant
Tests for email analysis and reply drafting functionality
"""

import unittest
import json
from email_assistant import (
    EmailAnalyzer, 
    ReplyDrafter, 
    LegalEmailAgent,
    analyze_email,
    draft_reply
)


class TestEmailAnalyzer(unittest.TestCase):
    """Test cases for EmailAnalyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmailAnalyzer()
        self.sample_email = """Subject: Termination of Services under MSA
Dear Counsel,
We refer to the Master Services Agreement dated 10 March 2023 between Acme
Technologies Pvt. Ltd. ("Acme") and Brightwave Solutions LLP ("Brightwave").
Due to ongoing performance issues and repeated delays in delivery, we are considering
termination of the Agreement for cause with effect from 1 December 2025.
Please confirm:
1. Whether we are contractually entitled to terminate for cause on the basis of repeated
delays in delivery;
2. The minimum notice period required.
We would appreciate your advice by 18 November 2025.
Regards,
Priya Sharma
Legal Manager, Acme Technologies Pvt. Ltd."""

    def test_analyze_email_returns_dict(self):
        """Test that analyze_email returns a dictionary."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertIsInstance(result, dict)

    def test_analyze_email_has_required_keys(self):
        """Test that analysis contains all required keys."""
        result = self.analyzer.analyze_email(self.sample_email)
        required_keys = [
            'intent', 'primary_topic', 'parties', 
            'agreement_reference', 'questions', 
            'requested_due_date', 'urgency_level'
        ]
        for key in required_keys:
            self.assertIn(key, result)

    def test_intent_extraction(self):
        """Test intent extraction."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertEqual(result['intent'], 'legal_advice_request')

    def test_primary_topic_extraction(self):
        """Test primary topic extraction."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertEqual(result['primary_topic'], 'termination_for_cause')

    def test_parties_extraction(self):
        """Test party extraction."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertIn('client', result['parties'])
        self.assertIn('counterparty', result['parties'])
        self.assertEqual(result['parties']['client'], 'Acme Technologies Pvt. Ltd.')
        self.assertEqual(result['parties']['counterparty'], 'Brightwave Solutions LLP')

    def test_agreement_reference_extraction(self):
        """Test agreement reference extraction."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertIn('type', result['agreement_reference'])
        self.assertIn('date', result['agreement_reference'])
        self.assertEqual(result['agreement_reference']['type'], 'Master Services Agreement')
        self.assertEqual(result['agreement_reference']['date'], '10 March 2023')

    def test_questions_extraction(self):
        """Test question extraction."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertIsInstance(result['questions'], list)
        self.assertGreater(len(result['questions']), 0)
        # Check that questions are extracted
        self.assertTrue(any('terminate' in q.lower() for q in result['questions']))

    def test_due_date_extraction(self):
        """Test due date extraction."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertEqual(result['requested_due_date'], '18 November 2025')

    def test_urgency_level_determination(self):
        """Test urgency level determination."""
        result = self.analyzer.analyze_email(self.sample_email)
        self.assertIn(result['urgency_level'], ['low', 'medium', 'high'])

    def test_empty_email(self):
        """Test handling of empty email."""
        result = self.analyzer.analyze_email("")
        self.assertIsInstance(result, dict)
        self.assertIn('intent', result)

    def test_email_without_dates(self):
        """Test email without dates."""
        email = """Subject: General Inquiry
Dear Team,
We have some questions about the contract.
Regards, John"""
        result = self.analyzer.analyze_email(email)
        self.assertIsNone(result['requested_due_date'])


class TestReplyDrafter(unittest.TestCase):
    """Test cases for ReplyDrafter class."""

    def setUp(self):
        """Set up test fixtures."""
        self.drafter = ReplyDrafter()
        self.sample_email = """Subject: Termination of Services under MSA
Dear Counsel,
We refer to the Master Services Agreement dated 10 March 2023 between Acme
Technologies Pvt. Ltd. ("Acme") and Brightwave Solutions LLP ("Brightwave").
Due to ongoing performance issues and repeated delays in delivery, we are considering
termination of the Agreement for cause with effect from 1 December 2025.
Please confirm:
1. Whether we are contractually entitled to terminate for cause on the basis of repeated
delays in delivery;
2. The minimum notice period required.
We would appreciate your advice by 18 November 2025.
Regards,
Priya Sharma
Legal Manager, Acme Technologies Pvt. Ltd."""

        self.sample_analysis = {
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
                "Whether we are contractually entitled to terminate for cause?",
                "The minimum notice period required?"
            ],
            "requested_due_date": "18 November 2025",
            "urgency_level": "medium"
        }

        self.sample_contract = """Clause 9 – Termination for Cause
9.1 Either Party may terminate this Agreement for cause upon thirty (30) days' written
notice if the other Party commits a material breach.
9.2 Repeated failure to meet delivery timelines constitutes a material breach.
Clause 10 – Notice
10.1 All notices shall be given in writing and shall be effective upon receipt.
10.2 For termination, minimum thirty (30) days' prior written notice is required."""

    def test_draft_reply_returns_string(self):
        """Test that draft_reply returns a string."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIsInstance(result, str)

    def test_reply_contains_subject(self):
        """Test that reply contains a subject line."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIn('Subject:', result)

    def test_reply_contains_greeting(self):
        """Test that reply contains proper greeting."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIn('Dear', result)

    def test_reply_mentions_agreement(self):
        """Test that reply mentions the agreement."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIn('Master Services Agreement', result)

    def test_reply_cites_clauses(self):
        """Test that reply cites relevant contract clauses."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIn('Clause', result)
        self.assertTrue('9.1' in result or '9.2' in result or '10.2' in result)

    def test_reply_addresses_termination(self):
        """Test that reply addresses termination questions."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIn('termination', result.lower())

    def test_reply_addresses_notice_period(self):
        """Test that reply addresses notice period."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIn('30', result)
        self.assertIn('days', result.lower())

    def test_reply_has_signature(self):
        """Test that reply has proper signature."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        self.assertIn('Regards', result)
        self.assertIn('Legal Team', result)

    def test_reply_professional_tone(self):
        """Test that reply maintains professional tone."""
        result = self.drafter.draft_reply(
            self.sample_email, 
            self.sample_analysis, 
            self.sample_contract
        )
        # Check for professional language indicators
        professional_terms = ['pursuant', 'regarding', 'please', 'thank you']
        self.assertTrue(any(term in result.lower() for term in professional_terms))


class TestLegalEmailAgent(unittest.TestCase):
    """Test cases for LegalEmailAgent orchestrator."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = LegalEmailAgent()
        self.sample_email = """Subject: Termination of Services under MSA
Dear Counsel,
We refer to the Master Services Agreement dated 10 March 2023 between Acme
Technologies Pvt. Ltd. ("Acme") and Brightwave Solutions LLP ("Brightwave").
Due to ongoing performance issues and repeated delays in delivery, we are considering
termination of the Agreement for cause with effect from 1 December 2025.
Please confirm:
1. Whether we are contractually entitled to terminate for cause on the basis of repeated
delays in delivery;
2. The minimum notice period required.
We would appreciate your advice by 18 November 2025.
Regards,
Priya Sharma
Legal Manager, Acme Technologies Pvt. Ltd."""

        self.sample_contract = """Clause 9 – Termination for Cause
9.1 Either Party may terminate this Agreement for cause upon thirty (30) days' written
notice if the other Party commits a material breach.
9.2 Repeated failure to meet delivery timelines constitutes a material breach.
Clause 10 – Notice
10.1 All notices shall be given in writing and shall be effective upon receipt.
10.2 For termination, minimum thirty (30) days' prior written notice is required."""

    def test_process_email_returns_dict(self):
        """Test that process_email returns a dictionary."""
        result = self.agent.process_email(self.sample_email, self.sample_contract)
        self.assertIsInstance(result, dict)

    def test_process_email_contains_analysis(self):
        """Test that result contains analysis."""
        result = self.agent.process_email(self.sample_email, self.sample_contract)
        self.assertIn('analysis', result)
        self.assertIsInstance(result['analysis'], dict)

    def test_process_email_contains_draft_reply(self):
        """Test that result contains draft reply when contract provided."""
        result = self.agent.process_email(self.sample_email, self.sample_contract)
        self.assertIn('draft_reply', result)
        self.assertIsNotNone(result['draft_reply'])

    def test_process_email_without_contract(self):
        """Test processing email without contract text."""
        result = self.agent.process_email(self.sample_email)
        self.assertIn('analysis', result)
        self.assertIsNone(result['draft_reply'])


class TestAPIFunctions(unittest.TestCase):
    """Test cases for top-level API functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_email = """Subject: Termination of Services under MSA
Dear Counsel,
We refer to the Master Services Agreement dated 10 March 2023 between Acme
Technologies Pvt. Ltd. ("Acme") and Brightwave Solutions LLP ("Brightwave").
Due to ongoing performance issues and repeated delays in delivery, we are considering
termination of the Agreement for cause with effect from 1 December 2025.
Please confirm:
1. Whether we are contractually entitled to terminate for cause on the basis of repeated
delays in delivery;
2. The minimum notice period required.
We would appreciate your advice by 18 November 2025.
Regards,
Priya Sharma
Legal Manager, Acme Technologies Pvt. Ltd."""

        self.sample_contract = """Clause 9 – Termination for Cause
9.1 Either Party may terminate this Agreement for cause upon thirty (30) days' written
notice if the other Party commits a material breach.
9.2 Repeated failure to meet delivery timelines constitutes a material breach.
Clause 10 – Notice
10.1 All notices shall be given in writing and shall be effective upon receipt.
10.2 For termination, minimum thirty (30) days' prior written notice is required."""

    def test_analyze_email_function(self):
        """Test the analyze_email API function."""
        result = analyze_email(self.sample_email)
        self.assertIsInstance(result, dict)
        self.assertIn('intent', result)

    def test_draft_reply_function(self):
        """Test the draft_reply API function."""
        analysis = analyze_email(self.sample_email)
        result = draft_reply(self.sample_email, analysis, self.sample_contract)
        self.assertIsInstance(result, str)
        self.assertIn('Subject:', result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EmailAnalyzer()
        self.drafter = ReplyDrafter()

    def test_malformed_email(self):
        """Test handling of malformed email."""
        malformed = "This is not a proper email format"
        result = self.analyzer.analyze_email(malformed)
        self.assertIsInstance(result, dict)

    def test_email_with_special_characters(self):
        """Test email with special characters."""
        email = """Subject: Re: Contract — Review & Comments
Dear Team,
We need to discuss the "special provisions" mentioned.
Regards, John O'Brien"""
        result = self.analyzer.analyze_email(email)
        self.assertIsInstance(result, dict)

    def test_very_long_email(self):
        """Test handling of very long emails."""
        long_email = "Subject: Test\n" + "This is a very long email. " * 1000
        result = self.analyzer.analyze_email(long_email)
        self.assertIsInstance(result, dict)

    def test_multiple_agreements_mentioned(self):
        """Test email mentioning multiple agreements."""
        email = """Subject: Multiple Agreements
We refer to the Service Agreement dated 1 Jan 2023 and 
the Master Agreement dated 2 Feb 2023.
Regards, John"""
        result = self.analyzer.analyze_email(email)
        self.assertIsInstance(result['agreement_reference'], dict)


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEmailAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestReplyDrafter))
    suite.addTests(loader.loadTestsFromTestCase(TestLegalEmailAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)