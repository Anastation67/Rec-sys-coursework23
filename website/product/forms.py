
from django import forms
from .models import Supplier

class AddForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('company_name', 'reg_number', 'full_company_name', 'address', 'head_name', 'phone', 'email', 'reg_date', 'company_age', 'industry_type', 'summary_indicator', 'share_capital', 'sale_articles', 'important_info')
