import json
from collections import defaultdict

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, TemplateView

from .forms import *
from .models import *
from .utils import group_by_combination


class ContainerListView(View):
    """
    View for displaying a list of containers.
    """

    def get(self, request):
        """
        Renders the tables page with a list of containers.
        """
        containers = Container.objects.all()
        return render(request, "tables.html", {"containers": containers})


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
        return render(request, "containerform.html", {"form": form, "vendors": vendors})

    def post(self, request):
        """
        Handles POST request to create a new container.
        """
        mutable_post = request.POST.copy()

        if "status" not in mutable_post:
            mutable_post["status"] = "draft"
        form = ContainerForm(mutable_post)
        if form.is_valid():
            form.save()
            return redirect("container_list")
        else:
            vendors = Vendor.objects.all()
            return render(
                request, "containerform.html", {"form": form, "vendors": vendors}
            )


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
            log_exists = True

        return render(
            request,
            "containerform.html",
            {"form": form, "vendors": vendors, "log_exists": log_exists},
        )

    def post(self, request, pk):
        """
        Handles POST request to update an existing container.
        """
        container = get_object_or_404(Container, pk=pk)
        form = ContainerForm(request.POST, instance=container)
        form.fields.pop("status", None)
        if form.is_valid():
            container = form.save(commit=False)
            container.save()
            container.calculate_sort_axis()
            return redirect("update_container", pk=pk)
        else:
            vendors = Vendor.objects.all()
            return render(
                request, "containerform.html", {"form": form, "vendors": vendors}
            )


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
        return redirect("container_list")

    def delete(self, request, pk):
        """
        Handles DELETE request to delete a container.
        """
        container_obj = get_object_or_404(Container, pk=pk)
        container_obj.delete()
        return JsonResponse({"message": "container deleted successfully"})


class LockContainerView(View):
    """
    View for locking a container.

    This view locks a container identified by its ID.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to lock a container.
        """

        container_id = request.POST.get("container_id")
        try:
            container = Container.objects.get(pk=container_id)
            container.status = "lock"
            container.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Container locked successfully",
                    "reload": True,
                }
            )
        except Container.DoesNotExist:
            return JsonResponse({"success": False, "error": "Container not found"})


class LogsFormView(View):
    """
    View for handling logs form submissions.
    """

    def get(self, request):
        """
        Renders the logs form page.
        """
        form = LogForm()
        return render(request, "logsform.html", {"form": form})

    def post(self, request):
        """
        Handles POST request for logs form submission.
        """
        # Get container object based on the provided container id
        container_id = request.POST.get("container")
        container = Container.objects.get(id=container_id)

        if Log.objects.filter(container=container).exists():
            return redirect("update_container", container_id)

        errors = []

        reference_id = 1

        for _ in range(container.pieces):
            data = request.POST.copy()

            data["reference_id"] = reference_id

            form = LogForm(data)

            if form.is_valid():
                form.save()
            else:
                errors.append(form.errors)

            reference_id += 1

        return redirect("update_container", container_id)


class LogsListView(View):
    """
    View for displaying logs.

    This view retrieves logs from the database and groups them by container number for display.
    """

    def get(self, request):
        """Handles GET request to display log."""
        logs = Log.objects.all()

        grouped_logs = {}

        for log in logs:
            container_number = log.container.container_number

            if container_number not in grouped_logs:
                grouped_logs[container_number] = []

            grouped_logs[container_number].append(log)

        return render(request, "logstables.html", {"grouped_logs": grouped_logs})


class ContainerLogsView(View):
    """
    View for displaying logs of a specific container.

    This view retrieves logs associated with a specific container ID and renders them in a template.
    """

    def get(self, request, container_id):
        """
        Handle GET request to display logs of a specific container.
        """
        logs = Log.objects.filter(container_id=container_id)
        context = {
            "logs": logs,
        }
        return render(request, "container_logs.html", context)


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
        return render(request, "logsform.html", {"form": form, "log": log})

    def put(self, request):
        """
        Handles PUT request to update log entries.
        """
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
                    return JsonResponse(
                        {"error": f"Log with id {log_id} does not exist"}, status=404
                    )
            if "cont_id" in data:
                container_id = data["cont_id"]
                container = Container.objects.get(id=container_id)
                container.recompute_totals()
                container.calculate_sort_axis()
                return JsonResponse(
                    {
                        "message": "Logs updated successfully",
                        "total_cbm": container.total_cbm,
                        "total_pieces": container.total_pieces,
                        "net_avg": container.a_navg,
                    }
                )
            else:
                return JsonResponse(
                    {"error": "Container ID is missing from the request"}, status=400
                )

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class DeleteLogsView(View):
    """
    View for deleting a container logs.
    """

    def get(self, request, pk):
        """
        Renders the confirmation page for deleting a container.
        """
        log = get_object_or_404(Log, pk=pk)
        return render(request, "logdelete.html", {"log": log})

    def post(self, request, pk):
        """
        Handles POST request to delete a container log.
        """
        log = get_object_or_404(Log, pk=pk)
        log.delete()
        return redirect("container_list")


class SingleLogsView(View):
    """
    View for handling logs form submissions.
    """

    def get(self, request):
        """
        Renders the logs form page.
        """
        form = LogForm()
        return render(request, "logs_form.html", {"form": form})

    def post(self, request):
        """
        Handles POST request to create new log entries.
        """
        container_id = request.POST.get("container")

        logs_data = (
            Log.objects.filter(container_id=container_id)
            .order_by("-reference_id")
            .values("reference_id")
            .first()
        )

        next_reference_id = logs_data["reference_id"] + 1 if logs_data else 1

        post_data = request.POST.copy()
        post_data["reference_id"] = next_reference_id

        form = LogForm(post_data)

        if form.is_valid():
            form.save()
            container = Container.objects.get(id=container_id)
            container.recompute_totals()
            container.calculate_sort_axis()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Logs create successfully",
                    "total_cbm": container.total_cbm,
                    "total_pieces": container.total_pieces,
                    "net_avg": container.a_navg,
                }
            )
        else:
            errors = form.errors.as_json()
            return JsonResponse({"success": False, "errors": errors})


class FinishedLogsInfoView(View):
    """
    View for creating a new FinishedLogsInfo.
    """

    def get(self, request):
        """
        Renders the form to create a new FinishedLogsInfo.
        """

        finishedlogs = FinishedLogForm()

        return render(request, "containerform.html", {"finishedlogs": finishedlogs})

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
                if FinishedLog.objects.filter(
                    id=finished_log_id, log_id=log_ids
                ).exists():
                    finished_log_instance = FinishedLog.objects.get(
                        id=finished_log_id, log_id=log_ids
                    )
                    finished_log_instance.length = finished_log_data["length"]
                    finished_log_instance.width = finished_log_data["width"]
                    finished_log_instance.thickness = finished_log_data["thickness"]
                    finished_log_instance.cft = finished_log_data["cft"]
                    finished_log_instance.save()
            else:
                next_reference_id = 1
                if FinishedLog.objects.filter(log_id=log_ids).exists():
                    latest_finished_log = (
                        FinishedLog.objects.filter(log_id=log_ids)
                        .order_by("-reference_id")
                        .first()
                    )
                    next_reference_id = latest_finished_log.reference_id + 1
                FinishedLog.objects.create(
                    log_id=log_ids,
                    length=finished_log_data["length"],
                    width=finished_log_data["width"],
                    thickness=finished_log_data["thickness"],
                    cft=finished_log_data["cft"],
                    reference_id=next_reference_id,
                )

        return redirect("container_list")


class FinishedLogsView(View):
    """
    A view to retrieve finished logs associated with a specific log entry.
    """

    def get(self, request):
        """
        Handles GET request to retrieve finished logs associated with a specific log entry.
        """
        try:
            log_id = request.GET.get("log_id")
            if log_id:
                fin_logs = FinishedLog.objects.filter(log_id=log_id).values()
                logs_list = list(fin_logs)
                logs_list = sorted(logs_list, key=lambda x: x["reference_id"])
                return JsonResponse(logs_list, safe=False)
            else:
                return JsonResponse({"success": False, "error": "No log ID provided"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


class FinishedListView(View):
    def get(self, request):
        """Handles GET request to display finished log list."""

        finished_logs = FinishedLog.objects.all()

        seen_combinations = set((log.width, log.thickness) for log in finished_logs)
        products_by_combination = group_by_combination(finished_logs, seen_combinations)

        combination_logs = []
        for combination, logs in products_by_combination.items():
            length_counts = defaultdict(int)
            for log in logs:
                length_counts[log["length"]] += 1

            length_counts = dict(length_counts)
            combination_logs.append((combination, logs, len(logs), length_counts))

        return render(
            request, "finishedlogstable.html", {"combination_logs": combination_logs}
        )


class FinishedLogsList(View):
    def get(self, request):
        """
        A view to retrieve finished logs data for a given container ID.
        """
        fin_logs_grouped = defaultdict(list)
        con_id = request.GET.get("cont_id")

        logs_data = Log.objects.filter(container_id=con_id).prefetch_related(
            "finishedlog_set"
        )

        for log in logs_data:
            for f_log in log.finishedlog_set.all():
                key = (str(f_log.width), str(f_log.thickness))
                data = {
                    "log_no": log.reference_id,
                    "finished_log_no": f_log.reference_id,
                    "length": float(f_log.length),
                    "width": float(f_log.width),
                    "thickness": float(f_log.thickness),
                    "cft": float(f_log.cft),
                }
                fin_logs_grouped[key].append(data)

        fin_logs_grouped_str = {json.dumps(k): v for k, v in fin_logs_grouped.items()}

        # Preprocess the data to extract width and thickness
        processed_logs = [
            {"width": json.loads(key)[0], "thickness": json.loads(key)[1], "logs": logs}
            for key, logs in fin_logs_grouped_str.items()
        ]
        return JsonResponse(processed_logs, safe=False)


class DeleteFinishedlogs(View):
    """
    A view to delete a finished log entry.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to delete a finished log entry.
        """
        try:
            data = json.loads(request.body)
            finish_log_id = data.get("fin_log_id")
            if finish_log_id:
                finished_log = get_object_or_404(FinishedLog, id=finish_log_id)
                log_id = finished_log.log_id
                finished_log.delete()

                # Retrieve all finished logs for the same container ordered by reference_id
                logs = FinishedLog.objects.filter(log_id=log_id).order_by(
                    "reference_id"
                )

                # Reset the reference_id for each log starting from 1
                for index, log_entry in enumerate(logs, start=1):
                    log_entry.reference_id = index
                    log_entry.save()

                return redirect("container_list")
            else:
                return JsonResponse(
                    {"success": False, "error": "No finish log ID provided"}
                )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


class SaleOrderCreateView(View):
    """
    View for creating sale orders.

    This view handles the creation of sale orders based on the data received.
    """

    def get(self, request):
        """
        Handle GET request to render sale order form.
        """
        form = SaleOrderlineForm()
        return render(request, "saleorder.html", {"form": form})

    def post(self, request):
        """
        Handle POST request to create sale orders.
        """
        try:
            data = request.POST.get("sale_order")
            if not data:
                return JsonResponse(
                    {"success": False, "error": "No sale order data received"},
                    status=400,
                )

            sale_order_list = json.loads(data)

            for item in sale_order_list:
                width = item.get("width")
                thickness = item.get("thickness")
                length = item.get("length")
                quantity = int(item.get("quantity"))

                f_count = FinishedLog.objects.filter(
                    width=width, thickness=thickness, length=length
                ).count()

                if SaleOrderline.objects.filter(
                    width=width, thickness=thickness, length=length
                ).exists():
                    sale_orderlines = (
                        SaleOrderline.objects.filter(
                            width=width, thickness=thickness, length=length
                        ).aggregate(total_quantity=Sum("quantity"))["total_quantity"]
                        or 0
                    )

                    if sale_orderlines >= f_count:
                        return JsonResponse(
                            {
                                "success": False,
                                "message": f"Requested sale quantity {quantity} is not available",
                            },
                            status=400,
                        )

                    if sale_orderlines:
                        avlb = f_count - sale_orderlines
                        if quantity > avlb:
                            return JsonResponse(
                                {
                                    "success": False,
                                    "message": f"Requested sale quantity {quantity} is not available",
                                },
                                status=400,
                            )

                if quantity > f_count:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": f"Requested sale quantity {quantity} is not available",
                        },
                        status=400,
                    )

                sale_order_line = SaleOrderline.objects.create(
                    width=width,
                    thickness=thickness,
                    length=length,
                    quantity=quantity,
                )

                SaleOrder.objects.create(orderline=sale_order_line)

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "Invalid JSON format in sale order data"},
                status=400,
            )

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)


class SaleReportView(View):
    """
    View for generating and displaying sale reports.

    This view retrieves sale order data and renders a sale report template.
    """

    def get(self, request):
        """
        Handle GET request to generate and display sale report.
        """
        try:
            sale_orders = SaleOrder.objects.all().values(
                "sale_date",
                "orderline__width",
                "orderline__thickness",
                "orderline__length",
                "orderline__quantity",
            )

            sale_order_list = list(sale_orders)
            return render(request, "salereport.html", {"sale_order": sale_order_list})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


class StockListView(View):
    """
    View for displaying stock report.

    This view retrieves stock data and renders a stock report template.
    """

    def get(self, request):
        """
        Handle GET request to generate and display stock report.

        """
        stock_list = []

        finishedlog = FinishedLog.objects.values(
            "width", "thickness", "length"
        ).distinct()

        for f_log in finishedlog:
            width = f_log["width"]
            thickness = f_log["thickness"]
            length = f_log["length"]
            log_count = FinishedLog.objects.filter(
                width=width, thickness=thickness, length=length
            ).count()
            if SaleOrderline.objects.filter(
                width=width, thickness=thickness, length=length
            ).exists():
                sale_orderlines = SaleOrderline.objects.filter(
                    width=width, thickness=thickness, length=length
                ).aggregate(total_quantity=Sum("quantity"))

                available_log = log_count - sale_orderlines["total_quantity"]

            else:
                available_log = log_count

            data = {
                "width": width,
                "thickness": thickness,
                "length": length,
                "available_log": available_log,
            }
            stock_list.append(data)

        return render(request, "stockreport.html", {"stock_list": stock_list})


class SignupView(FormView):
    """View for user signup."""

    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        """Handles form submission."""
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    """View for user login."""

    template_name = "login2.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("container_list")

    def form_valid(self, form):
        """Handles form submission."""
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(TemplateView):
    """View for user logout."""

    def get(self, request, *args, **kwargs):
        """Handles GET request to logout."""
        logout(request)
        return redirect("login")
