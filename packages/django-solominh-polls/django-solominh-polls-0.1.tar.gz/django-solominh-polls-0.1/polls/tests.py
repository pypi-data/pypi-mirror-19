from django.test import TestCase

from .models import Question,Choice
from django.utils import timezone
# Create your tests here.
class TestQuestionModel(TestCase):
    
    def test_abc(self):
        expected=False
        question=Question(question_text="What's what?",pub_date=timezone.now() + timezone.timedelta(days=1))
        result=question.is_published_recently()
        return self.assertIs(result,expected)




