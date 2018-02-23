from django.db import models
from django.contrib.auth.models import User


class VcStatusName(models.Model):
    status_name_set = (
        (0, 'Новое'),
        (1, 'Просмотренное'),
        (2, 'Собеседование'),
        (3, 'Принят'),
        (4, 'НЕ принят'),
        (5, 'Архив')
    )

    status = models.PositiveSmallIntegerField('Статус резюме', choices=status_name_set, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Справочник: Статусы анкеты"
        verbose_name_plural = "Справочник: Статусы анкеты"

    def __str__(self):
        return '{}'.format(self.get_status_display())



class VcState(models.Model):
    date = models.DateTimeField('Дата создания', auto_now_add=True)
    vc = models.ForeignKey('candidate.Person', verbose_name='ID Person', on_delete=models.CASCADE)
    status = models.ForeignKey(VcStatusName, verbose_name='Статус', on_delete=models.SET_NULL, null=True)
    user_set = models.ForeignKey(User, related_name='setter', verbose_name='Установил статус', on_delete=models.SET_NULL, blank=True, null=True)
    user_responsible = models.ForeignKey(User, related_name='getter', verbose_name='Кому назначено', on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField('Комментарий', max_length=200, default='', blank=False, null=True)

    class Meta:
        verbose_name = "Статусы анкет"
        verbose_name_plural = "Статусы анкет"
        get_latest_by = "date"

    def __str__(self):
        return "{} - {}".format(self.vc.full_name, self.vc.position)

    def full_name(self):
        return self.vc.full_name
    full_name.short_description = 'ФИО'

    def position(self):
        return self.vc.position
    full_name.short_description = 'Должность'