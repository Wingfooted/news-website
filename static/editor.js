let inputIdCounter = 1; 
let idList = [];

function updateForm () {
    var form = document.getElementById("form-data");
    form.value = JSON.stringify(idList);
    console.log(idList)
};

function addText() {
    const textWrapper = document.createElement("div");
    textWrapper.className = "content-wrapper";

    const contentDiv = document.createElement("div");
    contentDiv.className = "content-text"
    contentDiv.textContent = "enter text"; 
    contentDiv.id = `div-${inputIdCounter}`; 
    contentDiv.contentEditable = true;

    const hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.id = `text-${inputIdCounter}`;
    hidden.name = hidden.id;
    idList.push(`text-${inputIdCounter}`);

    contentDiv.addEventListener("input", function () {
        hidden.value = contentDiv.textContent;
    });

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function() {
        textWrapper.remove();
    };

    const editorContents = document.getElementById("editor-contents");
    textWrapper.appendChild(contentDiv);
    textWrapper.appendChild(hidden);
    textWrapper.appendChild(deleteButton);
    editorContents.appendChild(textWrapper); 

    inputIdCounter++;
    updateForm();
}

function addSub() {
    const subWrapper = document.createElement("div");
    subWrapper.className = "content-wrapper";

    const subDiv = document.createElement("div");
    subDiv.className = "subheading-text";
    subDiv.id = `div-${inputIdCounter}`;
    subDiv.textContent = "Subheading Text"
    subDiv.contentEditable = true;

    const hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.id = `sub-${inputIdCounter}`;
    hidden.name = hidden.id;
    idList.push(`sub-${inputIdCounter}`);

    subDiv.addEventListener("input", function () {
        hidden.value = subDiv.textContent;
    });

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function() {
        subWrapper.remove();
    };

    const editorContents = document.getElementById("editor-contents");
    subWrapper.appendChild(subDiv);
    subWrapper.appendChild(hidden);
    subWrapper.appendChild(deleteButton);
    editorContents.appendChild(subWrapper); 

    inputIdCounter++;
    updateForm();

}

function addQuote() {
    const quoteWrapper = document.createElement("div");
    quoteWrapper.className = "content-wrapper";

    const quoteDiv = document.createElement("div");
    quoteDiv.className = "quote-text";
    quoteDiv.id = `div-${inputIdCounter}`;
    quoteDiv.textContent = "Quote Text"
    quoteDiv.contentEditable = true;

    const hidden = document.createElement("input");
    hidden.type = "hidden";
    hidden.id = `quote-${inputIdCounter}`;
    hidden.name = hidden.id;
    idList.push(`quote-${inputIdCounter}`);

    quoteDiv.addEventListener("input", function () {
        hidden.value = quoteDiv.textContent;
    });

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function() {
        quoteWrapper.remove();
    };

    const editorContents = document.getElementById("editor-contents");
    quoteWrapper.appendChild(quoteDiv);
    quoteWrapper.appendChild(hidden);
    quoteWrapper.appendChild(deleteButton);
    editorContents.appendChild(quoteWrapper); 

    inputIdCounter++;
    updateForm();
}

function addTable() {
    const tableWrapper = document.createElement('div');
    tableWrapper.className = 'content-wrapper';

    const rowHTML = `
    <select id="rowSize">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
    </select>
    `;

    const colHTML = `
    <select id="colSize">
      <option value="1">1</option>
      <option value="2">2</option>
      <option value="3">3</option>
      <option value="4">4</option>
    </select>
    `;

    // Parse HTML strings to DOM elements
    const parser = new DOMParser();

    const rowSelect = parser.parseFromString(rowHTML, 'text/html').body.firstChild;
    const colSelect = parser.parseFromString(colHTML, 'text/html').body.firstChild;

    // Append the select elements to the tableWrapper
    tableWrapper.appendChild(rowSelect);
    tableWrapper.appendChild(colSelect);

    rowSelect.addEventListener('change', function() {
        console.log('Row Size:', rowSelect.value);
    });

    // Event listener for colSize change
    colSelect.addEventListener('change', function() {
        console.log('Column Size:', colSelect.value);
    });

    const table = `
    <table border="1">
        <tr>
            <td>Row 1, Col 1</td>
            <td>Row 1, Col 2</td>
        </tr>
        <tr>
            <td>Row 2, Col 1</td>
            <td>Row 2, Col 2</td>
        </tr>
    </table>
    `;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function() {
        tableWrapper.remove();
    };

    const editorContents = document.getElementById("editor-contents");
    tableWrapper.appendChild(deleteButton);
    editorContents.appendChild(tableWrapper);
}

function addImg() {
    const imageWrapper = document.createElement("div");
    imageWrapper.className = "content-wrapper";

    const imageForm = document.createElement("input");
    imageForm.type = "file"
    imageForm.id = `img-${inputIdCounter}`;
    imageForm.name = `img-${inputIdCounter}`;
    imageForm.required = true;
    idList.push(`img-${inputIdCounter}`);

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.onclick = function() {
        imageWrapper.remove();
    };

    const editorContents = document.getElementById("editor-contents");
    imageWrapper.appendChild(imageForm);
    imageWrapper.appendChild(deleteButton);
    editorContents.appendChild(imageWrapper);

    inputIdCounter++;
    updateForm();
}

function save() {
    console.log("Saving content");
}