# from .models import *
# def cal_total_cbm(logs):
#     total_cbm = 0
#     total_pices = 0
#     for log in logs:
#             cbm_value = float(log.get('cbm', 0))
#             total_cbm += cbm_value
#             total_pices = total_pices+1
#     return total_cbm,total_pices
#
# def cal_total_navg():
#
# def cont_update(container):
#     breakpoint()
#     logs = Log.objects.filter(container_id=container.id).values('cbm')
#     tot_cbm = cal_total_cbm(logs)
