from django.test import SimpleTestCase
from accounts.forms import CustomerSignUpForm

# this test for form
class TestCustomerSignUpForm(SimpleTestCase):
    def test_valid_data(self):
        form = CustomerSignUpForm(data={'first_name':'ali','last_name':'niazi'})
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        form = CustomerSignUpForm(data={})
        self.assertFalse(form.is_valid())




