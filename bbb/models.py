from django.db import models
from uuid import uuid4
import datetime
from django.core.validators import (RegexValidator, EmailValidator,
                                   URLValidator, MinLengthValidator,
                                   MaxValueValidator, MinValueValidator,
                                   MinLengthValidator, FileExtensionValidator)
from django.core.exceptions import ValidationError
import re

date = datetime.datetime.now()
year = date.year
month = date.month
day = date.day

class Usuarios(models.Model):
   class Meta:
      verbose_name_plural = 'Usuario'

   def validate_youtube_link(value):
      # Verifica se o URL é válido
      validate_url = URLValidator()
      try:
         validate_url(value)
      except ValidationError:
         raise ValidationError("O URL fornecido é inválido.")

      # Verifica se o URL é um link do YouTube
      youtube_regex = r'(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com|\.be)\/(?:watch\?v=|embed\/)?([a-zA-Z0-9\-_]+)'
      if not re.match(youtube_regex, value):
         raise ValidationError("O URL fornecido não é um link do YouTube.")

   id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
   registration_date = models.DateTimeField(default=date, null=True)
   full_name = models.CharField(
                              max_length=255,
                              null=False,
                              validators=[MinLengthValidator(10),
                                          RegexValidator(r'^[A-Za-z\sçáéíóúàâêôãõëöü ]+$',
                                                         message="Only insert letters"
                                          )]
                              )
   cpf = models.CharField(
                           max_length=15,
                           unique=True,
                           null=False,
                           help_text='Please insert in this format xxx.xxx.xxx-xx',
                           validators=[RegexValidator(r'^\d\d\d.\d\d\d.\d\d\d-\d\d$',
                                                      message="Wrong format to CPF xxx.xxx.xxx-xx"
                                    )]
                        )
   born_date = models.DateField(null=False,
                              validators=[MaxValueValidator(
                                 datetime.date(year-18, month, day)
                              ), MinValueValidator(
                                 datetime.date(year-70, month, day)
                              )]
                              )
   email = models.EmailField(
                           null=False,
                           help_text='Please insert in this format oi@oi.com',
                           validators=[EmailValidator(message="Wrong format to email oi@oi.com")]
                           )
   phone = models.CharField(
                           max_length=13,
                           null=False,
                           help_text='Please insert in this format xx xxxxx-xxxx',
                           validators=[RegexValidator(r'^\d\d \d\d\d\d\d-\d\d\d\d$',
                                                      message="Wrong format to Phone 12 34567-8901"
                                       )]
                           )
   state = models.CharField(max_length=2,
                           null=False,
                           validators=[MinLengthValidator(2),
                                       RegexValidator('^[A-Z ]+$',
                                                      message="Only insert letters"
                           )])
   city = models.CharField(max_length=255,
                           null=False,
                           validators=[MinLengthValidator(3),
                                       RegexValidator(r'^[A-Za-z\sçáéíóúàâêôãõëöü ]+$',
                                                      message="Only insert letters")]
                        )
   street = models.CharField(max_length=255,
                           null=False,
                           validators=[MinLengthValidator(7),
                                       RegexValidator(r'^[A-Za-z\sçáéíóúàâêôãõëöü ]+$',
                                                      message="Only insert letters"
                                       )]
                           )
   number_street = models.IntegerField(null=True)
   registration_video = models.URLField(max_length=200, validators=[validate_youtube_link])
