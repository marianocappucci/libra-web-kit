// Resume el reporte JSON de Playwright (`test-results/resultado.json`, lo escribe `libra-ui/e2e`): al resumen del job, un warning por
// cada flake (pasó recién al reintento) y los totales como outputs (`flaky`, `fallos`). No falla nunca: el que pone rojo el job es
// `playwright test`; esto sólo cuenta.
import fs from 'node:fs'

const [, , archivo] = process.argv
const salida = process.env.GITHUB_OUTPUT
const resumen = process.env.GITHUB_STEP_SUMMARY

const escribir = (ruta, texto) => { if (ruta) fs.appendFileSync(ruta, texto) }

if (!archivo || !fs.existsSync(archivo)) {
  console.log(`Sin reporte (${archivo}): no se llegó a correr Playwright.`)
  escribir(salida, 'flaky=0\nfallos=0\n')
  process.exit(0)
}

const reporte = JSON.parse(fs.readFileSync(archivo, 'utf8'))
const filas = []
const recorrer = (suite, titulos) => {
  const camino = suite.title && !/\.(ts|js)$/.test(suite.title) ? [...titulos, suite.title] : titulos
  for (const hijo of suite.suites ?? []) recorrer(hijo, camino)
  for (const spec of suite.specs ?? []) {
    for (const prueba of spec.tests ?? []) {
      filas.push({
        archivo: spec.file, titulo: [...camino, spec.title].join(' › '), proyecto: prueba.projectName,
        estado: prueba.status, intentos: (prueba.results ?? []).length,
      })
    }
  }
}
for (const suite of reporte.suites ?? []) recorrer(suite, [])

const cuenta = (estado) => filas.filter((f) => f.estado === estado).length
const flaky = filas.filter((f) => f.estado === 'flaky')
const fallos = filas.filter((f) => f.estado === 'unexpected')
const segundos = ((reporte.stats?.duration ?? 0) / 1000).toFixed(1)

for (const f of flaky) console.log(`::warning title=Flake en ${f.proyecto}::${f.archivo} › ${f.titulo} pasó recién al reintento (${f.intentos} intentos)`)
for (const f of fallos) console.log(`::error title=Falló ${f.proyecto}::${f.archivo} › ${f.titulo}`)

let texto = `### Tests de navegador\n\n| Pasaron | Fallaron | Flakes | Salteados | Tiempo |\n|---|---|---|---|---|\n`
texto += `| ${cuenta('expected')} | ${fallos.length} | ${flaky.length} | ${cuenta('skipped')} | ${segundos} s |\n`
if (flaky.length) texto += `\n**Flakes** (pasaron al reintento; cuentan contra las dos semanas sin flakes):\n\n${flaky.map((f) => `- \`${f.archivo}\` › ${f.titulo}`).join('\n')}\n`
if (fallos.length) texto += `\n**Fallaron:**\n\n${fallos.map((f) => `- \`${f.archivo}\` › ${f.titulo}`).join('\n')}\n`
escribir(resumen, texto)
console.log(texto)
escribir(salida, `flaky=${flaky.length}\nfallos=${fallos.length}\n`)
