from django.db import models
from decimal import Decimal, ROUND_HALF_UP
def calculate_net_avg(total_cbm, total_pieces):
    if total_pieces == 0:
        return Decimal('0.00')  # Return 0 if total_pieces is 0 to avoid division by zero
    net_avg = (total_cbm * Decimal('35.315')) / Decimal(total_pieces)
    return net_avg.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calculate_totals(logs):
    total_cbm = Decimal('0.00')
    total_pieces = 0
    for log in logs:
        try:
            cbm_value = Decimal(log.cbm)
            total_cbm += cbm_value
            total_pieces += 1
        except:
            # Handle invalid CBM values gracefully
            pass
    return total_cbm, total_pieces

def calculate_all_totals_and_net_avg(logs):
    total_cbm, total_pieces = calculate_totals(logs)
    net_avg = calculate_net_avg(total_cbm, total_pieces)
    return total_cbm, total_pieces, net_avg

class Vendor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Container(models.Model):
    container_number = models.CharField(max_length=50,unique=True)
    pieces = models.IntegerField(default=0)
    ncbm = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    navg = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    rate = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    total_pieces = models.IntegerField(default=0, null=True, blank=True)
    total_cbm = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    a_navg = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)

    def __str__(self):
        return self.container_number

    def recompute_totals(self):
        logs = self.logs.all()
        total_cbm, total_pieces, net_avg = calculate_all_totals_and_net_avg(logs)

        # Update the model fields
        self.total_cbm = float(total_cbm)
        self.total_pieces = total_pieces
        self.a_navg = float(net_avg)

        # Save the updated values
        self.save()

        # Return the calculated values
        return total_cbm, total_pieces, net_avg


class Log(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name="logs")
    length = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    girth = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    cft = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    cbm = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    reference_id = models.IntegerField(default=0)

    def __str__(self):
        return f"Container: {self.container.container_number}, LogsInfo id: {self.id}, Cft: {self.cft}, Cbm:{self.cbm}"


class FinishedLog(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE)
    length = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    width = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    thickness = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    cft = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    reference_id = models.IntegerField(default=0)

    def __str__(self):
        return f"Log: {self.log.id}, FinishedLog id: {self.id}"

