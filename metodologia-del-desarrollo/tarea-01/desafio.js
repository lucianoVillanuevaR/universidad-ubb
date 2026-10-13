//Tienes una lista de pedidos. Cada pedido es un objeto con un `id`, un `producto`, y una propiedad `entregado` que puede ser `true` o `false`.
// Crea una función asincrónica que:
//Espere 1 segundo por cada pedido usando `setTimeout` dentro de una promesa.
//Si el pedido está entregado, resuelva la promesa con un mensaje indicando que ya se entregó.
//- Si no, la rechace con un mensaje indicando que el pedido está pendiente.
//1. Usa `async/await` y `try/catch` para recorrer todos los pedidos y mostrar el resultado de cada uno.
const pedidos = [
    { id: 1, producto: "Laptop", entregado: true },
    { id: 2, producto: "Smartphone", entregado: false },
    { id: 3, producto: "Tablet", entregado: true }
  ];
  
  async function procesarPedido(pedido) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (pedido.entregado) {
          resolve(`El pedido con ID ${pedido.id} (${pedido.producto}) ya fue entregado.`);
        } else {
          reject(`El pedido con ID ${pedido.id} (${pedido.producto}) aún está pendiente.`);
        }
      }, 1000)
    });
  }
  
  async function procesarPedidos() {
    for (const pedido of pedidos) {
      try {
        const resultado = await procesarPedido(pedido);
        console.log(resultado);
      } catch (error) {
        console.error(error);
      }
    }
  }
  
  procesarPedidos();
  