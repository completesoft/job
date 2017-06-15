from django.db import models


class Person(models.Model):

    fill_date = models.DateField('Дата заполнения',auto_now_add=True)

    position = models.CharField('Должность',max_length=50)
    full_name = models.CharField('Фамилия, имя, отчество',max_length=100)
    birthday = models.DateField('Дата рождения', null=True, blank=True)

    gender_set = (
        ('0', 'Мужской'),
        ('1', 'Женский'),
    )
    gender = models.CharField('Пол', max_length=1, choices=gender_set, default=2, blank=True)

    registration = models.TextField('Адрес прописки', default='', blank=True)
    residenceBool = models.BooleanField('Адрес проживания совпадает с адресом прописки', default=True, blank=True)

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

    # Section: Other
        # referrer first
    ref1_full_name = models.CharField('Фамилия, имя, отчество',max_length=100, default='', blank=True)
    ref1_position = models.CharField('Должность',max_length=50, default='', blank=True)
    ref1_workplace = models.CharField('Место работы', max_length=100, default='', blank=True)
    ref1_phone = models.CharField('Мобильный телефон',max_length=15, default='', blank=True)
        # referrer second
    ref2_full_name = models.CharField('Фамилия, имя, отчество', max_length=100, default='', blank=True)
    ref2_position = models.CharField('Должность', max_length=50, default='', blank=True)
    ref2_workplace = models.CharField('Место работы', max_length=100, default='', blank=True)
    ref2_phone = models.CharField('Мобильный телефон', max_length=15, default='', blank=True)

    source_about_as = models.CharField('Из какого источника узнали о вакансии',max_length=50, default='', blank=True)
    add_details = models.TextField('Дополнительне данные', default='', blank=True)

    start = models.DateField('Могу начать работать', null=True, blank=True)

    class Meta():
        verbose_name = 'Соискатель'
        verbose_name_plural = 'Соискатели'

    def __str__(self):
        return '{} : {}'.format(self.full_name, self.position)



class Residence_address(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    residence = models.TextField('Адрес проживания', default='', blank=True)

    class Meta():
        verbose_name = 'Адрес проживания'
        verbose_name_plural = 'Адрес проживания'

    def __str__(self):
        return '{} {}'.format('адрес', self.person.full_name)

class Education(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    start_date = models.DateField('Начало обучения', null=True, blank=True)
    end_date = models.DateField('Окончание обучения', null=True, blank=True)
    name_institute = models.TextField('Название учебного заведения, факультет, форма обучения', default='', blank=True)
    qualification = models.CharField('Специальность', max_length=50, default='', blank=True)

    class Meta():
        verbose_name = 'Образование и специальность'
        verbose_name_plural = 'Образование и специальность'

    def __str__(self):
        return '{} {}'.format('Образование', self.person.full_name)


class Experience(models.Model):

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    exp_start_date = models.DateField('Период работы с', null=True, blank=True)
    exp_end_date = models.DateField('Период работы по', null=True, blank=True)
    workplace = models.CharField('Место работы', max_length=100, default='', blank=True)
    exp_position = models.CharField('Должность', max_length=100, default='', blank=True)
    responsibility = models.TextField('Обязанности', max_length=100,default='', blank=True)
    exp_salary = models.IntegerField('Зарплата', default=0, blank=True)
    reason_leaving = models.TextField('Причина увольнения',max_length=100, default='', blank=True)

    class Meta():
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'

    def __str__(self):
        return '{} {}'.format('Опыт работы', self.person.full_name)