from faker import Faker
from .models import Expend
import random
fake = Faker()


def populate(n):

    for entry in range(n):
        fake_source_amount = random.randrange(1000, 20000)
        fake_expend_amount = random.randrange(1000, 20000)
        fake_source_fund = fake.company()
        fake_expend_in = fake.company()
        by_user = random.choice(['adminer', 'panda123'])
        verified = random.choice(['no', 'yes'])
        fake_text = fake.text(max_nb_chars=380, ext_word_list=None)
        data = Expend.objects.create(by_user=by_user, verified=verified, expend_in=fake_expend_in, expend_amount=fake_expend_amount, source_fund=fake_source_fund, source_amount=fake_source_amount, description=fake_text)
        data.save()


