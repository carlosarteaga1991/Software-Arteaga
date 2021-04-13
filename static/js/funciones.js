
function mostrarContrasenia(){ 
 
    var p=document.getElementById("pass2");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";

    var p=document.getElementById("pass");
    var c=document.getElementById("chec");
    p.type=(c.checked) ? "text" : "password";
}

function validarContrasenias(){
    var pass = document.getElementById("pass").value;
    var pass2 = document.getElementById("pass2").value;

    if (pass==pass2){
             if (document.getElementById("resultado").innerHTML!="Correo invalido"){
            return true;
            }else{
            alert("El correo es inválido, por favor colocar uno válido");
            return false;
               }
    }else{
    alert("Contraseña y Confirmar Contraseña deben de ser iguales");
    return false;
       }
}


function caracteresContrasenia(e)
{   
	var key=e.KeyCode || e.which;
	var teclado=String.fromCharCode(key).toLowerCase();
	var letras="abcdefghijklmnñopqrstuvwxyzABCDEFGHIJQLMNÑOPQRSTUVWXYZ_!·$%&ºª(¨+´{})=?¿ª@#~€¬^*123456789¨_:;[]-.<@\\|/";
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