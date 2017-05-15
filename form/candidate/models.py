from django.db import models

# Create your models here.

class Person(models.Model):

    class Meta():
        verbose_name = 'Соискатель'
        verbose_name_plural = 'Соискатели'


    fill_date = models.DateField('Дата заполнения',auto_now_add=True)

    position = models.CharField('Должность',max_length=50)
    full_name = models.CharField('Фамилия, имя, отчество',max_length=100)
    birthday = models.DateField('Дата рождения', null=True, blank=True)

    sex_set = (
        (0, 'Мужской'),
        (1, 'Женский'),
        (2, 'Не указан')
    )
    sex = models.IntegerField('Пол', choices=sex_set, default=2, blank=True)

    registration = models.TextField('Адрес прописки', default='', blank=True)
    residence = models.BooleanField('Адрес проживания совпадает с адресом прописки', default=True, blank=True)

    phone = models.CharField('Мобильный телефон',max_length=15, default='', blank=True)

    children = models.BooleanField('Дети', default=False)

    passp_number = models.CharField('Серия, номер паспорта',max_length=20, default='', blank=True)
    passp_issue = models.CharField('Кем выдан',max_length=50, default='', blank=True)
    passp_date = models.DateField('Дата выдачи', null=True, blank=True)

    army = models.BooleanField('Служба в армии', default=False)
    army_id = models.BooleanField('Военный билет', default=False)
    driver_lic = models.BooleanField('Водительское удостоверение', default=False)
    car = models.BooleanField('Личный автомобиль', default=False)

    advantage = models.TextField('Ваши сильные стороны', default='', blank=True)
    disadvantage = models.TextField('Ваши слабые стороны', default='', blank=True)
    convicted = models.BooleanField('Привлекались ли Вы к ответственности (административной, уголовной и т.д.)', default=False, blank=True)
    illness = models.BooleanField('Страдаете ли Вы хроническими заболеваниями?', default=False, blank=True)
    salary = models.IntegerField('Какую заработную плату Вы хотите получать?', default=0, blank=True)

    def __str__(self):
        return '{} {}'.format(self.full_name, self.position)



class Residence_address(models.Model):

    class Meta():
        verbose_name = 'Адрес проживания'
        verbose_name_plural = 'Адрес проживания'

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    residence = models.TextField('Адрес проживания', default='', blank=True)


class Experience(models.Model):

    class Meta():
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    start_date = models.DateField('Период работы с', null=True, blank=True)
    end_date = models.DateField('Период работы по', null=True, blank=True)
    workplace = models.CharField('Место работы', max_length=100, default='', blank=True)
    responsibility = models.TextField('Обязанности', default='', blank=True)
    salary = models.IntegerField('Зарплата', default=0, blank=True)
    reason_leaving = models.TextField('Причина увольнения', default='', blank=True)






