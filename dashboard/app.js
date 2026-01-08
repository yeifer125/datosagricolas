let chart;

const BASE =
  "https://raw.githubusercontent.com/yeifer125/datosagricolas/main/data";

async function cargarDatos() {
  const series = await fetch(`${BASE}/series_productos.json`).then(r => r.json());
  const tendencias = await fetch(`${BASE}/tendencias.json`).then(r => r.json());
  const predicciones = await fetch(`${BASE}/predicciones.json`).then(r => r.json());
  const alertas = await fetch(`${BASE}/alertas.json`).then(r => r.json());

  const select = document.getElementById("productoSelect");
  select.innerHTML = "";

  Object.keys(series).forEach(producto => {
    const option = document.createElement("option");
    option.value = producto;
    option.textContent = producto;
    select.appendChild(option);
  });

  if (select.options.length) {
    mostrarProducto(select.value, series, tendencias, predicciones, alertas);
  }

  select.onchange = () =>
    mostrarProducto(select.value, series, tendencias, predicciones, alertas);
}

function mostrarProducto(producto, series, tendencias, predicciones, alertas) {
  const datos = series[producto];

  document.getElementById("infoProducto").innerHTML = `
    <b>${producto}</b><br>
    📈 Tendencia: ${tendencias[producto]?.tendencia || "N/D"}<br>
    🔮 Predicción: ${predicciones[producto]?.prediccion_proxima || "N/D"}<br>
    🚨 Alerta: ${alertas[producto] || "Sin alertas"}
  `;

  if (chart) chart.destroy();

  chart = new Chart(document.getElementById("graficaPrecios"), {
    type: "line",
    data: {
      labels: datos.map(d => d.fecha),
      datasets: [{
        label: producto,
        data: datos.map(d => d.promedio),
        borderWidth: 2,
        tension: 0.3,
        pointRadius: 2,
        pointHoverRadius: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,

      /* 🔑 ESTO HACE QUE EL TOOLTIP FUNCIONE */
      interaction: {
        mode: "index",
        intersect: false
      },

      plugins: {
        tooltip: {
          enabled: true,
          callbacks: {
            title: (items) => {
              return "📅 Fecha: " + items[0].label;
            },
            label: (item) => {
              return "💰 Precio: ₡" + item.formattedValue;
            }
          }
        }
      },

      scales: {
        x: {
          ticks: {
            autoSkip: true,
            maxTicksLimit: 10
          }
        }
      }
    }
  });
}

cargarDatos();
