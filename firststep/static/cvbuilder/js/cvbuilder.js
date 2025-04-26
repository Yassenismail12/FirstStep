let sectionCount = 0;

function addSection() {
  sectionCount++;
  const container = document.getElementById('sectionsContainer');
  const section = document.createElement('div');
  section.className = "border p-3 mb-3";
  section.innerHTML = `
    <h5>Section ${sectionCount}</h5>
    <input type="text" name="sections[${sectionCount}][type]" placeholder="Section Type (e.g. Experience)" class="form-control mb-2" required>
    <div class="entries">
      <div class="entry mb-2">
        <input type="text" name="sections[${sectionCount}][entries][0][title]" placeholder="Title" class="form-control mb-1">
        <input type="text" name="sections[${sectionCount}][entries][0][subtitle]" placeholder="Subtitle" class="form-control mb-1">
        <textarea name="sections[${sectionCount}][entries][0][description]" placeholder="Description" class="form-control mb-1"></textarea>
        <input type="text" name="sections[${sectionCount}][entries][0][location]" placeholder="Location" class="form-control mb-1">
      </div>
    </div>
    <button type="button" class="btn btn-sm btn-outline-primary" onclick="addEntry(this, ${sectionCount})">Add Entry</button>
  `;
  container.appendChild(section);
}

function addEntry(button, sectionIndex) {
  const section = button.closest('.border');
  const entries = section.querySelector('.entries');
  const entryIndex = entries.children.length;
  const newEntry = document.createElement('div');
  newEntry.className = "entry mb-2";
  newEntry.innerHTML = `
    <input type="text" name="sections[${sectionIndex}][entries][${entryIndex}][title]" placeholder="Title" class="form-control mb-1">
    <input type="text" name="sections[${sectionIndex}][entries][${entryIndex}][subtitle]" placeholder="Subtitle" class="form-control mb-1">
    <textarea name="sections[${sectionIndex}][entries][${entryIndex}][description]" placeholder="Description" class="form-control mb-1"></textarea>
    <input type="text" name="sections[${sectionIndex}][entries][${entryIndex}][location]" placeholder="Location" class="form-control mb-1">
  `;
  entries.appendChild(newEntry);
}
