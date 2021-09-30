import { asyncRun } from "./py-worker.js";



      async function main(){
        const inputElement = document.getElementById("upload");
        inputElement.addEventListener("change", handleFiles, false);
        async function handleFiles() {
          const fileList = this.files; /* now you can work with the file list */
          const uploadName = fileList[0].name
          console.log(uploadName);
          const upload = await fileList[0].text();
          console.log(upload);
          console.log("uploaded inside script", inputElement.value)
          const context = {
            fileName: uploadName,
            fileText: upload 
          };
          console.log(context)
          try {
            const { results, error } = await asyncRun(pyScript, context);
            if (results) {
              console.log("pyodideWorker return results: ", results);

              // Automatic Download
              var hiddenElement = document.createElement('a');
              hiddenElement.href = 'data:attachment/text,' + encodeURI(results);
              hiddenElement.target = '_blank';
              hiddenElement.download = 'myFile.csv';
              hiddenElement.click();

            } else if (error) {
              console.log("pyodideWorker error: ", error);
            }
          } catch (e) {
            console.log(
              `Error in pyodideWorker at ${e.filename}, Line: ${e.lineno}, ${e.message}`
            );
          }        // pyFuncs = await pyodide.runPython(pyScript);

        }
        // let pyodide = await loadPyodide({
        //   indexURL : "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/"
        // });
        // console.log(pyodide.runPython("1 + 2"));
        // await pyodide.loadPackage("pandas");
        // await pyodide.loadPackage("micropip");

        // pyodide.runPythonAsync(`
        // import micropip
        // micropip.install('https://files.pythonhosted.org/packages/69/bf/f0f194d3379d3f3347478bd267f754fc68c11cbf2fe302a6ab69447b1417/beautifulsoup4-4.10.0-py3-none-any.whl')
// `);
        const response = await fetch("notebook.py");
        const pyScript = await response.text();
    try {
      const { results, error } = await asyncRun(pyScript, context);
      if (results) {
        console.log("pyodideWorker return results: ", results);
      } else if (error) {
        console.log("pyodideWorker error: ", error);
      }
    } catch (e) {
      console.log(
        `Error in pyodideWorker at ${e.filename}, Line: ${e.lineno}, ${e.message}`
      );
    }        // pyFuncs = await pyodide.runPython(pyScript);


      }
      main();

