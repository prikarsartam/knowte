const notesList = document.getElementById('notes-list');
let currentGraph = null;

document.addEventListener('DOMContentLoaded', () => {
  fetchNotes();
});

function fetchNotes() {
  fetch('http://localhost:8000/notes')
    .then(response => response.json())
    .then(data => {
      notesList.innerHTML = '';
      data.forEach(note => {
        const li = document.createElement('li');
        li.innerText = note.title;
        li.onclick = () => loadNoteGraph(note.title);
        notesList.appendChild(li);
      });
    });
}

function createNewNote() {
  const title = prompt('Enter note title:');
  if (title) {
    fetch('http://localhost:8000/notes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title, nodes: [] })
    }).then(() => fetchNotes());
  }
}

function loadNoteGraph(title) {
  fetch(`http://localhost:8000/notes/${title}`)
    .then(response => response.json())
    .then(data => {
      const nodes = new vis.DataSet(data.nodes.map((label, id) => ({ id, label })));
      const edges = new vis.DataSet(data.edges);

      const container = document.getElementById('mynetwork');
      const networkData = { nodes, edges };
      const options = {};
      const network = new vis.Network(container, networkData, options);

      currentGraph = { title, network };
    });
}

function addNode() {
  if (currentGraph) {
    const label = prompt('Enter node label:');
    if (label) {
      fetch(`http://localhost:8000/notes/${currentGraph.title}/nodes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ label })
      }).then(() => loadNoteGraph(currentGraph.title));
    }
  }
}
