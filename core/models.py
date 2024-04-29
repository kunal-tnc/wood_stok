from decimal import ROUND_HALF_UP, Decimal

from django.db import models


def calculate_net_avg(total_cbm, total_pieces):
    if total_pieces == 0:
        return Decimal("0.000")
    net_avg = (total_cbm * Decimal("35.315")) / Decimal(total_pieces)
    return net_avg.quantize(Decimal("0.000"), rounding=ROUND_HALF_UP)


def calculate_totals(logs):
    total_cbm = Decimal("0.000")
    total_pieces = 0
    for log in logs:
        try:
            cbm_value = Decimal(log.cbm)
            total_cbm += cbm_value
            total_pieces += 1
        except:

            pass
    return total_cbm, total_pieces


def calculate_all_totals_and_net_avg(logs):
    total_cbm, total_pieces = calculate_totals(logs)
    net_avg = calculate_net_avg(total_cbm, total_pieces)
    return total_cbm, total_pieces, net_avg


class Vendor(models.Model):
    """
    Model representing a vendor.

    Attributes:
    - name (CharField): The name of the vendor.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Container(models.Model):
    """
    Model representing a container.

    Attributes:
    - container_number (CharField): The unique identifier of the container.
    - pieces (IntegerField): The number of pieces in the container.
    - ncbm (DecimalField): The net cubic meters of the container.
    - navg (DecimalField): The net average of the container.
    - rate (IntegerField): The rate of the container.
    - amount (CharField): The amount of the container.
    - vendor (ForeignKey): The vendor associated with the container.
    - total_pieces (IntegerField): The total number of pieces in the container.
    - total_cbm (DecimalField): The total cubic meters of the container.
    - a_navg (DecimalField): The average net average of the container.
    - sort_axis_pieces (IntegerField): The sorting axis for pieces.
    - sort_axis_cbm (DecimalField): The sorting axis for cubic meters.
    - sort_axis_navg (DecimalField): The sorting axis for net average.
    - status (CharField): The status of the container (Locked or Draft).
    """
    STATUS_CHOICES = [
        ("lock", "Locked"),
        ("draft", "Draft"),
    ]
    container_number = models.CharField(max_length=50, unique=True)
    pieces = models.IntegerField(default=0)
    ncbm = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    navg = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    rate = models.IntegerField(default=0)
    amount = models.CharField(max_length=20, default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    total_pieces = models.IntegerField(default=0, null=True, blank=True)
    total_cbm = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True, blank=True
    )
    a_navg = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True, blank=True
    )

    sort_axis_pieces = models.IntegerField(default=0, null=True, blank=True)
    sort_axis_cbm = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True, blank=True
    )
    sort_axis_navg = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True, blank=True
    )
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="draft")

    def __str__(self):
        return self.container_number

    def calculate_sort_axis(self):
        self.sort_axis_pieces = self.total_pieces - self.pieces
        self.sort_axis_cbm = float(self.total_cbm) - float(self.ncbm)
        self.sort_axis_navg = float(self.a_navg) - float(self.navg)
        self.save()
        return True

    def recompute_totals(self):
        logs = self.logs.all()
        total_cbm, total_pieces, net_avg = calculate_all_totals_and_net_avg(logs)

        self.total_cbm = float(total_cbm)
        self.total_pieces = total_pieces
        self.a_navg = float(net_avg)

        self.save()

        return True


class Log(models.Model):
    """
    Model representing a log.

    Attributes:
    - container (ForeignKey): The container associated with the log.
    - length (CharField): The length of the log.
    - girth (CharField): The girth of the log.
    - cft (DecimalField): The cubic feet of the log.
    - cbm (DecimalField): The cubic meters of the log.
    - reference_id (IntegerField): The reference ID of the log.
    """
    container = models.ForeignKey(
        Container, on_delete=models.CASCADE, related_name="logs"
    )
    length = models.CharField(max_length=20, default=0, null=True, blank=True)
    girth = models.CharField(max_length=20, default=0, null=True, blank=True)
    cft = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True, blank=True
    )
    cbm = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True, blank=True
    )
    reference_id = models.IntegerField(default=0)

    def __str__(self):
        return f"Container: {self.container.container_number}, LogsInfo id: {self.id}, Cft: {self.cft}, Cbm:{self.cbm}"


class FinishedLog(models.Model):
    """
    Model representing a finished log.

    Attributes:
    - log (ForeignKey): The log associated with the finished log.
    - length (CharField): The length of the finished log.
    - width (CharField): The width of the finished log.
    - thickness (CharField): The thickness of the finished log.
    - cft (DecimalField): The cubic feet of the finished log.
    - reference_id (IntegerField): The reference ID of the finished log.
    """
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    length = models.CharField(max_length=20, default=0, null=True, blank=True)
    width = models.CharField(max_length=20, default=0, null=True, blank=True)
    thickness = models.CharField(max_length=20, default=0, null=True, blank=True)
    cft = models.DecimalField(
        max_digits=20, decimal_places=3, default=0, null=True, blank=True
    )
    reference_id = models.IntegerField(default=0)

    def __str__(self):
        return f"Log: {self.log.id}, FinishedLog id: {self.id}, length:{self.length}, width:{self.width}, thickness:{self.thickness}"


class SaleOrderline(models.Model):
    """
    Model representing a sale order line.

    Attributes:
    - width (CharField): The width of the sale order line.
    - thickness (CharField): The thickness of the sale order line.
    - length (CharField): The length of the sale order line.
    - quantity (IntegerField): The quantity of the sale order line.
    """
    width = models.CharField(max_length=20)
    thickness = models.CharField(max_length=20)
    length = models.CharField(max_length=20, default=0, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return f"width:{self.width}, thickness:{self.thickness}, length:{self.length}, quantity:{self.quantity}"


class SaleOrder(models.Model):
    """
    Model representing a sale order.

    Attributes:
    - orderline (ForeignKey): The sale order line associated with the sale order.
    - sale_date (DateField): The date of the sale order.
    """
    orderline = models.ForeignKey(SaleOrderline, on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Sale Order - {self.sale_date}"
