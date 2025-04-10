from django.contrib.admin.views.decorators import staff_member_required as login_required
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch
from graphs.models import *
from monitor.settings import FALLBACK_API_KEY


@require_http_methods(["GET"])
def temperature_measurement_add(request):
    data = {"status": 0}
    errors = []

    try:
        serial = request.GET["serial"]
        value = request.GET["temperature"]
        key = request.GET["key"]
        if key == FALLBACK_API_KEY:
            sensor = Sensor.objects.filter(serial=serial).first()
            if not sensor:
                sensorType = SensorType.objects.filter(raw_name="temperature").first()
                if not sensorType:
                    sensorType = SensorType.objects.create(raw_name="temperature")
                sensor = Sensor.objects.create(serial=serial, sensor_type=sensorType)
            else:
                sensor.update_last_measurement_date()
            Measurement.objects.create(sensor=sensor, value=value)
            data["status"] = 100
        else:
            data["status"] = 101
            errors.append("Wrong key!")
    except:
        data["status"] = 102
        errors.append("Wrong parameters!")

    data["errors"] = errors
    return JsonResponse(data)


@login_required()
@permission_required("graphs.view_sensor", raise_exception=True)
def prefetch_sensors_measurement(request, sensors):
    now = timezone.now()
    last_hours = request.GET.get("last_hours", "")
    datetime_begin = request.GET.get("datetime_begin", "")
    datetime_end = request.GET.get("datetime_end", "")

    if not last_hours and not datetime_begin:
        last_hours = 24
    if last_hours:
        datetime_begin = now - timedelta(hours=int(last_hours))
        datetime_end = now
    if not datetime_end:
        datetime_end = now

    measurements = Measurement.objects.filter(posted_date__range=(datetime_begin, datetime_end)).order_by("posted_date")
    return sensors.prefetch_related(Prefetch("measurement_set", queryset=measurements))


@login_required()
@permission_required("graphs.view_sensor", raise_exception=True)
def get_sensors(request):
    try:
        group = SensorsGroup.objects.filter(id=request.GET["group_id"], visible=True).first()
        sensors = group.sensors.filter_latest().order_by("name").all()
        name = group.name
    except:
        try:
            sensorType = SensorType.objects.filter(id=request.GET["sensor_type_id"], visible=True).first()
            sensors = Sensor.objects.filter_latest().filter(visible=True, sensor_type=sensorType).order_by("name")
            name = sensorType.name
        except:
            try:
                sensors = Sensor.objects.filter_latest().filter(id=request.GET["sensor_id"], visible=True)
                name = sensors.first().name
            except:
                sensors = Sensor.objects.none()
                name = ""
    return (prefetch_sensors_measurement(request, sensors), name)


@require_http_methods(["GET"])
@login_required()
@permission_required("graphs.view_sensor", raise_exception=True)
def graphs(request):
    if request.GET.get("format", None) == "json":
        data = {"status": 0}
        aggregation_time = request.GET.get("aggregation_time", "minute")
        min_max_enabled = "min_max" in request.GET
        (sensors, data["name"]) = get_sensors(request)
        data["sensors"] = [s.get_data(aggregation_time, min_max_enabled) for s in sensors]
        return JsonResponse(data, safe=False)
    else:
        (_, name) = get_sensors(request)
        return render(request, "graphs.html", {"name": name})
