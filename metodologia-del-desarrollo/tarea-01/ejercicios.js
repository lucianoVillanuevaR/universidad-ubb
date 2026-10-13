//1) Crea tres variables: una que almacene tu nombre (string), otra tu edad (number), y otra que indique si tienes mascotas (boolean). Luego imprímelas por consola.

let nombre = "luciano";
let edad = 20;
let TienesMascota = true;

console.log("Nombre:", nombre);
console.log("edad:", edad);
console.log("tienes mascota?:", TienesMascota);

//2) Crea dos variables numéricas y muestra en consola su suma, resta, multiplicación y división.

let num1 = 25;
let num2 = 5;

let suma = num1 + num2;
let resta = num1 - num2;
let multi = num1 * num2;
let div = num1 / num2;

console.log ("la suma es", suma)
console.log ("la resta es", resta)
console.log ("la multiplicacion es", multi)
console.log ("la division es:", div)

//3) Crea una función que reciba un nombre como parámetro y devuelva un saludo como string.

function nombreSaludo(nombre){
    return "hola " + nombre;
};

console.log(nombreSaludo("Luciano"));

// 4) Crea un array con 5 frutas y recórrelo con un bucle for, mostrando cada fruta en consola.
const frutas = ["Manzana", "Banana", "Naranja", "Manzana verde", "Uva"];

for (let i = 0; i < frutas.length; i++) {
  console.log(frutas[i]);
}


//5. Crea un array de 3 números, multiplícalos por 2 y guárdalos en un nuevo array usando `map`.
const numeroS = [5, 10, 15];
const numerosMultiplicados = numeroS.map(numero => numero * 2);
console.log(numerosMultiplicados);

//6) Crea un array de objetos donde cada objeto tenga un nombre y una edad. Luego, muestra en consola el nombre de cada persona usando forEach.
const personas = [
    { nombre: "Luciano", edad: 25 },
    { nombre: "camilo", edad: 30 },
    { nombre: "ela", edad: 22 }
  ];
  personas.forEach(persona => {
    console.log(persona.nombre);
  });
  

 // 7)Crea un array de números y utiliza `filter` para obtener los números mayores a 5.

const numeros = [3, 8, 1, 12, 5, 7];
const numerosMayoresA5 = numeros.filter(numero => numero > 5);
console.log(numerosMayoresA5);

//8) Crea un array de números y usa reduce para obtener la suma total.
const numeros3 = [3, 5, 2, 8, 10];

const sumaTotal = numeros3.reduce((acumulador, numero) => acumulador + numero, 0);

console.log(sumaTotal);



//9) Crea una función asincrónica que espere 2 segundos y luego devuelva un mensaje. Usa await para esperar su resultado e imprimirlo.
async function esperarMensaje() {
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return "¡Hola después de 2 segundos!";
  }
  
  async function main() {
    const mensaje = await esperarMensaje();
    console.log(mensaje); 
  }
 
  main();
  
