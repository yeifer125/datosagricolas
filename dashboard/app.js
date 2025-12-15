let chart;

async function cargarDatos() {
  const series = await fetch("../series_productos.json").then(r => r.json());
  const tendencias = await fetch("../tendencias.json").then(r => r.json());
  const predicciones = await fetch("../predicciones.json").then(r => r.json());
  const alertas = await fetch("../alertas.json").then(r => r.json());

  const select = document.getElementById("productoSelect");

  Object.keys(series).forEach(producto => {
    const option = document.createElement("option");
    option.value = producto;
    option.textContent = producto;
    select.appendChild(option);
  });

  select.onchange = () =>
    mostrarProducto(select.value, series, tendencias, predicciones, alertas);

  mostrarProducto(select.value, series, tendencias, predicciones, alertas);
}

function mostrarProducto(producto, series, tendencias, predicciones, alertas) {
  const datos = series[producto];

  const fechas = datos.map(d => d.fecha);
  const precios = datos.map(d => d.promedio);

  document.getElementById("precioActual").innerHTML =
    `💰 Precio actual<br><b>₡${precios[precios.length - 1]}</b>`;

  document.getElementById("tendencia").innerHTML =
    `📈 Tendencia<br><b>${tendencias[producto]?.tendencia || "N/A"}</b>`;

  document.getElementById("prediccion").innerHTML =
    `🔮 Predicción<br><b>₡${predicciones[producto]?.prediccion_proxima || "N/A"}</b>`;

  document.getElementById("alerta").innerHTML =
    `🚨 Alerta<br><b>${alertas[producto] || "Sin alertas"}</b>`;

  if (chart) chart.destroy();

  chart = new Chart(document.getElementById("grafico"), {
    type: "line",
    data: {
      labels: fechas,
      datasets: [{
        label: producto,
        data: precios,
        fill: false
      }]
    }
  });
}

cargarDatos();
