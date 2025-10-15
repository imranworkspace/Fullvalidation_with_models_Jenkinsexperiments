from django import forms
from django.core import validators
from .models import StudentModel
# for specific_fields
def start_with_i(value):
    raise forms.ValidationError('name should be starts with i')


class StudentForm(forms.Form):
    # name=forms.CharField(max_length=25,validators=[start_with_i],widget=forms.TextInput(attrs={'placeholder':'enter student name'}),
    name=forms.CharField(label='Student Name',label_suffix=':',max_length=25,widget=forms.TextInput(attrs={'placeholder':'enter student name'}),error_messages={'required':'Student Name required'})
    email=forms.EmailField(label='Email',label_suffix=':',widget=forms.EmailInput(attrs={'placeholder':'enter email'}),error_messages={'required':'Email required'})
    password=forms.CharField(label='Password',label_suffix=':',max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'enter password'}),error_messages={'required':'Password required'},validators=[validators.MinLengthValidator(8),validators.MaxLengthValidator(25)])
    pincode = forms.IntegerField(
        label='Pin code',
        min_value=100000,
        max_value=999999,
        error_messages={
            'min_value': 'Enter at least 6 digits',
            'max_value': 'Enter maximum 6 digits',
        },
        widget=forms.TextInput(attrs={'placeholder': '6 digit pincode'})
    )

    # Date-related fields
    dob = forms.DateField(
        label='Date Of Birth',
        required=False,
        help_text='Enter YYYY-MM-DD format',
        widget=forms.TextInput(attrs={'type':'date','placeholder': 'ex.1993/05/10'})
    )

    appointment_time = forms.TimeField(
        label='Appointment Time',
        required=False,
        widget=forms.TextInput(attrs={'type':'time','placeholder': 'ex.10:00'})
    )

    appointment_date = forms.DateField(
        label='Appointment Date',
        required=False,
        widget=forms.TextInput(attrs={'type':'date','placeholder': 'ex.1993/05/10'})
    )

    appointment_datetime = forms.DateTimeField(
        label='Appointment Date Time',
        required=False,
        widget=forms.TextInput(attrs={'type':'datetime-local','placeholder': 'ex.1993/05/10 10:00'})
    )

    is_agreed = forms.BooleanField(label='IsAgreed')
    agree_terms = forms.NullBooleanField(label='I Agreed')

    GENDER_CHOICE = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    INTERESTS_CHOICE = [
        ('cricket', 'Cricket'),
        ('football', 'Football'),
        ('reading', 'Reading')
    ]

    # Choice-related fields
    gender = forms.ChoiceField(
        label='Gender',
        choices=GENDER_CHOICE)
        
                            
    

    interests = forms.MultipleChoiceField(
        label='Your Interest',
        choices=INTERESTS_CHOICE,
        widget=forms.SelectMultiple(attrs={'placeholder': 'Select Multiple Interests'})
    )

    # File and URL fields
    profile_pic = forms.ImageField(
        label='Profile Pic',
        required=False,
        widget=forms.ClearableFileInput()
    )

    resume = forms.FileField(
        label='Upload Resume',
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Upload Your Resume'})
    )

    website = forms.URLField(
        label='Personal Website',
        required=False,
        widget=forms.URLInput(attrs={'placeholder': 'Enter website'})
    )

    # Other fields
    mobile_no = forms.RegexField(
        regex=r'^[6-9]\d{9}$',
        widget=forms.TextInput(attrs={'placeholder': 'Enter mobile number'}),
        error_messages={'invalid': 'Enter a valid 10-digit Indian mobile number starting with 6-9.'}
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        max_length=10,
        validators=[validators.MinLengthValidator(3)]
    )

    slug = forms.SlugField(label='Slug',widget=forms.TextInput(attrs={'placeholder':'enter slug'}))

    ip_address = forms.GenericIPAddressField(
        label='IP Address',
        protocol='both',
        unpack_ipv4=True,
        localize=True,
        widget=forms.TextInput(attrs={'placeholder': 'Your IPv4 or IPv6 address'})
    )

    rating = forms.DecimalField(
        label='Ratings',
        widget=forms.NumberInput(attrs={'placeholder': 'Enter rating'})
    )

    content = forms.CharField(
        label='Post-Content',widget=forms.Textarea(attrs={'placeholder':'Enter Multiple Line of Text'})
    )

    # marriedornot=forms.RadioSelect(label='Married or Not',widget=forms.TextInput(attrs={'type':"radio"}))
    MARRIED_CHOICES = [('True', 'Married'),('False', 'Unmarried')]

    marriedornot = forms.ChoiceField(
        label='Marital Status',
        choices=MARRIED_CHOICES,
        widget=forms.RadioSelect
    )

    # multiwidgets
    split_date_time = forms.SplitDateTimeField(
        label='Split Date and Time Field',
        widget=forms.SplitDateTimeWidget()
    )



     # for specific_fields
    '''def clean_name(self):
        nm=self.cleaned_data['name']
        if nm[0]!='i': 
            raise forms.ValidationError('name should be starts with i')
        return nm
    
    def clean_password(self):
        pw=self.cleaned_data['password']
        if len(pw)<8:
            raise forms.ValidationError('password length should be minimum 8 characters')
        return pw'''
    
    # for all fields 
    '''def clean(self):
        cleaned_data=super().clean()
        nm=cleaned_data.get('name')
        pw=cleaned_data.get('password')
        if nm and nm[0]!='i': 
            self.add_error('name','name should be starts with i')
        
        if pw and len(pw)<8:
            self.add_error('password','password length should be minimum 8 characters')

        return cleaned_data  
'''

'''class LoginForm(forms.Form):
    name=forms.CharField(label='Student Name',label_suffix=':',max_length=25,widget=forms.TextInput(attrs={'placeholder':'enter student name'}),error_messages={'required':'Student Name required'})
    password=forms.CharField(label='Password',label_suffix=':',max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'enter password'}),error_messages={'required':'Password required'})
'''

class LoginForm(forms.ModelForm):
    class Meta:
        model=StudentModel
        fields=['name','password']
        labels={'name':'Name','email':'Email Address','password':'Password'}
        error_messages={'name':{'required':'Name is required'},'email':{'required':'Email is required'},
                        'password':{'required':'Password is required'}}
        widgets={'name':forms.TextInput(attrs={'placeholder':'enter student name'}),
                 'email':forms.EmailInput(attrs={'placeholder':'enter email address'}),
                 'password':forms.PasswordInput(attrs={'placeholder':'enter password'})
                 }    