from test_app import models

import random
import string


def randstr():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


fk1 = models.TestOneToMany.objects.create(name=randstr())

for x in range(100):
    print("go")
    models.TestModel.objects.create(
        name=randstr(),
        f1=randstr(),
        f2=randstr(),
        my_fk=fk1,
    )
