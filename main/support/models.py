from django.db import models

# مدل مربوط به تیکت‌های پشتیبانی
class SupportTicket(models.Model):
    ticket_id = models.AutoField(primary_key=True)  # شناسه یکتا برای هر تیکت (کلید اصلی)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)  # ارتباط با مدل کاربر (در صورت حذف کاربر، تیکت هم حذف می‌شود)
    subject = models.CharField(max_length=255)  # موضوع تیکت
    description = models.TextField()  # توضیحات تیکت
    status = models.CharField(
        max_length=50,
        choices=[('open', 'Open'), ('closed', 'Closed')],
        default='open'
    )  # وضعیت تیکت (باز یا بسته)
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد تیکت (به صورت خودکار)
    updated_at = models.DateTimeField(auto_now=True)  # زمان آخرین بروزرسانی (به صورت خودکار)

    def __str__(self):
        # نمایش تیکت به صورت رشته‌ای (برای پنل ادمین و ...)
        return f'Ticket {self.ticket_id} - {self.subject}'

    class Meta:
        verbose_name = 'Support Ticket'  # نام نمایشی مفرد
        verbose_name_plural = 'Support Tickets'  # نام نمایشی جمع
        ordering = ['-created_at']  # ترتیب پیش‌فرض بر اساس زمان ایجاد (جدیدترین اول)
        indexes = [
            models.Index(fields=['status']),  # ایندکس روی وضعیت برای جستجوی سریع‌تر
            models.Index(fields=['created_at']),  # ایندکس روی زمان ایجاد
        ]


# مدل مربوط به پیام‌های هر تیکت پشتیبانی
class SupportMessage(models.Model):
    message_id = models.AutoField(primary_key=True)  # شناسه یکتا برای هر پیام (کلید اصلی)
    ticket = models.ForeignKey(
        SupportTicket,
        related_name='messages',
        on_delete=models.CASCADE
    )  # ارتباط با تیکت (در صورت حذف تیکت، پیام هم حذف می‌شود)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)  # کاربر ارسال‌کننده پیام
    message = models.TextField()  # متن پیام
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد پیام (به صورت خودکار)

    def __str__(self):
        # نمایش پیام به صورت رشته‌ای
        return f'Message {self.message_id} - Ticket {self.ticket.ticket_id}'

    class Meta:
        verbose_name = 'Support Message'  # نام نمایشی مفرد
        verbose_name_plural = 'Support Messages'  # نام نمایشی جمع
        ordering = ['-created_at']  # ترتیب پیش‌فرض بر اساس زمان ایجاد (جدیدترین اول)
        indexes = [
            models.Index(fields=['ticket']),  # ایندکس روی تیکت برای جستجوی سریع‌تر پیام‌های هر تیکت
            models.Index(fields=['created_at']),  # ایندکس روی زمان ایجاد
        ]