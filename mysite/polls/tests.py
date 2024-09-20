import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
# Create your tests here.

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, publication_date=time)

class QuestionModelTests(TestCase):

    def test_no_question(self):
        response = self.client.get(reverse("polls:index"))
        '''
        if(self.assertEqual(response.status_code, 200)):
            print("Se ha encontrado la página. 200")
        else:
            print("No se ha encontrado la página. 404")
        '''
        if(response.status_code == 200):
            print("Se ha encontrado la página. 200")
        else:
            print("No se ha encontrado la página. 404")

        if(response == "No polls are available."):
            print("No hay Questions.")
        else:
            print("Si hay Questions.")

        print(self.assertContains(response, "No polls are available."))
        print(self.assertQuerySetEqual(response.context["latest_question_list"], []))

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publication_date=time)
        self.assertIs(future_question.was_published_recently(),False)
    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(publication_date=time)
        self.assertIs(old_question.was_published_recently(), False)


    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(publication_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    #Test creando Questions.

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"],[])

    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question])
    
    def test_two_past_questions(self):
        question1 = create_question(question_text="Past_question 1.", days=-30)
        question2 = create_question(question_text="Past_question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question2,question1],)