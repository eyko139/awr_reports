importScripts("https://cdn.jsdelivr.net/pyodide/v0.18.1/full/pyodide.js");

onmessage = async function (e) {
  try {
    const data = e.data;
    for (let key of Object.keys(data)) {
      if (key !== "python") {
        // Keys other than python must be arguments for the python script.
        // Set them on self, so that `from js import key` works.
        self[key] = data[key];
      }
    }

    if (!loadPyodide.inProgress) {
      self.pyodide = await loadPyodide({ indexURL: "./" });
    }
    await self.pyodide.loadPackagesFromImports(data.python);
    let results = await self.pyodide.runPythonAsync(data.python);
    self.postMessage({ results });
  } catch (e) {
    // if you prefer messages with the error
    self.postMessage({ error: e.message + "\n" + e.stack });
    // if you prefer onerror events
    // setTimeout(() => { throw err; });
  }
};

async function loadPyodideAndPackages() {
  self.pyodide = await loadPyodide({
    indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/",
  });


  // Double imports here are unnecessary, maybe needed later...
  //
  // await self.pyodide.loadPackage(["numpy", "pandas", "micropip"])
    // pyodide.runPythonAsync(`
    // import micropip
    // micropip.install('https://files.pythonhosted.org/packages/69/bf/f0f194d3379d3f3347478bd267f754fc68c11cbf2fe302a6ab69447b1417/beautifulsoup4-4.10.0-py3-none-any.whl')
// `);

}

let pryodideReadyPromise = loadPyodideAndPackages();

self.onmessage = async (event) => {
  //
  //Ensure loading is Done
  await pryodideReadyPromise;

  const { python, ...context} = event.data;

  for (const key of Object.keys(context)) {
    self[key] = context[key];
  }

  try {
    await self.pyodide.loadPackagesFromImports(python);
    let results = await self.pyodide.runPythonAsync(python);
    self.postMessage({ results });
  } catch (error) {
    self.postMessage({ error: error.message })
  }
}
