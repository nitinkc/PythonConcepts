const PYODIDE_INDEX = "https://cdn.jsdelivr.net/pyodide/v314.0.4/full/";
let pyodidePromise;

function getPyodide() {
    if (!pyodidePromise) {
        pyodidePromise = import(`${PYODIDE_INDEX}pyodide.mjs`).then(({loadPyodide}) =>
            loadPyodide({indexURL: PYODIDE_INDEX})
        );
    }
    return pyodidePromise;
}

async function runPython(container) {
    const button = container.querySelector("button");
    const editor = container.querySelector("textarea");
    const output = container.querySelector("pre");
    button.disabled = true;
    button.textContent = "Loading Python…";
    output.textContent = "";

    try {
        const pyodide = await getPyodide();
        let buffer = "";
        pyodide.setStdout({
            batched: (text) => {
                buffer += `${text}\n`;
            }
        });
        pyodide.setStderr({
            batched: (text) => {
                buffer += `${text}\n`;
            }
        });
        button.textContent = "Running…";
        const result = await pyodide.runPythonAsync(editor.value);
        if (result !== undefined && result !== null) {
            buffer += `${result}\n`;
        }
        output.textContent = buffer || "Code completed without output.";
    } catch (error) {
        output.textContent = `${error}`;
    } finally {
        button.disabled = false;
        button.textContent = "Run Python";
    }
}

function upgradePythonFence(container) {
    if (container.dataset.pythonRunner) {
        return;
    }

    const code = container.querySelector("code");
    const filename = container.querySelector(".filename");
    const title = filename?.textContent || "Python experiment";
    const editor = document.createElement("textarea");
    editor.value = code.textContent;
    editor.setAttribute("aria-label", title);
    editor.setAttribute("spellcheck", "false");

    const button = document.createElement("button");
    button.className = "md-button md-button--primary";
    button.type = "button";
    button.textContent = "Run Python";

    const hint = document.createElement("small");
    hint.textContent = "Runs locally in your browser";
    const actions = document.createElement("div");
    actions.className = "python-runner__actions";
    actions.append(button, hint);

    const outputCode = document.createElement("code");
    outputCode.textContent = "Output will appear here.";
    const output = document.createElement("pre");
    output.append(outputCode);

    container.replaceChildren(editor, actions, output);
    container.dataset.pythonRunner = "true";
}

function initializePythonRunners() {
    document.querySelectorAll(".python-runner.highlight").forEach(upgradePythonFence);
    document.querySelectorAll("[data-python-runner]").forEach((container) => {
        const button = container.querySelector("button");
        if (!button.dataset.ready) {
            button.dataset.ready = "true";
            button.addEventListener("click", () => runPython(container));
        }
    });
}

document.addEventListener("DOMContentLoaded", initializePythonRunners);
if (typeof document$ !== "undefined") {
    document$.subscribe(initializePythonRunners);
}
