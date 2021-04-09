$(function() {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {}, 
            dataSrc: ""
        },
        columns: [
            { "data": "Id"},
            { "data": "Nombre"},
            { "data": "naUsuariome"},
            { "data": "Departamento"},
            { "data": "Puesto"},
            { "data": "Estado"},
            { "data": "boton"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) { //para acceder a cada dato d ela fila colocamos row.nombre o row.puesto
                    return data;
                }
            },
        ],
        initComplete: function(settings, json) {
                alert('ingresó');//aquí algún mensaje si deseo
          }
        });
});