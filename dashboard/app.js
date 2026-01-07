let SERIES = {};
let TENDENCIAS = {};
let PREDICCIONES = {};
let ALERTAS = {};
let chart = null;

// cache-busting para GitHub Pages
const nocache = `?v=${Date.now()}`;

async function cargarJSON(path) {
  const res = await fetch(path + nocache);
  if (!res.ok) throw new Error(`Error cargando ${path}`);
  return res.json();
}

async function cargarDatos() {
  try {
    SERIES = await cargarJSON("../data/series_productos.json");
    TENDENCIAS = await cargarJSON("../data/tendencias.json");
    PREDICCIONES = await cargarJSON("../data/predicciones.json");
    ALERTAS = await cargarJSON("../data/alertas.json");

    const select = document.getElementById("productoSelect");
    select.innerHTML = "";

    Object.keys(SERIES).forEach(producto => {
      const opt = document.createElement("option");
      opt.value = producto;
      opt.textContent = producto;
      select.appendChild(opt);
    });

    if (select.options.length > 0) {
      mostrarProducto(select.value);
    }

    select.onchange = () => mostrarProducto(select.value);

  } catch (err) {
    console.error(err);
    alert("Error cargando datos agrícolas");
  }
}

function mostrarProducto(producto) {
  const datos = SERIES[producto];
  if (!datos) return;

  const tendencia = TENDENCIAS[producto]?.tendencia ?? "N/D";
  const pred = PREDICCIONES[producto]?.prediccion_proxima ?? "N/D";
  const alerta = ALERTAS[producto] ?? "Sin alertas";

  document.getElementById("infoProducto").innerHTML = `
    <h3>${producto}</h3>
    <p>📈 Tendencia: <b>${tendencia}</b></p>
    <p>🔮 Predicción próxima: <b>${pred}</b></p>
    <p>🚨 Alerta: <b>${alerta}</b></p>
  `;

  actualizarGrafica(datos, producto);
}

function actualizarGrafica(datos, producto) {
  const ctx = document.getElementById("graficaPrecios");

  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: datos.map(d => d.fecha),
      datasets: [{
        label: producto,
        data: datos.map(d => d.promedio),
        borderWidth: 2,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: true }
      }
    }
  });
}

cargarDatos();
