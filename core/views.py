from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import *
from .models import *
from .utils import *
from django.views.generic import TemplateView, FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.http import JsonResponse
import json



class ContainerListView(View):
    """
    View for displaying a list of containers.
    """

    def get(self, request):
        """
        Renders the tables page with a list of containers.
        """
        containers = Container.objects.all()
        return render(request, 'tables.html', {'containers': containers})


class CreateContainerView(View):
    """
    View for creating a new container.
    """

    def get(self, request):
        """
        Renders the container creation form.
        """
        form = ContainerForm()
        vendors = Vendor.objects.all()
        return render(request, 'containerform.html', {'form': form, 'vendors': vendors})

    def post(self, request):
        """
        Handles POST request to create a new container.
        """
        form = ContainerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('container_list')
        else:
            vendors = Vendor.objects.all()
            return render(request, 'containerform.html', {'form': form, 'vendors': vendors})


class UpdateContainerView(View):
    """
    View for updating an existing container.
    """

    def get(self, request, pk):
        """
        Renders the container update form.
        """

        container = get_object_or_404(Container, pk=pk)
        form = ContainerForm(instance=container)
        vendors = Vendor.objects.all()
        log_exists = False
        if Log.objects.filter(container=container).exists():
            log_exists=True

        return render(request, 'containerform.html', {'form': form, 'vendors': vendors, 'log_exists':log_exists})


    def post(self, request, pk):
        """
        Handles POST request to update an existing container.
        """
        container = get_object_or_404(Container, pk=pk)
        form = ContainerForm(request.POST, instance=container)
        if form.is_valid():
            form.save()
            return redirect('container_list')
        else:
            vendors = Vendor.objects.all()
            return render(request, 'containerform.html', {'form': form, 'vendors': vendors})


class DeleteContainerView(View):
    """
    View for deleting a container.
    """

    def post(self, request, pk):
        """
        Handles POST request to delete a container.
        """
        container = get_object_or_404(Container, pk=pk)
        container.delete()
        return redirect('container_list')

    def delete(self, request, pk):
        """
        Handles DELETE request to delete a container.
        """
        container_obj = get_object_or_404(Container, pk=pk)
        container_obj.delete()
        return JsonResponse({'message': 'container deleted successfully'})

class UpdateContainerReportView(View):
    """
    View for updating container records.
    """

    def put(self, request):
        try:
            data = json.loads(request.body)
            if data:
                try:
                    con_data = Container.objects.get(id=data['cont_id'])
                except Container.DoesNotExist:
                    return JsonResponse({'error': f'Container does not exist'}, status=404)
                con_data.total_pieces = data['total_pieces']
                con_data.total_cbm = data['total_cbm']
                con_data.a_navg = data['a_navg']
                con_data.save()
            return JsonResponse({'message': 'container updated successfully', 'total_pieces':data['total_pieces'], 'total_cbm':data['total_cbm'], 'a_navg':data['a_navg']})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class LogsFormView(View):
    """
    View for handling logs form submissions.
    """

    def get(self, request):
        """
        Renders the logs form page.
        """
        form = LogForm()
        return render(request, 'logsform.html', {'form': form})

    def post(self, request):
        """
        Handles POST request for logs form submission.
        """
        # Get container object based on the provided container id
        container_id = request.POST.get('container')
        container = Container.objects.get(id=container_id)

        if Log.objects.filter(container=container).exists():
            return redirect('update_container', container_id)

        errors = []

        reference_id = 1

        for _ in range(container.pieces):
            data = request.POST.copy()

            data['reference_id'] = reference_id

            form = LogForm(data)

            if form.is_valid():
                form.save()
            else:
                errors.append(form.errors)

            reference_id += 1

        return redirect('update_container', container_id)

class LogsListView(View):
    def get(self, request):
        """Handles GET request to display log."""
        logs = Log.objects.all()
        return render(request, 'logstables.html', {'logs': logs})

class ContainerLogsView(View):
    def get(self, request, container_id):
        logs = Log.objects.filter(container_id=container_id)
        context = {
            'logs': logs,
        }
        return render(request, 'container_logs.html', context)

class UpdateLogsView(View):
    """
    View for updating log records.
    """

    def get(self, request):
        """
        Renders the form for updating a log record.
        """
        log = get_object_or_404(Log)
        form = LogForm(instance=log)
        return render(request, 'logsform.html', {'form': form, 'log': log})

    def put(self, request):
        try:
            data = json.loads(request.body)
            for log_id, values in data.items():
                try:
                    if log_id != "cont_id":
                        log = Log.objects.get(id=log_id)
                        log.length = values[0]
                        log.girth = values[1]
                        log.cft = values[2]
                        log.cbm = values[3]
                        log.save()
                except Log.DoesNotExist:
                    return JsonResponse({'error': f'Log with id {log_id} does not exist'}, status=404)

            if 'cont_id' in data:
                container_id = data['cont_id']
                container = Container.objects.get(id=container_id)
                total_cbm, total_pieces, net_avg = container.recompute_totals()

                return JsonResponse(
                    {'message': 'Logs updated successfully', 'total_cbm': total_cbm, 'total_pieces': total_pieces,
                     'net_avg': net_avg})
            else:
                return JsonResponse({'error': 'Container ID is missing from the request'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class DeleteLogsView(View):
    """
    View for deleting a container logs.
    """

    def get(self, request, pk):
        """
        Renders the confirmation page for deleting a container.
        """
        log = get_object_or_404(Log, pk=pk)
        return render(request, 'logdelete.html', {'log': log})

    def post(self, request, pk):
        """
        Handles POST request to delete a container log.
        """
        log = get_object_or_404(Log, pk=pk)
        log.delete()
        return redirect('container_list')


class FinishedLogsInfoView(View):
    """
    View for creating a new FinishedLogsInfo.
    """
    def get(self, request):
        """
        Renders the form to create a new FinishedLogsInfo.
        """

        finishedlogs = FinishedLogForm()

        return render(request, 'containerform.html', {'finishedlogs': finishedlogs})

    def post(self, request):
        """
        Handles POST request to create or update FinishedLogsInfo.
        """
        data = json.loads(request.body)
        log_ids = data["log_id"]
        finished_logs = data["finished_log"]
        for finished_log_data in finished_logs:
            finished_log_id = finished_log_data["id"]
            if not str(finished_log_id).startswith("#"):
                if FinishedLog.objects.filter(id=finished_log_id, log_id=log_ids).exists():
                    finished_log_instance = FinishedLog.objects.get(id=finished_log_id, log_id=log_ids)
                    finished_log_instance.length = finished_log_data["length"]
                    finished_log_instance.width = finished_log_data["width"]
                    finished_log_instance.thickness = finished_log_data["thickness"]
                    finished_log_instance.cft = finished_log_data["cft"]
                    finished_log_instance.save()
            else:
                next_reference_id = 1
                if FinishedLog.objects.filter(log_id=log_ids).exists():
                    latest_finished_log = FinishedLog.objects.filter(log_id=log_ids).order_by(
                        '-reference_id').first()
                    next_reference_id = latest_finished_log.reference_id + 1
                FinishedLog.objects.create(log_id=log_ids, length=finished_log_data["length"],
                                           width=finished_log_data["width"], thickness=finished_log_data["thickness"], cft=finished_log_data["cft"],reference_id=next_reference_id)


        return redirect('container_list')


class FinishedLogsView(View):
    def get(self, request):
        id = request.GET.get('log_id')
        fin_logs = FinishedLog.objects.filter(log_id=id).values()
        logs_list = list(fin_logs)
        return JsonResponse(logs_list, safe=False)

class FinishedListView(View):
    def get(self, request):
        """Handles GET request to display finished log list."""

        finished_log = FinishedLog.objects.all()

        return render(request, 'finishedlogstable.html', {'finishedlog': finished_log})


class FinishedLogsList(View):
    def get(self, request):
        fin_log = []
        con_id = request.GET.get('cont_id')

        logs_data = Log.objects.filter(container_id=con_id).prefetch_related('finishedlog_set')

        for log in logs_data:
            for f_log in log.finishedlog_set.all():
                data = {
                    'log_no': log.reference_id,
                    'finished_log_no': f_log.reference_id,
                    'length': float(f_log.length),
                    'width': float(f_log.width),
                    'thickness': float(f_log.thickness),
                    'cft': float(f_log.cft)
                }
                fin_log.append(data)

        return JsonResponse(fin_log, safe=False)

class DeleteFinishedlogs(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            finish_log_id = data.get('fin_log_id')
            if finish_log_id:
                finished_log = FinishedLog.objects.get(id=finish_log_id)
                finished_log.delete()
                return redirect('container_list')
            else:
                return JsonResponse({'success': False, 'error': 'No finish log ID provided'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

class SignupView(FormView):
    """View for user signup."""
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Handles form submission."""
        form.save()
        return super().form_valid(form)

class LoginView(FormView):
    """View for user login."""
    template_name = 'login2.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('container_list')

    def form_valid(self, form):
        """Handles form submission."""
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)

class LogoutView(TemplateView):
    """View for user logout."""
    def get(self, request, *args, **kwargs):
        """Handles GET request to logout."""
        logout(request)
        return redirect('login')


class SingleLogsView(View):
    """
    View for handling logs form submissions.
    """

    def get(self, request):
        """
        Renders the logs form page.
        """
        form = LogForm()
        return render(request, 'logs_form.html', {'form': form})

    def post(self, request):
        container_id = request.POST.get('container')

        logs_data = Log.objects.filter(container_id=container_id).order_by('-reference_id').values(
            'reference_id').first()

        next_reference_id = logs_data['reference_id'] + 1 if logs_data else 1

        post_data = request.POST.copy()
        post_data['reference_id'] = next_reference_id

        form = LogForm(post_data)

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Log added successfully'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})