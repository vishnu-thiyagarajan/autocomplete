from django.db import models

# Create your models here.


class currency_convertion(models.Model):
    CAD = "CAD"
    HKD = "HKD"
    LVL = "LVL"
    PHP = "PHP"
    DKK = "DKK"
    HUF = "HUF"
    CZK = "CZK"
    AUD = "AUD"
    RON = "RON"
    SEK = "SEK"
    IDR = "IDR"
    INR = "INR"
    BRL = "BRL"
    RUB = "RUB"
    LTL = "LTL"
    JPY = "JPY"
    THB = "THB"
    CHF = "CHF"
    SGD = "SGD"
    PLN = "PLN"
    BGN = "BGN"
    TRY = "TRY"
    CNY = "CNY"
    NOK = "NOK"
    NZD = "NZD"
    ZAR = "ZAR"
    USD = "USD"
    MXN = "MXN"
    EEK = "EEK"
    GBP = "GBP"
    KRW = "KRW"
    MYR = "MYR"
    HRK = "HRK"
    choice = [(CAD, "CAD"),
              (HKD, "HKD"),
              (LVL, "LVL"),
              (PHP, "PHP"),
              (DKK, "DKK"),
              (HUF, "HUF"),
              (CZK, "CZK"),
              (AUD, "AUD"),
              (RON, "RON"),
              (SEK, "SEK"),
              (IDR, "IDR"),
              (INR, "INR"),
              (BRL, "BRL"),
              (RUB, "RUB"),
              (LTL, "LTL"),
              (JPY, "JPY"),
              (THB, "THB"),
              (CHF, "CHF"),
              (SGD, "SGD"),
              (PLN, "PLN"),
              (BGN, "BGN"),
              (TRY, "TRY"),
              (CNY, "CNY"),
              (NOK, "NOK"),
              (NZD, "NZD"),
              (ZAR, "ZAR"),
              (USD, "USD"),
              (MXN, "MXN"),
              (EEK, "EEK"),
              (GBP, "GBP"),
              (KRW, "KRW"),
              (MYR, "MYR"),
              (HRK, "HRK")]

    date = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False)
    target_currency = models.CharField(max_length=3, choices=choice, default='INR', null=False, blank=False)
    base_currency = models.CharField(max_length=3, choices=choice, default='USD', null=False, blank=False)
    predicted_value = models.DecimalField(null=False, blank=False, max_digits=10,
                                          default=0.00000, decimal_places=5)

    def __str__(self):  # def __str__(self):
        return str(self.date) + '(' + self.base_currency + '-' + self.target_currency + ')'
