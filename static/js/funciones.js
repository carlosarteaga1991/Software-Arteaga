

// INICIO MOSTRAR CONFIRMAR CONTRASEÑA 
function mostrarContrasenia(){ 
 
    var p=document.getElementById("pass2");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";

    var p=document.getElementById("pass");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";
}
// FIN MOSTRAR CONFIRMAR CONTRASEÑA

// INICIO MOSTRAR CONFIRMAR LOGIN 
function mostrarContrasenia(){ 
     var p=document.getElementById("id_password");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";
}
// FIN MOSTRAR CONFIRMAR LOGIN

// INICIO MOSTRAR CONFIRMAR DENTRO DE LOGGIN
function mostrarContrasenia_session(){ 
 
    var p=document.getElementById("id_new_password2");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";

    var p=document.getElementById("id_new_password1");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";

    var p=document.getElementById("id_old_password");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";
}
// FIN MOSTRAR CONFIRMAR LOGIN DENTRO DE LOGGIN


// INICIO DE CARACTERES DE CONTRASEÑA
function caracteresContrasenia(e)
{   
	var key=e.KeyCode || e.which;
	var teclado=String.fromCharCode(key).toLowerCase();
	var letras="abcdefghijklmnñopqrstuvwxyzABCDEFGHIJQLMNÑOPQRSTUVWXYZ_!·$%&ºª(¨+´{})=?¿ª@#~€¬^*1234567890¨_:;[]-.<@\\|/";
    var especiales="8-37-38-46-164";
	var teclado_especial=false;

	for(var i in especiales)
		{
            
		    if(key==especiales[i]){
                
		        teclado_especial=true;break;
		        }
		}
		if(letras.indexOf(teclado)==-1 && !teclado_especial){
		    return false;

		}      
}
// FIN DE CARACTERES DE CONTRASEÑA

// INICIO DE CONFIRMACIÓN DE CONTRASEÑA FUERA DE LOGGIN
function validarContrasenia(e){
    var pass = document.getElementById("pass").value;
    var pass2 = document.getElementById("pass2").value;
    
    if ( pass==pass2) {
        document.getElementById("error").innerHTML= "";
        document.getElementById("pass").style.borderColor = "green";
        document.getElementById("pass2").style.borderColor = "green";
        document.getElementById("verificar").style.borderColor = "green";
        document.getElementById("verificar2").style.borderColor = "green";
        document.getElementById("noerror").innerHTML = "¡Correcto!";
        //document.getElementById("mostrarBoton").style.backgroundColor = "green";
        //document.getElementById("mostrarBoton").type = "submit";
    } else {
        document.getElementById("noerror").innerHTML = "";
        document.getElementById("pass").style.borderColor = "red";
        document.getElementById("pass2").style.borderColor = "red";
        document.getElementById("verificar").style.borderColor = "red";
        document.getElementById("verificar2").style.borderColor = "red";
        document.getElementById("error").innerHTML= "¡No son iguales!";
        //document.getElementById("mostrarBoton").style.backgroundColor = "gray";
        //document.getElementById("mostrarBoton").type = "";
    }

}
// FIN VALIDAR CONFIRMACIÓN DE CONTRASEÑA FUERA DE LOGGIN

// INICIO DE CONFIRMACIÓN DE CONTRASEÑA DENTRO DE LOGGIN
function validarContrasenia_loggin(e){

    var pass = document.getElementById("id_new_password1").value;
    var pass2 = document.getElementById("id_new_password2").value;
    
    if ( pass==pass2) {
        document.getElementById("error").innerHTML= "";
        document.getElementById("id_new_password1").style.borderColor = "green";
        document.getElementById("id_new_password2").style.borderColor = "green";
        //document.getElementById("verificar").style.borderColor = "green";
        //document.getElementById("verificar2").style.borderColor = "green";
        document.getElementById("noerror").innerHTML = "¡Correcto!";
        //document.getElementById("mostrarBoton").style.backgroundColor = "green";
        //document.getElementById("mostrarBoton").type = "submit";
    } else {
        document.getElementById("noerror").innerHTML = "";
        document.getElementById("id_new_password1").style.borderColor = "red";
        document.getElementById("id_new_password2").style.borderColor = "red";
        //document.getElementById("verificar").style.borderColor = "red";
        //document.getElementById("verificar2").style.borderColor = "red";
        document.getElementById("error").innerHTML= "¡No son iguales!";
        //document.getElementById("mostrarBoton").style.backgroundColor = "gray";
        //document.getElementById("mostrarBoton").type = "";
    }

}
// FIN VALIDAR CONFIRMACIÓN DE CONTRASEÑA DENTRO DE LOGGIN

// INICIO VALIDAR USUARIO
var anterior = 0;
var contador = 0;
function usuario(e) {
    var key = e.keyCode || e.which,
    tecla = String.fromCharCode(key).toLowerCase(),
    letras = "abcdefghijklmnñopqrstuvwxyz",
    especiales = [],
    tecla_especial = false;
    anterior = key;
    //alert(contador);

    for (var i in especiales) {
    if (key == especiales[i]) {
        if (46 == anterior && contador==2) {
            tecla_especial = false;
            contador += 1;
        }else {
            tecla_especial = true;
        break;
        }
        
    }
    }

    if (letras.indexOf(tecla) == -1 && !tecla_especial) {
    return false;
    }
}
// FIN VALIDAR USUARIO

// INICIO VALIDAR nombre
function nombre(e) {
    var key = e.keyCode || e.which,
    tecla = String.fromCharCode(key).toLowerCase(),
    letras = " áéíóúabcdefghijklmnñopqrstuvwxyz",
    especiales = [],
    tecla_especial = false;

    for (var i in especiales) {
    if (key == especiales[i]) {
        tecla_especial = true;
        break;
    }
    }

    if ((letras.indexOf(tecla) == -1 && !tecla_especial) ) {
    return false;
    }
}
// FIN VALIDAR nombre




// VALIDAR CORREO
// no está funcionando aquí hay q colocarlo directo
document.getElementById('id_email').addEventListener('input', function() {
    campo = event.target;
    campo2 = event.target;
    valido = document.getElementById('emailOK');
    invalido = document.getElementById('emailnoOK');
        
    emailRegex = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
    //Se muestra un texto a modo de ejemplo, luego va a ser un icono
    if (emailRegex.test(campo.value)) {
    valido.innerText = "Válido";
    invalido.innerText = "";
    } 

    if (emailRegex.test(campo2.value)) {

    } else {
    invalido.innerText = "Incorrecto";
    valido.innerText = "";
    }
    
});
//FIN VALIDAR CORREO

// INICIO VALIDAR SIN ESPACIOS
/*var anterior = 0;
var contador = 0;
function sinEspacios(e) {
 //número en código es 32
}*/
// FIN VALIDAR SIN ESPACIOS

