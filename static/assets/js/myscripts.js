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
            <td><input type="number" class="form-control td-cft" name="cft" id="#${count}cft" min="0" readonly style="font-weight: bold; color: #000;"></td>
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
                    Swal.fire({
                        title: 'Success',
                        text: 'Data Update Successfully',
                        icon: 'success',
                        confirmButtonText: 'OK'
                    });
                } else {
                    Swal.fire({
                        title: 'Error',
                        text: 'Failed to send data to log_update',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            } catch (error) {
                Swal.fire({
                    title: 'Error',
                    text: 'Error sending data to log_update: ' + error,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
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
                        <td><input type="number" class="form-control td-cft" id="${response[i]['id']}cft" name="cft" readonly value="${response[i]['cft']}" min="0" style="font-weight: bold; color: #000;"></td>
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
document.addEventListener('DOMContentLoaded', function() {
    const formElement = document.getElementById("Fform");
    if (formElement) {
        formElement.addEventListener("submit", function(event) {
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
    } else {
        console.error("Element with ID 'Fform' not found");
    }
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
        var conversionFactor = 35.315;
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
                Swal.fire({
                    title: 'Success',
                    text: response.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(function() {
                    $('#newLogModal').modal('hide');
                    location.reload();
                });
                } else {
                Swal.fire({
                    title: 'Error',
                    text: 'Error: ' + response.error,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        },
            error: function(xhr, status, error) {
            console.error(xhr.responseText);
            Swal.fire({
                title: 'Error',
                text: 'Error: ' + xhr.responseText,
                icon: 'error',
                confirmButtonText: 'OK'
            });
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
$(document).ready(function() {
            $('#tab3-tab').on('click', function() {
                var cont_id = $('#cont_id').val();

                $.ajax({
                    url: "/finished-logs/",
                    method: 'GET',
                    data: {
                        'cont_id': cont_id
                    },

                    success: function(response) {
                        // Clear existing accordion items
                        $('#accordion').empty();

                        // Iterate through the response data and create accordion items
                        response.forEach(function(item, index) {
                            var accordionItem = `
                                <div class="card-header" id="heading${index}" style="padding: 2px 5px;">
                                    <style>
                                        .chevron-down-arrow {
                                            float: right;
                                            right: 20px !important;
                                            position: absolute;
                                            cursor: pointer;
                                            transition: color 0.3s ease;
                                        }
                                        .chevron-down-arrow:hover {
                                                            color: blue;
                                                        }
                                        /* Adjust padding and font-size for smaller screens */
                                        @media (max-width: 768px) {
                                            .card-header {
                                                padding: 10px;
                                            }
                                            .btn {
                                                font-size: 14px;
                                            }
                                        }
                                    </style>
                                    <h5 class="mb-0">
                                        <button class="btn" data-toggle="collapse" data-target="#collapse${index}" aria-expanded="true" aria-controls="collapse${index}" style="background-color: white;">
                                            Width: ${item.width}, &nbsp;&nbsp;&nbsp; Thickness: ${item.thickness}
                                            <i class="fas fa-chevron-down chevron-down-arrow"></i>
                                        </button>
                                    </h5>
                                </div>

                                <div id="collapse${index}" class="collapse" aria-labelledby="heading${index}" data-parent="#accordion">
                                    <div class="card-body">

                                        <table class="table">
                                            <thead>
                                                <tr>
                                                    <th style="color: #000;">Log No</th>
                                                    <th style="color: #000;">Finished Log No</th>
                                                    <th style="color: #000;">Width</th>
                                                    <th style="color: #000;">Thickness</th>
                                                    <th style="color: #000;">Length</th>
                                                    <th style="color: #000;">CFT</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                ${item.logs.map(log => `
                                                    <tr>
                                                        <td style="color: #000;">${log.log_no}</td>
                                                        <td style="color: #000;">${log.finished_log_no}</td>
                                                        <td style="color: #000;">${log.width}</td>
                                                        <td style="color: #000;">${log.thickness}</td>
                                                        <td style="color: #000;">${log.length}</td>
                                                        <td style="color: #000;">${log.cft}</td>
                                                    </tr>
                                                `).join('')}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            `;
                            $('#accordion').append(accordionItem);
                        });
                    },
                    error: function(xhr, status, error) {
                        console.error(xhr.responseText);
                    }
                });
            });

            // Bind click event to toggle collapse when clicking the down arrow
            $(document).on('click', '.chevron-down-arrow', function() {
                var target = $(this).data('target');
                $(target).collapse('toggle');
            });
        });

//  11th scripted started
// Calculate cft and cbm for data update case
$(document).on('change', '.length-input, .girth-input', function() {
    var $tr = $(this).closest('tr');
    var conversionFactor = 35.315;
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
//  12th scripted started

$(document).on('click', '#lock-button', function(){

    console.log('Lock container function called');
    var containerId = $('#container_id').val();

    $.ajax({
        type: 'POST',
        url: '/lock-container/',
        data: {
            'container_id': containerId,
            'csrfmiddlewaretoken': csrfToken,
        },

        success: function(response) {
            if (response.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Container locked successfully',
                    showConfirmButton: false,
                    timer: 1500
                }).then(function() {
                    window.location.reload();
                });
            } else {
                Swal.fire({
                    title: 'Error',
                    text: 'Error: ' + response.error,
                    icon: 'error'
                });
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            console.error('Failed to lock container:', errorThrown);
            Swal.fire({
                title: 'Error',
                text: 'Error: ' + xhr.responseText,
                icon: 'error'
            });
        }
    });
});

$('#submit-button').click(function(event) {

    Swal.fire({
        icon: 'success',
        title: 'Container Successfully',
        showConfirmButton: false,
        timer: 8000
    });
});

//  13th scripted started
document.addEventListener("DOMContentLoaded", function() {
    var printButton = document.getElementById("printButton");
    var contentToPrint = document.getElementById("contentToPrint");

    if (printButton) {
        printButton.addEventListener("click", function() {
            printDiv(contentToPrint);
        });
    }
});

function printDiv(divId) {
    var printContents = divId.innerHTML;
    var originalContents = document.body.innerHTML;

    document.body.innerHTML = printContents;

    window.print();

    document.body.innerHTML = originalContents;
}


//  14th scripted started
var Sale_count = 0;

    $(document).on('click', '#add-more-order', function() {
        Sale_count += 1;
        var newRow = `
            <tr>
                <td><input type="number" class="form-control sale-width" name="width" id="${Sale_count}_width" min="0" step=".01" required></td>
                <td><input type="number" class="form-control sale-thickness" name="thickness" id="${Sale_count}_thickness" min="0" step=".01" required></td>
                <td><input type="number" class="form-control sale-length" name="length" id="${Sale_count}_length" min="0" step=".01" required></td>
                <td><input type="number" class="form-control sale-quantity" name="quantity" id="${Sale_count}_quantity" min="0" required></td>
                <td><a href="#" class="remove-row">Remove</a></td>
            </tr>
        `;
        $("#add-more-order-tr").before(newRow);
    });

    $(document).on('click', '.remove-row', function(e) {
        e.preventDefault();
        Sale_count -= 1;
        $(this).closest('tr').remove();
    });


$(document).on('click', '#submit_sale', function(e) {
    e.preventDefault();

    var sale_order = [];

    // Flag to track if any value is less than zero
    var isValid = true;

    for (var i = 0; i <= Sale_count; i++) {
        var s_width = document.getElementById(`${i}_width`);
        var s_thickness = document.getElementById(`${i}_thickness`);
        var s_length = document.getElementById(`${i}_length`);
        var s_quantity = document.getElementById(`${i}_quantity`);

        // Check if all elements exist
        if (s_width && s_thickness && s_length && s_quantity) {
            // Check if values are positive
            if (s_width.value >= 0 && s_thickness.value >= 0 && s_length.value >= 0 && s_quantity.value >= 0) {
                var saleorder_dict = {
                    'width': s_width.value,
                    'thickness': s_thickness.value,
                    'length': s_length.value,
                    'quantity': s_quantity.value
                };
                sale_order.push(saleorder_dict);
            } else {
                isValid = false;
                console.error(`One or more input values are negative for Sale ${i}`);
            }
        } else {
            isValid = false;
            console.error(`One or more elements with ID ${i}_width, ${i}_thickness, ${i}_length, or ${i}_quantity not found.`);
        }
    }

    // Check if any value is less than zero
    if (!isValid) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'One or more input values are negative. Please enter valid positive values.'
        });
        return; // Stop further processing
    }

    console.log("Sale order:", sale_order);

    // Proceed with AJAX request
    $.ajax({
        url: '/api/saleorder/',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        data: { sale_order: JSON.stringify(sale_order) },
        success: function(response) {
            if (response.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Success',
                    text: 'Sale order submitted successfully!'
                }).then(function() {
                    location.reload();
                });
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: response.message
                }).then(function() {
                    window.location.reload();
                });
            }
        },
        error: function(xhr, status, error) {
            Swal.fire({
                title: 'Error',
                text: 'Error: ' + xhr.responseText,
                icon: 'error',
            });
        }
    });
});