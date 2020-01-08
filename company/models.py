from django.db import models
from django.urls import reverse

#customer company list
class company(models.Model):
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=32)
    COMPANY_TYPE = (
        ('a', '媒體業'),
        ('b', '服務業'),
        ('c', 'AI公司'),
        ('d', '政府單位'),
        ('e', '教育機構'),
        ('z', '其他'),
    )
    type = models.CharField(max_length=1, choices=COMPANY_TYPE, blank=True)
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('company_detail', args=[str(self.id)])

#customer profile list
class profile(models.Model):
    name = models.CharField(max_length=32)
    department = models.CharField(max_length=32, blank=True)
    title = models.CharField(max_length=32, blank=True)
    email = models.EmailField(max_length=128, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    description = models.CharField(max_length=128, blank=True)
    company = models.ForeignKey('company', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile_detail', args=[str(self.id)])

#project list
class project(models.Model):
    company = models.ForeignKey('company', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=32)
    product = models.CharField(max_length=32, blank=True)
    member = models.CharField(max_length=128, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_update = models.DateField(null=True, blank=True)
    STATUS_TYPE = (
        ('a', '拜訪'),
        ('b', '報價'),
        ('c', '訂單'),
        ('d', '設計中'),
        ('e', '交貨'),
        ('z', '結案'),
    )
    status = models.CharField(max_length=1, choices=STATUS_TYPE, blank=True)
    detail = models.TextField()
    technical = models.CharField(max_length=256, blank=True)
    sales = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])
    #replace \n etc to <br>
    #def detail_br(self):
    #    detail_br = self.detail
    #    for i in ["\r\n", "\n\r", "\n", "\r"]:
    #        detail_br = detail_br.replace(i, '<br>')
    #    return detail_br

#staff list
class staff(models.Model):
    name = models.CharField(max_length=32)
    DEPARTMENT_TYPE = (
        ('a', '技術部'),
        ('b', '業務部'),
        ('c', '管理部'),
    )
    department = models.CharField(max_length=1, choices=DEPARTMENT_TYPE, blank=True)
    boss0 = models.IntegerField(default=0, blank=True)
    boss1 = models.IntegerField(default=0, blank=True)
    boss2 = models.IntegerField(default=0, blank=True)

    class Meta:
        permissions = (("can_check_others", "has staffs work for self"),)

    def __str__(self):
        return self.name

#report list
class report(models.Model):
    staff_id = models.ForeignKey('staff', on_delete=models.SET_NULL, null=True)
    date_app = models.DateField(null=True, blank=True)
    work = models.TextField()
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    b0 = models.IntegerField(default=0, blank=True)
    date_b0 = models.DateField(null=True, blank=True)
    b1 = models.IntegerField(default=0, blank=True)
    date_b1 = models.DateField(null=True, blank=True)
    b2 = models.IntegerField(default=0, blank=True)
    date_b2 = models.DateField(null=True, blank=True)
    STATUS_TYPE = (
        ('a', '暫存中'),
        ('b', '申請中'),
        ('c', '已核准'),
        ('d', '已駁回'),
    )
    status = models.CharField(max_length=1, choices=STATUS_TYPE, blank=True)
    comment = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return str(self.staff_id)

    def get_absolute_url(self):
        return reverse('report_detail', args=[str(self.id)])
