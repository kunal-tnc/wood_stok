document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const containerId = button.dataset.containerId;
            const csrfToken = button.dataset.csrfToken;

            bootbox.confirm({
                message: "Are you sure you want to delete this record?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-danger'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-secondary'
                    }
                },
                callback: function(result) {
                    if (result) {
                        fetch('/container/' + containerId + '/delete/', {
                                method: 'DELETE', // Specify the method as DELETE
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': csrfToken
                                },
                                body: JSON.stringify({
                                    id: containerId
                                })
                            })
                            .then(response => {
                                if (response.ok) {
                                    location.reload();
                                } else {
                                    console.error('Error deleting record');
                                }
                            })
                            .catch(error => {
                                console.error('Error deleting record:', error);
                            });

                    }
                }
            });
        });
    });
});

//	2nd script started
var count = 0;
var f_logs = []
$(document).ready(function() {
    $('#myTable').DataTable();
});
$(document).on('click', '#add-more', function() {
    count += 1
    var dynamicRow = `
        <tr>
            <td>#</td>
            <td><input type="number" class="form-control td-length" name="length" id="#${count}length" step="0.25" min="0" required></td>
            <td><input type="number" class="form-control td-width" name="width" id="#${count}width" min="0" step=".01" required></td>
            <td><input type="number" class="form-control td-thickness" name="height" id="#${count}thickness" min="0" step=".01" required></td>
            <td><input type="number" class="form-control td-cft" name="cft" id="#${count}cft" min="0" readonly></td>
            <td><a href="#"><i class="fa fa-trash delete-row"/></a></td>
        </tr>
        `;
    $("#add-more-tr").before(dynamicRow);
});
$(document).on('click', '.delete-row', function() {
    let finishLogId = $(this).data('finish-log-id');

    for (let i = f_logs.length - 1; i >= 0; i--) {
        if (f_logs[i] === finishLogId) {
            f_logs.splice(i, 1);
        }
    }

    if (finishLogId !== undefined) {
        $.ajax({
            url: "/finishedlogs/delete/",
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            data: JSON.stringify({
                'fin_log_id': finishLogId
            }),
            success: function(response) {

            },
            error: function(xhr, status, error) {

            }
        });
    }
    count -= 1;
    $(this).closest('tr').remove();
});

//	3rd script started
document.addEventListener('DOMContentLoaded', () => {
    const saveBtn = document.getElementById('save-table-data');
    if (saveBtn) {
        saveBtn.addEventListener('click', async () => {
            try {
                const formData = new FormData(document.getElementById('table-data'));
                const jsonData = {};
                var cont_id = $('#cont_id').val();

                for (const [key, value] of formData.entries()) {
                    if (key.startsWith('log_')) {
                        const logKey = key.replace('log_', '');
                        if (jsonData[logKey]) {
                            if (!Array.isArray(jsonData[logKey])) {
                                jsonData[logKey] = [jsonData[logKey]];
                            }
                            jsonData[logKey].push(value);
                        } else {
                            jsonData[logKey] = value;
                        }
                    }
                }
                jsonData['cont_id'] = $('#cont_id').val();
                const response = await fetch('/logs/update/', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify(jsonData),
                    cont_id: cont_id
                });

                if (response.ok) {
                    bootbox.alert('Data Update Successfully');

                } else {
                    console.error('Failed to send data to log_update');
                }
            } catch (error) {
                console.error('Error sending data to log_update:', error);
            }
        });
    } else {
        console.error('Element with ID "save-table-data" not found');
    }
});

//  4th script started
var activate_log_id
$(document).on('click', '#f_log', function() {
    const log_id = $(this).val();
    activate_log_id = log_id
    $("#log").val(log_id);
    const table = document.getElementById('finished-row-table');
    $("#finished-row-table tr:not(:first-child):not(tfoot tr)").remove();

    $.ajax({
        data: {
            'log_id': log_id
        },
        url: "/finishedlog/",
        success: function(response) {
            f_logs = []
            for (var i = 0; i < response.length; i++) {

                var dynamicRow = `
                    <tr>
                        <td id="${response[i]['reference_id']}reference_id" value="${response[i]['reference_id']}">${response[i]['reference_id']}</td>
                        <td><input type="number" class="form-control td-length" id="${response[i]['id']}length" name="length" required value="${response[i]['length']}" step="0.25" min="0"></td>
                        <td><input type="number" class="form-control td-width" id="${response[i]['id']}width" name="width" required value="${response[i]['width']}" min="0" step=".01"></td>
                        <td><input type="number" class="form-control td-thickness" id="${response[i]['id']}thickness" name="thickness" required value="${response[i]['thickness']}" min="0" step=".01"></td>
                        <td><input type="number" class="form-control td-cft" id="${response[i]['id']}cft" name="cft" readonly value="${response[i]['cft']}" min="0" step=".001"></td>
                        <td><a href="#" class="delete-row" data-finish-log-id="${response[i]['id']}"><i class="fa fa-trash"></i></a></td>
                    </tr>
                `;
                f_logs.push(response[i]['id'])
                $("#finished-row-table").append(dynamicRow);
            }

        }
    });
});
// 5th script started
$(document).ready(function() {
    log_exixts = document.getElementById("log_exists").value

    if (log_exixts == 'True') {
        logsExistselement = document.getElementById("logsExists")
        logsExistselement.setAttribute("hidden", true);
    }
})
//    6th script started
document.getElementById("Fform").addEventListener("submit", function(event) {
    event.preventDefault();
    var finished_log = [];

    for (var i = 0; i < f_logs.length; i++) {
        var f_length = document.getElementById(`${f_logs[i]}length`).value;
        var f_width = document.getElementById(`${f_logs[i]}width`).value;
        var f_thickness = document.getElementById(`${f_logs[i]}thickness`).value;
        var f_cft = document.getElementById(`${f_logs[i]}cft`).value;
        var finished_log_dict = {
            'id': f_logs[i],
            'length': f_length,
            'width': f_width,
            'thickness': f_thickness,
            'cft': f_cft
        };
        finished_log.push(finished_log_dict);
    }

    for (var i = 1; i <= count; i++) {

        var f_length = document.getElementById(`#${i}length`).value;
        var f_width = document.getElementById(`#${i}width`).value;
        var f_thickness = document.getElementById(`#${i}thickness`).value;
        var f_cft = document.getElementById(`#${i}cft`).value;
        var finished_log_dict = {
            'id': "#",
            'length': f_length,
            'width': f_width,
            'thickness': f_thickness,
            'cft': f_cft
        };
        finished_log.push(finished_log_dict);
    }

    count = 0;
    $.ajax({
        url: "/finished_logs_info/create/",
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        data: JSON.stringify({
            'log_id': activate_log_id,
            'finished_log': finished_log
        }),
        success: function(response) {
            $("#LogModalclose").click();
        }
    });
});

$(document).on('change', '.td-length, .td-width, .td-thickness', function() {

    var $tr = $(this).closest('tr');
    var length = parseFloat($tr.find('.td-length').val());
    var width = parseFloat($tr.find('.td-width').val());
    var thickness = parseFloat($tr.find('.td-thickness').val());

    var cft = (length * width * thickness) / 144;

    $tr.find('.td-cft').val(cft.toFixed(2));
});
//    7th script started
$(document).ready(function() {
    // Function to calculate CFT and CBM
    function calculateVolume() {
        var conversionFactor = 35.3147;
        var length = parseFloat($('#lengthInput').val());
        var girth = parseFloat($('#girthInput').val());



        // Calculate CBM
        var cal = (girth * girth * length) / 16;
        var cbm = cal / 1000000;
        var cft = cbm * conversionFactor
        cbm = cbm.toFixed(3);
        $('#cftInput').val(cft.toFixed(3));
        $('#cbmInput').val(cbm);
    }

    $('#lengthInput, #girthInput').on('change', calculateVolume);

    // Event listener for form submission
    $('#logForm').submit(function(event) {
        event.preventDefault();
        calculateVolume();

        var formData = $(this).serialize();
        var cont_id = $('#cont_id').val();

        $.ajax({
            url: "/single_logs_form/",
            method: 'POST',
            data: formData,
            container: cont_id,
            success: function(response) {
                if (response.success) {
                    bootbox.alert({
                        message: response.message,
                        callback: function() {
                            $('#newLogModal').modal('hide');
                            location.reload();
                        }
                    });
                } else {
                    bootbox.alert('Error: ' + response.errors);
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                bootbox.alert('Error: ' + xhr.responseText);
            }
        });
    });

    // Reset form fields when modal is hidden
    $('#newLogModal').on('hidden.bs.modal', function() {
        $('#logForm')[0].reset();
    });
});
//  8th scripted started
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-log-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const logId = button.dataset.logId;
            const csrfToken = button.dataset.csrfToken;
            bootbox.confirm({
                message: "Are you sure you want to delete this log?",
                buttons: {
                    confirm: {
                        label: 'Yes',
                        className: 'btn-danger'
                    },
                    cancel: {
                        label: 'No',
                        className: 'btn-secondary'
                    }
                },
                callback: function(result) {
                    if (result) {

                        fetch('/container/log/' + logId + '/delete/', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                    'X-CSRFToken': csrfToken
                                },
                                body: JSON.stringify({
                                    id: logId
                                })
                            })
                            .then(response => {
                                if (response.ok) {

                                    location.reload();
                                } else {

                                    console.error('Error deleting log');
                                }
                            })
                            .catch(error => {
                                console.error('Error deleting log:', error);
                            });
                    }
                }
            });
        });
    });
});

//  10th scripted started

$(document).on('click', '#tab3-tab', function() {

    var cont_id = $('#cont_id').val();

    $("#finished_log_table tr:not(:first-child)").remove();
    $.ajax({
        url: "/finished-logs/",
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        data: {
            'cont_id': cont_id
        },
        success: function(response) {

            for (var i = 0; i < response.length; i++) {
                var dynamicRow = `
                    <tr>
                        <td>${response[i]['log_no']}</td>
                        <td>${response[i]['finished_log_no']}</td>
                        <td>${response[i]['length']}</td>
                        <td>${response[i]['width']}</td>
                        <td>${response[i]['thickness']}</td>
                        <td>${response[i]['cft']}</td>
                    </tr>
                `;
                $("#finished_log_table").append(dynamicRow);
            }
        }
    });
});

//  11th scripted started
// Calculate cft and cbm for data update case
$(document).on('change', '.length-input, .girth-input', function() {
    var $tr = $(this).closest('tr');
    var conversionFactor = 35.3147;
    var length = parseFloat($tr.find('.length-input').val());
    var girth = parseFloat($tr.find('.girth-input').val());


    var cal = (girth * girth * length) / 16;
    var cbm = cal / 1000000;
    var cft = cbm * conversionFactor
    $tr.find('.cft-input').val(cft.toFixed(3));
    $tr.find('.cbm-input').val(cbm.toFixed(3));
})

document.addEventListener('DOMContentLoaded', () => {
    const containerInfoLink = document.getElementById('tab1-tab');

    if (containerInfoLink) {
        containerInfoLink.addEventListener('click', () => {
            window.location.reload();
        });
    } else {
        console.error('Element with ID "tab1-tab" not found');
    }
});