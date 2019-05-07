import json
import pytz
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.http import Http404, HttpResponse
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Q
from django.forms import formset_factory
from .vfunction import dict_alert_msg, convert_to_local_datetime
from datatable.forms import Basic_CRUD_Create_Form, EmployeeForm
from .models import Employee, ContactUs
from datetime import datetime, timedelta
# Call datatable properties


def register_view(request):
    employees = Employee.objects.all()
    return render(request, 'table.html', {'employees': employees})


def basic_crud_create_view(request):
    """Renders the basic crud create operation."""
    if request.method == 'GET':

        # Get contact us form to display
        form = Basic_CRUD_Create_Form()
        return render(request, 'basic_crud_create.html', {'form': form})

    data = dict()
    if request.method == 'POST':
        # Get the form data
        form = Basic_CRUD_Create_Form(request.POST)
        if form.is_valid():
            form.save()  # insert new row

            # Return some json response back to the user
            msg = """ Your data has been inserted successfully, thank you! """
            data = dict_alert_msg('True', 'Awesome!', msg, 'success')
        else:
            # Extract form.errors
            msg = None
            msg = [(k, v[0]) for k, v in form.errors.items()]
            data = dict_alert_msg('False', 'Oops, Error', msg, 'error')

        return JsonResponse(data)


def basic_crud_list_view(request):
    """
    This is the main Django Template to display the recent Basic CRUD
    table rows that you can manage using DataTable object.
    """
    if request.method == "GET":

        db_data = ContactUs.objects.filter(
            is_deleted=False
        ).order_by('-id')[:50]  # fetch the latest 50 rows

        return render(request, 'basic_crud_list.html', {'db_data': db_data})


def basic_crud_del_row_view(request):
    """To delete selected row data"""
    data = dict()
    if request.method == 'POST':
        row_id = request.POST.get('row_id')

        # Just update 'is_deleted=False' status of the row only
        ContactUs.objects.filter(
            id=row_id).update(is_deleted=True,
                              deleted_by=1,
                              deleted_date=timezone.now())

        # Return some json response back to the user
        msg = """Poof! Your selected data row has been deleted!"""
        data = dict_alert_msg('True', 'Success!', msg, 'success')
        return JsonResponse(data)


def basic_crud_dynamic_public_page_view(request, slug, id):
    """ return thr dynamic pubic page """
    if request.method == 'GET':
        db_data = ContactUs.objects.filter(is_deleted=False, id=id)
        if db_data.count():
            return render(request, 'basic_django_dynamic_public_page.html',
                          {'db_data': db_data})
        else:
            raise Http404()


def basic_crud_update_row_view(request, id):
    """Renders the Django edit form page and execute the update statement."""
    if request.method == "GET":

        # Get the selected row information
        db_data = ContactUs.objects.filter(id=id, is_deleted=False)

        if db_data:

            # Edit form data
            edit_data = ContactUs.objects.get(id=id, is_deleted=False)
            formEdit = Basic_CRUD_Create_Form(instance=edit_data)
            # print(formEdit)

            return render(request, 'basic_crud_update.html',
                          {'id': id,
                           'formEdit': formEdit
                           })
        else:
            raise Http404()

    data = dict()
    if request.method == "POST":

        # Get the  form modified data
        form_edit = Basic_CRUD_Create_Form(request.POST)
        id = request.POST.get('id')

        if form_edit.is_valid():

            # Check if the row still not deleted
            if ContactUs.objects.filter(id=id, is_deleted=False).exists():

                # Get the form edit instance
                update_data = ContactUs.objects.get(id=id, is_deleted=False)

                # Now, supply the form data to an instance
                form_edit = Basic_CRUD_Create_Form(
                    request.POST, instance=update_data)
                form_edit.save()  # Finally save the form data

                # Return some json response back to the user
                msg = """ Data has been modified successfully, thank you! """
                data = dict_alert_msg('True', 'Awesome!', msg, 'success')

            else:
                # Return some json response back to the user
                msg = """ Data no longer existed, update has been aborted! """
                data = dict_alert_msg('True', 'Update Failed!', msg, 'error')
        else:

            # Extract form.errors
            msg = None
            msg = [(k, v[0]) for k, v in form_edit.errors.items()]
            data = dict_alert_msg('False', 'Oops, Error', msg, 'error')

        return JsonResponse(data)


def basic_search_text_view(request):
    """ renders the basic search text """
    if request.method == 'POST':
        fsearch = request.POST.get('fsearch')

        data_lists = ContactUs.objects.filter(
            Q(is_deleted=False) & (
                Q(full_name__icontains=fsearch) |
                Q(email__icontains=fsearch) |
                Q(subject__icontains=fsearch) |
                Q(message__icontains=fsearch)
            )).order_by('id')[:50]
        fh_data = dict()
        fh_list = []

        for fh in data_lists:
            url = settings.BASE_URL + slugify(fh.full_name) + "-" + str(fh.id)
            trun_subject = fh.subject[:100] + '...'

            # Convert UTC datetime from db to user's local datetime.
            submitted_date = convert_to_local_datetime(fh.submitted)

            edit_url = settings.BASE_URL + \
                "basic_crud/" + str(fh.id) + "/change/"

            fh_list.append(
                {'full_name': (fh.full_name),
                 'subject': trun_subject,
                 'email': fh.email,
                 'submitted': submitted_date,
                 'id': fh.id,
                 'url': url,
                 'edit_url': edit_url
                 })

        fh_data = fh_list
        json_data = json.dumps(fh_data)
        return JsonResponse(json_data, safe=False)


def basic_search_dr_view(request):
    """Renders the basic search by date and time."""
    if request.method == "POST":

        # Get the date range values from the user input
        mStartDate = request.POST.get('mStartDate')
        mEndDate = request.POST.get('mEndDate')

        # Format date
        date_format = '%Y-%m-%d'

        unaware_start_date = datetime.strptime(mStartDate, date_format)
        aware_start_date = pytz.utc.localize(unaware_start_date)

        unaware_end_date = datetime.strptime(mEndDate, date_format
                                             ) + timedelta(days=1)
        aware_end_date = pytz.utc.localize(unaware_end_date)
        # Display data, using __range from Django's built-in functionality
        data_lists = ContactUs.objects.filter(
            is_deleted=False,
            submitted__range=(aware_start_date,
                              aware_end_date)
        ).order_by('-id')[:50]

        fh_data = dict()
        fh_list = []

        for fh in data_lists:
            url = settings.BASE_URL + slugify(fh.full_name) + "-" + str(fh.id)
            trun_subject = fh.subject[:100] + '...'

            # Convert UTC datetime from db to user's local datetime.
            submitted_date = convert_to_local_datetime(fh.submitted)

            edit_url = settings.BASE_URL + \
                "basic_crud/" + str(fh.id) + "/change/"

            fh_list.append(
                {'full_name': (fh.full_name),
                 'subject': trun_subject,
                 'email': fh.email,
                 'submitted': submitted_date,
                 'id': fh.id,
                 'url': url,
                 'edit_url': edit_url
                 })

        fh_data = fh_list
        json_data = json.dumps(fh_data)
        return JsonResponse(json_data, safe=False)


class ContactFormView(View):
    # We are creating a formset out of the EmployeeForm
    Contact_FormSet = formset_factory(EmployeeForm)
    # The Template name where we are going to display it
    template_name = "employees.html"

    # Overiding the get method
    def get(self, request, *args, **kwargs):
        # Creating an Instance of formset and putting it in context dict
        context = {
            'contact_form': self.Contact_FormSet(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        contact_formset = self.Contact_FormSet(self.request.POST)

        # Checking the if the form is valid
        if contact_formset.is_valid():
            # To save we have loop through the formset
            for contacts in contact_formset:
                # Saving in the contacts models
                contacts.save()

            return HttpResponse("data is submitted")

        else:
            context = {
                'contact_form': self.Contact_FormSet(),
            }

            return render(request, self.template_name, context)
