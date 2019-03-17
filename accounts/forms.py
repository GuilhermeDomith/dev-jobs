from django import forms
from .models import Profile
from django.contrib import messages 

class CompetenciasField(forms.MultiValueField):

    # Indica que este field serão múltiplos input de tipo hidden.
    widget=forms.MultipleHiddenInput()

    def __init__(self):
        super(CompetenciasField, self).__init__(
            required=False,
            require_all_fields=False,
            # Indeica que cada fied pode ser vazio.
            fields=[forms.CharField(required=False) for x in range(200)]
            )

    def compress(self, data_list):
        ''' Retorna a lista de competências '''
        # Remove as strings repetidas e vazias
        data_list = list(set(data_list))
        
        try: data_list.remove('')
        except: pass

        return data_list


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'vagas_desejadas']

    cpassword = forms.CharField(max_length=255)
    comp = CompetenciasField()
    vagas_desejadas = forms.CharField(required=False)
    first_name = forms.CharField(required=True)
    email = first_name = forms.CharField(required=True)

    def clean_cpassword(self):
        ''' Verifica se a comfirmação de senha é igual a senha. '''

        cpass = self.cleaned_data['cpassword']
        if self.cleaned_data['password'] != cpass:
            raise forms.ValidationError('A confirmação da senha deve ser igual a senha.')

        return cpass



