# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Types(models.Model):
    typee = models.BigIntegerField(primary_key=True, unique=True, db_column='id_type')
    # id_type = models.AutoField(primary_key=True)
    name_type = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'types'

class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    login = models.CharField(max_length=11)
    fio = models.CharField(max_length=100)
    password = models.CharField(max_length=11)  # Field renamed because it was a Python reserved word.
    role = models.IntegerField()
    srok = models.IntegerField()
    tel = models.CharField(max_length=64)
    is_active = models.IntegerField(db_comment='0-уволен,1-работает\t')
    last_login = models.DateTimeField(null=True, verbose_name="last login", blank=True)

    class Meta:
        managed = False
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Districts(models.Model):
    region_id = models.IntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'districts'

class RegionStatuses(models.Model):
    text = models.CharField(max_length=55)
    class_field = models.CharField(db_column='class', max_length=55)  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'region_statuses'

class RequestStatuses(models.Model):
    name = models.CharField(max_length=255)
    closed = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_statuses'


class Regions(models.Model):
    id_region = models.AutoField(primary_key=True)
    name_region = models.CharField(max_length=100)
    timezone = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'regions'

class RegionDescriptions(models.Model):
    # region_id = models.PositiveIntegerField(unique=True)
    # region_status_id = models.IntegerField()
    region = models.ForeignKey(Regions, to_field='id_region', default=0, on_delete=models.CASCADE)
    region_status = models.ForeignKey(RegionStatuses, to_field='id', default=0, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    is_moving_out = models.IntegerField(db_comment='0-не выезжаем, 1-выезжаем')

    class Meta:
        managed = False
        db_table = 'region_descriptions'


class Attachments(models.Model):
    email = models.ForeignKey('Emails', models.DO_NOTHING)
    original_name = models.CharField(max_length=500)
    filename = models.CharField(unique=True, max_length=500)

    class Meta:
        managed = False
        db_table = 'attachments'

class StatusJob(models.Model):
    # id_status_job = models.AutoField(primary_key=True)
    status_job = models.BigIntegerField(primary_key=True, unique=True, db_column='id_status_job')
    name_status = models.CharField(max_length=25)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'status_job'

class Company(models.Model):
    # id_company = models.BigIntegerField(primary_key=True, unique=True, null=False, auto_created=True, serialize=False, verbose_name='id_company', db_column='id_company')
    company = models.BigIntegerField(primary_key=True, unique=True, db_column='id_company')
    name_company = models.CharField(max_length=5000)
    company_site = models.CharField(max_length=200)
    region = models.ForeignKey(Regions, db_column='id_region', to_field='id_region', default=0, on_delete=models.SET_DEFAULT)
    district = models.ForeignKey(Districts, db_column='id_district', to_field='id', default=0, on_delete=models.SET_DEFAULT)
    is_primary = models.IntegerField()
    educational_municipal_status_id = models.IntegerField()
    date_create = models.DateTimeField()
    date_modify = models.DateTimeField()
    manager = models.ForeignKey(Users, db_column='id_manager', to_field='id_user', default=0, on_delete=models.SET_DEFAULT)
    phone = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    address = models.CharField(max_length=5000)
    director = models.CharField(max_length=1000)
    status_job = models.ForeignKey(StatusJob, db_column='id_status_job', default=0, on_delete=models.SET_DEFAULT)
    typee = models.ForeignKey(Types, db_column='id_type', default=0, on_delete=models.SET_DEFAULT)
    cont_pers = models.CharField(max_length=1000)
    phone_cont = models.CharField(max_length=1000)
    other_inf = models.TextField()
    id_company_crm2 = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'company'

class Comments(models.Model):
    id_comment = models.BigIntegerField(
        primary_key=True,
        unique=True,
        null=False,
        auto_created=True,
        serialize=False,
        verbose_name='id_comment'
    )
    
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        db_column='id_company'
    )
    id_user = models.IntegerField()
    phone_from = models.CharField(max_length=25, db_comment='телефон с которого сделан звонок (только для tomoru)')
    date_comment = models.DateTimeField()
    comment = models.TextField()
    result = models.IntegerField()
    task_ruk_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comments'
        
class CompanyPrivileges(models.Model):
    company_id = models.IntegerField()
    text = models.TextField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'company_privileges'

class EmailCompanies(models.Model):
    email = models.ForeignKey('Emails', models.DO_NOTHING)
    company = models.ForeignKey(Company, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'email_companies'
        unique_together = (('email', 'company'),)

class Requests(models.Model):
    company = models.ForeignKey(Company, models.DO_NOTHING)
    # user_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(Users, models.CASCADE)
    status = models.ForeignKey(RequestStatuses, models.DO_NOTHING, blank=True, null=True)
    title = models.TextField()
    company_name = models.CharField(max_length=5000)
    company_phone = models.CharField(max_length=1000, blank=True, null=True)
    company_address = models.CharField(max_length=5000, blank=True, null=True)
    company_email = models.CharField(max_length=1000, blank=True, null=True)
    company_director = models.CharField(max_length=1000, blank=True, null=True)
    company_contact = models.CharField(max_length=1000, blank=True, null=True)
    company_contact_phone = models.CharField(max_length=1000, blank=True, null=True)
    contract_info = models.TextField(blank=True, null=True)
    contract_name = models.CharField(max_length=1000)
    contract_subject = models.TextField()
    contract_start = models.DateTimeField()
    contract_time = models.TextField()
    contract_agreement = models.CharField(max_length=1000)
    contract_population = models.CharField(max_length=1000)
    contract_owner = models.CharField(max_length=1000)
    road_length = models.CharField(max_length=1000)
    contract_terms = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'requests'

class Emails(models.Model):
    user_id = models.IntegerField()
    subject = models.CharField(max_length=500)
    message = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'emails'


class EmailsQueue(models.Model):
    email_id = models.IntegerField()
    company_id = models.IntegerField()
    send_date = models.DateField()
    updated_at = models.DateTimeField()
    is_sended = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'emails_queue'
        db_table_comment = 'сообщения к отправке'


class Logstore(models.Model):
    user_id = models.IntegerField()
    model = models.CharField(max_length=50, blank=True, null=True)
    action = models.CharField(max_length=50)
    crud = models.CharField(max_length=5)
    data = models.TextField(blank=True, null=True)
    logged_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'logstore'


class ProjectStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'project_status'


class Projects(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'

class CompanyProjects(models.Model):
    company = models.ForeignKey(Company, to_field='company', db_column='company_id', related_name='company_projects', on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, to_field='id', db_column='project_id', on_delete=models.CASCADE)
    status = models.ForeignKey(ProjectStatus, to_field='id', db_column='status_id', on_delete=models.CASCADE)

    year = models.TextField(blank=True, null=True)
    contract_ok = models.IntegerField(blank=True, null=True)
    act_ok = models.IntegerField(blank=True, null=True)
    project_ok = models.IntegerField(blank=True, null=True)
    more = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'company_projects'
        unique_together = (('company', 'project'),)


class Reminders(models.Model):
    id_reminder = models.AutoField(primary_key=True)
    reminder = models.TextField()
    id_user = models.IntegerField()
    # id_company = models.IntegerField()
    company = models.ForeignKey(Company, models.DO_NOTHING, db_column='id_company')
    date_reminder = models.DateField()
    check_reminder = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'reminders'


class RequestComments(models.Model):
    request = models.ForeignKey(Requests, models.CASCADE)
    user_id = models.IntegerField(blank=True, null=True)
    text = models.TextField()
    status = models.BooleanField()
    # status = models.ForeignKey('RequestStatuses', models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'request_comments'


class RequestReminders(models.Model):
    # request = models.ForeignKey('Requests', models.DO_NOTHING)
    request = models.ForeignKey(Requests, models.CASCADE)
    user_id = models.IntegerField(blank=True, null=True)
    text = models.TextField()
    status = models.IntegerField()
    due_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'request_reminders'




class Tasks(models.Model):
    id_task = models.AutoField(primary_key=True)
    task = models.TextField()
    id_user_isp = models.IntegerField()
    id_user_ruk = models.IntegerField()
    date_task = models.DateField()
    date_task_end = models.DateField()
    check_task = models.CharField(max_length=2)
    id_company = models.IntegerField(blank=True, null=True)
    id_comment = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tasks'


class TasksPom(models.Model):
    id_task = models.AutoField(primary_key=True)
    task = models.TextField()
    id_user_isp = models.IntegerField()
    id_user_ruk = models.IntegerField()
    date_task = models.DateField()
    date_task_end = models.DateTimeField(blank=True, null=True)
    date_task_check = models.DateField(blank=True, null=True)
    check_task = models.CharField(max_length=2)
    id_company = models.IntegerField(blank=True, null=True)
    och = models.IntegerField()
    id_comment = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tasks_pom'


class UserCompanyPrivileges(models.Model):
    user_id = models.IntegerField()
    privilege_id = models.IntegerField()
    company_id = models.IntegerField()
    viewed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_company_privileges'
        unique_together = (('user_id', 'privilege_id', 'company_id'),)



