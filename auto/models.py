from django.db import models

STAT_UNPAID   = 'unpaid'
STAT_PEND     = 'pending'
STAT_RUN      = 'running'
STAT_COMP     = 'completed'

class Action(models.Model):
    label = models.CharField(max_length=150)
    class Meta:
        verbose_name = 'Task Action'
        verbose_name_plural = 'Task Actions'
    
    def __str__(self):
        return self.label

class TaskPackage(models.Model):
    number = models.IntegerField()
    price = models.FloatField()
    action = models.ForeignKey('Action', on_delete=models.CASCADE, related_name='packages')
    class Meta:
        verbose_name_plural = 'Task Packages'
    
    def __str__(self):
        return "%s : %d" % (self.action.label, self.number)

class Task(models.Model):
    entity_ident = models.CharField(max_length=200, verbose_name='username')
    action = models.ForeignKey('Action', on_delete=models.CASCADE, related_name='tasks')
    package = models.ForeignKey('TaskPackage',on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=(
                                (STAT_UNPAID, 'Unpaid'), 
                                (STAT_PEND, 'Pending'),
                                (STAT_RUN, 'Running'),
                                (STAT_COMP, 'Completed')), default=STAT_PEND )
    
    random_token = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    member_count = models.IntegerField()
    target_member_count = models.IntegerField()
    invoice = models.OneToOneField('Invoice', on_delete=models.CASCADE,  related_name='task')

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['created_at']

class RunningTask(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='running_tasks')
    class Meta:
        ordering = ('-created_at',)

class Invoice(models.Model):
    expected_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Payment(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    transaction_time = models.DateTimeField(auto_now_add=True)
